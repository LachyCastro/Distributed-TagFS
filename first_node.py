import asyncio
import os
import sys

import storage
from network import Server


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
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])