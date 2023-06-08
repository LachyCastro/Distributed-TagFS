import asyncio
import sys

import storage
from network import Server

# Usage: <python3> <node_ip> <node_port> <bootstrap_node_ip> <bootstrap_node_port>

loop = asyncio.get_event_loop()
loop.set_debug(True)

server = Server(storage=storage.FileStorage())
loop.run_until_complete(server.listen(int(sys.argv[2]), sys.argv[1]))
bootstrap_node = (sys.argv[3], int(sys.argv[4]))
loop.run_until_complete(server.bootstrap([bootstrap_node]))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.stop()
    loop.close()