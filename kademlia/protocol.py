class KademliaProtocol(RPCProtocol): #RPCProtocol es RPC sobre UDP, hansel trabaja en eso 
    def __init__(self, source_node, storage, ksize):
       pass

    def get_refresh_ids(self):
        pass

    def rpc_stun(self, sender):
        return sender

    def rpc_ping(self):
        pass

    def rpc_store(self):
        pass

    def rpc_delete(self):
        pass

    def rpc_delete_tag(self):
        pass

    def rpc_find_node(self):
        pass
       

    def rpc_find_value(self):
        pass

    async def call_find_node(self):
        pass

    async def call_find_value(self):
        pass

    async def call_ping(self):
        pass

    async def call_store(self):
        pass

    async def call_delete(self):
       pass

    async def call_delete_tag(self):
        pass

    def welcome_if_new(self):
        pass

    def handle_call_response(self):
        pass

