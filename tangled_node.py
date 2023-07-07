import asyncio
import os
import sys
import json
import storage
from network import Server
sys.path.append('instruction_parser/')
from instruction_parser.command import Add
# Usage: <python3> <node_ip> <node_port> <bootstrap_node_ip> <bootstrap_node_port>
loop = asyncio.get_event_loop()
loop.set_debug(True)

server = Server(storage=storage.FileStorage())
loop.run_until_complete(server.listen(int(sys.argv[2]), sys.argv[1]))
bootstrap_node = (sys.argv[3], int(sys.argv[4]))
loop.run_until_complete(server.bootstrap([bootstrap_node]))

client_node = (sys.argv[1], sys.argv[2])
inst = ['python3', 'tcp_server.py', sys.argv[1], sys.argv[2]]
pid = os.fork()
if pid:
    print(str(client_node) + " ---> " + str(pid))
else:
    os.execvp(inst[0], inst)

#############load state################## 
# try:
# with open("secure/state.json", "r") as f:
#     data_dict = json.load(f)
# for key in data_dict.keys():
#     print(type(key),flush=True)
#     add = Add([key], data_dict[key])
#     loop.run_until_complete(add.execute(server))
# except:
#     pass
###########################################

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.stop()
    loop.close()