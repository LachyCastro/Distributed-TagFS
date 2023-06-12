import asyncio
import os
import sys

sys.path.append('instruction_parser/')
from network import Server
from storage import FileStorage

sys.path.append('instruction_parser/')
from instruction_parser.ply_parser import parser

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python3 client.py <client ip> <client port > <bootstrap routing_node> <bootstrap routing_port>")
        sys.exit(1)

    
    loop = asyncio.get_event_loop()
    server = Server(storage=FileStorage())
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
        
    inst = ['echo', '', '>', '/Test/output']

    
    while True:
        try:
            print(' >>', end=' ')
            inp = input()
            if not len(inp):
                continue
            response_parser = parser.parse(inp)
            loop.run_until_complete(response_parser.execute(server))
        except Exception as e:
            if e == KeyboardInterrupt:
                server.close()
                loop.close()
                break
            print(e)