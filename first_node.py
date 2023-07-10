import asyncio
import os
import sys
import json
import storage
from network import Server
sys.path.append('instruction_parser/')

from instruction_parser.command import Add
sys.path.append('auxiliar/')

from auxiliar.utils import create_folders

def run(ip, port):
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log = logging.getLogger('kademlia')
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    """

    create_folders()

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

    async def execute(files, tags, server,prt = True):
            for t in tags:
                for i in range(len(files)):
                    with open('secure/'+files[i], 'rb') as file:
                        content = file.read()
                    name = files[i].split('|')[-1]
                    value = files[i].split('|')[0]
                    await server.set(t, name, value)
    #try:
    with open("secure/state.json", "r") as f:
        data_dict = json.load(f)
    for key in data_dict.keys():
        print(type(key),flush=True)
        loop.run_until_complete(execute([key], data_dict[key], server))
    #except:
    #    pass
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