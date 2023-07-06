import asyncio
import os
import sys
import json
import storage
from network import Server
sys.path.append('instruction_parser/')
from instruction_parser.command import Add

def run(ip, port):
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log = logging.getLogger('kademlia')
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    """
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    server = Server(storage=storage.FileStorage())
    loop.run_until_complete(server.listen(int(port), ip))

    first_node = (ip, port)
    inst = ['python3', 'tcp_server.py', ip, port]
    pid = os.fork()
    if pid:
        print(str(first_node) + " ---> " + str(pid))
    else:
        os.execvp(inst[0], inst)

    #############load state################## 
    # try:
    #     with open("secure/state.json", "r") as f:
    #         data_dict = json.load(f)
    #     for key in data_dict.keys():
    #         print(type(key),flush=True)
    #         add = Add([key], data_dict[key])
    #         loop.run_until_complete(add.execute(server))
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

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])