import asyncio
import logging
import random
import sys

from routing import RoutingTable

sys.path.append('auxiliar/')
from auxiliar.node import Node
from auxiliar.tcp_utils import send_file
from auxiliar.utils import digest
from protocol.rpc import RPCProtocol

log = logging.getLogger(__name__)


class KademliaProtocol(RPCProtocol):
    def __init__(self, source_node, storage, ksize):
        RPCProtocol.__init__(self)
        self.router = RoutingTable(self, ksize, source_node)
        self.storage = storage
        self.source_node = source_node

    def get_refresh_ids(self):
        ids = []
        for bucket in self.router.lonely_buckets():
            rid = random.randint(*bucket.range).to_bytes(20, byteorder='big')
            ids.append(rid)
        return ids

    def rpc_stun(self, sender):
        return sender

    def rpc_ping(self, sender, nodeid):
        source = Node(nodeid, sender[0], sender[1])
        self.welcome_if_new(source)
        return self.source_node.id

    def rpc_store(self, sender, nodeid, dkey, key, name, value, hash = True):
        source = Node(nodeid, sender[0], sender[1])
        self.welcome_if_new(source)
        log.debug("got a store request from %s, storing '%s'='%s'",
                  sender, dkey.hex(), value)
        self.storage.set(dkey, key, name, value, hash)
        return True

    def rpc_delete(self, sender, nodeid, key):
        source = Node(nodeid, sender[0], sender[1])
        self.welcome_if_new(source)
        log.debug("got a delete request from %s, deleting '%s'",
                  sender, key.hex())
        self.storage.delete(key)
        return True

    def rpc_delete_tag(self, sender, nodeid, dkey, key, value):
        source = Node(nodeid, sender[0], sender[1])
        self.welcome_if_new(source)
        log.debug("got a delete request from %s, deleting '%s'",
                  sender, dkey.hex())
        self.storage.delete_tag(dkey, key, value)
        return True

    def rpc_find_node(self, sender, nodeid, key):
        log.info("finding neighbors of %i in local table",
                 int(nodeid.hex(), 16))
        source = Node(nodeid, sender[0], sender[1])
        self.welcome_if_new(source)
        node = Node(key)
        neighbors = self.router.find_neighbors(node, exclude=source)
        return list(map(tuple, neighbors))

    def rpc_find_value(self, sender, nodeid, key):
        source = Node(nodeid, sender[0], sender[1])
        self.welcome_if_new(source)
        value = self.storage.get(key, None)
        if value is None:
            return self.rpc_find_node(sender, nodeid, key)
        return {'value': value}

    async def call_find_node(self, node_to_ask, node_to_find):
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.find_node(address, self.source_node.id,
                                      node_to_find.id)
        return self.handle_call_response(result, node_to_ask)

    async def call_find_value(self, node_to_ask, node_to_find):
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.find_value(address, self.source_node.id,
                                       node_to_find.id)
        return self.handle_call_response(result, node_to_ask)

    async def call_ping(self, node_to_ask):
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.ping(address, self.source_node.id)
        return self.handle_call_response(result, node_to_ask)

    async def call_store(self, node_to_ask, dkey, key, name=None, value=None, hash=True):
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.store(address, self.source_node.id,dkey, key, name, value, hash)
        if result[0] and name:
            file_result = await send_file(node_to_ask.ip, node_to_ask.port,name)
            result = result and file_result
        return self.handle_call_response(result, node_to_ask)

    async def call_delete(self, node_to_ask, key):
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.delete(address, self.source_node.id, key)
        #if result[0]:
        #    await delete(node_to_ask.ip, node_to_ask.port,name)
        return self.handle_call_response(result, node_to_ask)

    async def call_delete_tag(self, node_to_ask, dkey ,key, value):
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.delete_tag(address, self.source_node.id, dkey ,key, value)
        return self.handle_call_response(result, node_to_ask)

    def welcome_if_new(self, node):
        if not self.router.is_new_node(node):
            return

        log.info("never seen %s before, adding to router", node)
        for key, value in self.storage:
            keynode = Node(digest(key))
            neighbors = self.router.find_neighbors(keynode)
            if neighbors:
                last = neighbors[-1].distance_to(keynode)
                new_node_close = node.distance_to(keynode) < last
                first = neighbors[0].distance_to(keynode)
                this_closest = self.source_node.distance_to(keynode) < first
            if not neighbors or (new_node_close and this_closest):
                asyncio.ensure_future(self.call_store(node, key, value))
        self.router.add_contact(node)

    def handle_call_response(self, result, node):
        if not result[0]:
            #log.warning("no response from %s, removing from router", node)
            self.router.remove_contact(node)
            return result

        #log.info("got successful response from %s", node)
        self.welcome_if_new(node)
        return result
