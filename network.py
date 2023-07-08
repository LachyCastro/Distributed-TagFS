import asyncio
import logging
import pickle
import random
import sys
import os
import json

sys.path.append('auxiliar/')
sys.path.append('crawler/')
sys.path.append('kademlia/')
sys.path.append('protocol/')

from auxiliar.node import Node
from auxiliar.tcp_utils import send_file
from auxiliar.utils import digest
from crawler.crawling import NodeSpiderCrawl, ValueSpiderCrawl
from kademlia.protocol import KademliaProtocol
from storage import ForgetfulStorage

log = logging.getLogger(__name__)

class Server:

    protocol_class = KademliaProtocol

    def __init__(self, ksize=20, alpha=3, node_id=None, storage=None, is_client=False):
        self.ksize = ksize
        self.alpha = alpha
        self.storage = (storage or ForgetfulStorage())
        self.node = Node(node_id or digest(random.getrandbits(255)))
        self.transport = None
        self.protocol = None
        self.refresh_loop = None
        self.save_state_loop = None
        self.is_client = is_client

    def stop(self):
        if self.transport is not None:
            self.transport.close()

        if self.refresh_loop:
            self.refresh_loop.cancel()

        if self.save_state_loop:
            self.save_state_loop.cancel()

    def _create_protocol(self):
        return self.protocol_class(self.node, self.storage, self.ksize)

    async def listen(self, port, interface='0.0.0.0'):
        self.node = Node(self.node.id, interface, port)
        loop = asyncio.get_event_loop()
        listen = loop.create_datagram_endpoint(self._create_protocol,
                                               local_addr=(interface, port))
        log.info("Node %i listening on %s:%i",
                 self.node.long_id, interface, port)
        self.transport, self.protocol = await listen
        # finally, schedule refreshing table
        self.refresh_table()
        if not self.is_client:
            loop = asyncio.get_event_loop()
            self.refresh_loop = loop.call_later(60, self.collect_garbage)
        

    def collect_garbage(self):
        log.debug("Collecting garbage")
        asyncio.ensure_future(self._collect_garbage())
        loop = asyncio.get_event_loop()
        self.refresh_loop = loop.call_later(60, self.collect_garbage)

    async def _collect_garbage(self):
        filenames = os.listdir("secure")
        if 'state.json' in filenames:
            filenames.remove('state.json')
        
        with open("secure/state.json", "r") as _f:
            data_dict = json.load(f)

        for f in filenames:
            splitted_f= f.split('|')
            hash_val_cont= digest(splitted_f[0])
            if (len(splitted_f)!= 2) or (hash_val_cont not in self.storage.data_file.keys()):
                try:
                    os.remove("secure/"+f)
                    del data_dict[f]
                    with open("secure/state.json", "w") as _f:
                        json.dump(data_dict, f)
                    with open("secure/state.json", "r") as _f:
                        data_dict = json.load(f)
                except:
                    pass
            else:
                # If the file is in the storage, add tags from state.json if needed
                _f,_t,_name= pickle.loads(self.storage.data_file[hash_val_cont][1])
                tags= pickle.loads(_t)
                tags_in_json= data_dict[f]
                tags_to_add= [tag for tag in tags_in_json if tag not in tags]
                for tag_item in tags_to_add:
                    self.set(tag_item, _name, pickle.loads(_f), hash = True)
        

    def refresh_table(self):
        log.debug("Refreshing routing table")
        asyncio.ensure_future(self._refresh_table())
        loop = asyncio.get_event_loop()
        self.refresh_loop = loop.call_later(3600, self.refresh_table)

    async def _refresh_table(self):
        results = []
        for node_id in self.protocol.get_refresh_ids():
            node = Node(node_id)
            nearest = self.protocol.router.find_neighbors(node, self.alpha)
            spider = NodeSpiderCrawl(self.protocol, node, nearest,
                                     self.ksize, self.alpha)
            results.append(spider.find())

        await asyncio.gather(*results)

        # for dkey, value in self.storage.iter_older_than(3600):
        #     await self.set_digest(dkey, value)

    async def bootstrappable_neighbors(self):
        neighbors = self.protocol.router.find_neighbors(self.node)
        print(neighbors) # added by myselfs
        return [tuple(n)[-2:] for n in neighbors]

    async def bootstrap(self, addrs):
        log.debug("Attempting to bootstrap node with %i initial contacts",
                  len(addrs))
        cos = list(map(self.bootstrap_node, addrs))
        gathered = await asyncio.gather(*cos)
        nodes = [node for node in gathered if node is not None]
        spider = NodeSpiderCrawl(self.protocol, self.node, nodes,
                                 self.ksize, self.alpha)
        return await spider.find()

    async def bootstrap_node(self, addr):
        result = await self.protocol.ping(addr, self.node.id)
        return Node(result[1], addr[0], addr[1]) if result[0] else None

    async def get(self, key, hash=False):
        log.info("Looking up key %s", key)
        dkey = key
        if hash:
            dkey = digest(key)
        node = Node(dkey)
        nearest = self.protocol.router.find_neighbors(node)
        if not nearest:
            log.warning("There are no known neighbors to get key %s", key)
            return None, None
        spider = ValueSpiderCrawl(self.protocol, node, nearest,
                                  self.ksize, self.alpha)
        return await spider.find()

    async def delete(self, key, hash = True):
        dkey = key
        if hash:
            dkey = digest(key)
        """
        if self.storage.get(dkey) is not None:
            # delete the key from here
            self.storage.delete(dkey)
        """
        # also delete the key from neighbors
        node = Node(dkey)
        nearest = self.protocol.router.find_neighbors(node)
        if not nearest:
            log.warning("There are no known neighbors to get key %s", key)
            return None
        spider = NodeSpiderCrawl(self.protocol, node, nearest, self.ksize, self.alpha)
        nodes = await spider.find()

        results = [self.protocol.call_delete(n, dkey) for n in nodes]
        # return true only if at least one delete call succeeded
        return any(await asyncio.gather(*results))

    async def delete_tag(self, key, value):
        dkey = digest(key)

        node = Node(dkey)
        nearest = self.protocol.router.find_neighbors(node)
        if not nearest:
            log.warning("There are no known neighbors to set key %s", key)
            return None
        spider = NodeSpiderCrawl(self.protocol, node, nearest,
                                 self.ksize, self.alpha)
        nodes = await spider.find()
        log.info("setting '%s' on %s", dkey.hex(), list(map(str, nodes)))

        results = [self.protocol.call_delete_tag(n, dkey, key, value) for n in nodes]
        # return true only if at least one store call succeeded
        return any(await asyncio.gather(*results))

    async def set(self, key, name, value, hash = True):
        if not check_dht_value_type(value):
            raise TypeError(
                "Value must be of type int, float, bool, str, or bytes"
            )
        log.info("setting '%s' = '%s' on network", key, value)
        dkey = digest(key)
        return await self.set_digest(dkey, key, name , value, hash)

    async def set_digest(self, dkey, key , name, value, hash = True):
        node = Node(dkey)

        nearest = self.protocol.router.find_neighbors(node)
        if not nearest:
            log.warning("There are no known neighbors to set key %s",
                        dkey.hex())
            return False

        spider = NodeSpiderCrawl(self.protocol, node, nearest,
                                 self.ksize, self.alpha)
        nodes = await spider.find()

        log.info("setting '%s' on %s", dkey.hex(), list(map(str, nodes)))

        # if this node is close too, then store here as well
        biggest = max([n.distance_to(node) for n in nodes])
        if self.node.distance_to(node) < biggest:
            if await send_file(self.node.ip, self.node.port, name, key, value):
                self.storage.set(dkey, key, name , value, hash)

        results = [self.protocol.call_store(n, dkey, key, name, value,s_d=True, hash=hash) for n in nodes]
        # return true only if at least one store call succeeded
        return any(await asyncio.gather(*results))

    def save_state(self, fname):
        log.info("Saving state to %s", fname)
        data = {
            'ksize': self.ksize,
            'alpha': self.alpha,
            'id': self.node.id,
            'neighbors': self.bootstrappable_neighbors()
        }
        if not data['neighbors']:
            log.warning("No known neighbors, so not writing to cache.")
            return
        with open(fname, 'wb') as file:
            pickle.dump(data, file)

    @classmethod
    def load_state(cls, fname):
        log.info("Loading state from %s", fname)
        with open(fname, 'rb') as file:
            data = pickle.load(file)
        svr = Server(data['ksize'], data['alpha'], data['id'])
        if data['neighbors']:
            svr.bootstrap(data['neighbors'])
        return svr

    def save_state_regularly(self, fname, frequency=600):
        self.save_state(fname)
        loop = asyncio.get_event_loop()
        self.save_state_loop = loop.call_later(frequency,
                                               self.save_state_regularly,
                                               fname,
                                               frequency)


def check_dht_value_type(value):
    typeset = [
        int,
        float,
        bool,
        str,
        bytes,
        set
    ]
    return type(value) in typeset
