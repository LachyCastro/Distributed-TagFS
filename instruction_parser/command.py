import hashlib
import os
import pickle
import sys
from abc import ABC, abstractmethod

# Get the absolute path to the root directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the root directory to sys.path
sys.path.insert(0, root_dir)

sys.path.append('auxiliar/')
from auxiliar.tcp_utils import delete_file, download
from auxiliar.utils import infix_postfix, ops


class Command(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass
    @abstractmethod
    async def execute(self, server, prt = True):
        pass

    async def get_fileIds(self, tag_query, server, prt=False):
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

class Add(Command):
    def __init__(self, files, tags) -> None:
        self.files = files
        self.tags = tags
    async def execute(self, server, prt = True):
        for t in self.tags:
            for i in range(len(self.files)):
                with open(self.files[i], 'rb') as file:
                    content = file.read()
                name_and_content = self.files[i].encode() + content
                value = hashlib.md5(name_and_content).hexdigest()
                await server.set(t, self.files[i], value)

class Delete(Command):
    def __init__(self, tags) -> None:
        self.tags = tags
    async def execute(self, server, prt = True):
        files = await super().get_fileIds(self.tags, server, False)
        list = List(self.tags)
        info, nodes_per_value = await list.execute(server, prt=False)

        for f in files:
            l, _ = (await server.get(f, False))
        
            if not l:
                continue
            f1, tags, name = pickle.loads(l)
            tag_list = pickle.loads(tags)
            for t in tag_list:
                await server.delete_tag(t, f)

            await server.delete(f, False)

        for key in nodes_per_value.keys():
            value, _, name = pickle.loads(key)
            value = pickle.loads(value)
            nodes = nodes_per_value[key]
            for node in nodes:
                node = node.split(':')
                ip = node[0]
                port = node[1]
                await delete_file(ip, int(port), name, value)
    
class List(Command):
    def __init__(self, tags) -> None:
        self.tags = tags
    async def execute(self, server, prt=True):
        to_return = []
        nodes_per_value = {}
        fids = await super().get_fileIds(self.tags, server, False)

        if len(fids):
            for f in fids:
            
                l, d = (await server.get(f, False))
                if d: nodes_per_value.update(d)
                if not l and prt:
                    print('No results')
                    return
                f, tags, name = pickle.loads(l) 

                to_return.append((name, pickle.loads(f)))
                
                result = 'file: ' + name + ' tags:'
                for t in pickle.loads(tags):
                    result += ' ' + t
                if prt: print(result)
        elif prt:
            print('No results')
        return to_return, nodes_per_value
    
class AddTags(Command):
    def __init__(self, query, tags) -> None:
        self.query = query
        self.tags = tags
    async def execute(self, server, prt = True):
        response = await super().get_fileIds(self.query, server)
        for t in self.tags:
            for f in response:
                try:
                    r, _ = await server.get(t, True)
                    r = pickle.loads(r)
                    if f not in r:
                        # print('not match')
                        await server.set(t, None ,f, False)

                except:
                    l, _ = (await server.get(f, False))
                    # print(l)
                    # input()
                    f1, tags, name = pickle.loads(l)
                    await server.set(t, name ,pickle.loads(f1), True)
    
class DeleteTags(Command):
    def __init__(self, query, tags) -> None:
        self.query = query
        self.tags = tags
    async def execute(self, server, prt = True):
        files = await super().get_fileIds(self.tags, server, False)
        for t in self.tags:
            for f in files:
                await server.delete_tag(t, f)

class Get(Command):
    def __init__(self, tags) -> None:
        self.tags = tags
    async def execute(self, server, prt = True):
        list = List(self.tags)
        info, nodes_per_value = await list.execute(server)
        for key in nodes_per_value.keys():
            value, _, name = pickle.loads(key)
            value = pickle.loads(value)
            nodes = nodes_per_value[key]
            for node in nodes:
                node = node.split(':')
                ip = node[0]
                port = node[1]
                success = await download(ip, int(port), name, value)
                if success:
                    break

