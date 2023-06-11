import asyncio
import os
import pickle
import sys

sys.path.append('auxiliar/')
from auxiliar.parser import CommandParser
from auxiliar.tcp_utils import download
from auxiliar.utils import infix_postfix, ops
from network import Server
from storage import FileStorage


async def operation(response, server):
    if response[0] == 'add':
        return await add(response[1], response[2], server)
    elif response[0] == 'add-tags':
        return await add_tags(response[1], response[2], server)
    elif response[0] == 'delete':
        return await delete(response[1], server)
    elif response[0] == 'delete-tags':
        return await delete_tags(response[1], response[2], server)
    elif response[0] == 'list':
        files, _ = await list(response[1], server, prt=True)
        return files
    elif response[0] == 'get':
        return await get(response[1], server)

async def add(file_list, tag_list, server):
    for t in tag_list:
        for i in range(len(file_list)):
            await server.set(t, file_list[i], file_list[i])

async def add_tags(tag_query, tag_list, server):
    response = await get_fileIds(tag_query, server)
    for t in tag_list:
        for f in response:
            try:
                r = pickle.loads(await server.get(t, True))
                r = r.keys()
                if f not in r:
                    # print('not match')
                    await server.set(t, None ,f, False)

            except:
                l = (await server.get(f, False))
                l = l.keys()
                # print(l)
                # input()
                f1, tags, name = pickle.loads(l)
                await server.set(t, name ,pickle.loads(f1), True)



async def get_fileIds(tag_query, server, prt=False):
    files = []
    tokens = infix_postfix(tag_query)
    if len(tokens) == 1:
        try:
            l, nodes_per_values = await server.get(tokens[0], True)
            file_ids = pickle.loads(l)
            if prt:
                print("Get result:", end=" ")
                print(file_ids)
            return file_ids

        except:
            return files

    else:
        stack = []
        for item in tokens:
            if item in ops:
                if item == 'not':
                    pass
                else:
                    op1 = stack.pop()
                    op2 = stack.pop()

                    if item == 'and':
                        # stack.append(op1 and op2)
                        if not op1 or not op2:
                            stack.append(set())
                        stack.append(op1.intersection(op2))
                    else:
                        # stack.append(op1 or op2)
                        if not op1 and op2:
                            stack.append(op2)
                        elif op1 and not op2:
                            stack.append(op1)
                        elif not op1 and not op2:
                            stack.append(set())
                        else:
                            stack.append(op1.union(op2))
            else:
                load, nodes_per_values = await server.get(item, True)

                if load:
                    stack.append(pickle.loads(load))
                else:
                    stack.append(set())

        result = stack.pop()
        # files = []
        # for f in result:
        #     files.append(pickle.loads(await server.get(f, False)))
        if prt:
            print("Get result:", end=" ")
            print(result)
        return result

#todo list de verdad
async def list(tag_query, server, prt = False):
    to_return = []
    nodes_per_value = {}
    fids = await get_fileIds(tag_query, server, False)
    if len(fids):
        for f in fids:
            l, d = (await server.get(f, False))
            nodes_per_value.update(d)
            if not l:
                print('No results')
                return
            f, tags, name = pickle.loads(l)

            to_return.append((name, pickle.loads(f)))
            result = 'file: ' + name + ' tags:'
            for t in pickle.loads(tags):
                result += ' ' + t

            print(result)
    else:
        print('No results')

    return to_return, nodes_per_value

async def get(tag_query, server):
    info, nodes_per_value = await list(tag_query, server)
    # print(info)
    #print(nodes_per_value,'desde get',flush=True)
    for key in nodes_per_value.keys():
        _, _, name = pickle.loads(key)
        nodes = nodes_per_value[key]
        for node in nodes:
            node = node.split(':')
            ip = node[0]
            port = node[1]
            succes = await download(ip, int(port), name)
            if succes:
                break

    # for name, file in info:
    #     w = open('downloads/' + name, "wb")
    #     w.write(file)
    #     w.close()

async def delete(tag_query, server):
    files = await get_fileIds(tag_query, server, False)
    for f in files:
        l = (await server.get(f, False))
        l = l.keys()
        # print(l)
        # input()
        if not l:
            continue
        f1, tags, name = pickle.loads(l)
        tag_list = pickle.loads(tags)
        for t in tag_list:
            await server.delete_tag(t, f)

        await server.delete(f, False)

async def delete_tags(tag_query, tag_list, server):
    files = await get_fileIds(tag_query, server, False)
    for t in tag_list:
        for f in files:
            await server.delete_tag(t, f)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python3 client.py <client ip> <client port > <bootstrap routing_node> <bootstrap routing_port>")
        sys.exit(1)

    parser = CommandParser()

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
            loop.run_until_complete(operation(parser(inp), server))

        except Exception as e:
            if e == KeyboardInterrupt:
                server.close()
                loop.close()
                break
            print(e)