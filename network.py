import random
import pickle
import asyncio
import logging


from kademlia.protocol import KademliaProtocol


log = logging.getLogger(__name__)

class Server:

    protocol_class = KademliaProtocol

    def __init__(self, ksize=20, alpha=3, node_id=None, storage=None):
        self.ksize = ksize
        self.alpha = alpha
        self.storage = None
        self.node = Node(node_id or digest(random.getrandbits(255)))
        self.transport = None
        self.protocol = None
        self.refresh_loop = None
        self.save_state_loop = None

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

    def refresh_table(self):
        log.debug("Refreshing routing table")
        asyncio.ensure_future(self._refresh_table())
        loop = asyncio.get_event_loop()
        self.refresh_loop = loop.call_later(3600, self.refresh_table)

    

    async def bootstrappable_neighbors(self):
        neighbors = self.protocol.router.find_neighbors(self.node)
        print(neighbors) # added by myselfs
        return [tuple(n)[-2:] for n in neighbors]

   
