import asyncio
import hashlib
import os

ops = ['||', '&', '~']
prec = { '&': 1, '||': 1, '~': 2, '(': 0, ')': 0 }


async def gather_dict(dic):
    cors = list(dic.values())
    results = await asyncio.gather(*cors)
    return dict(zip(dic.keys(), results))

def digest(string):
    if not isinstance(string, bytes):
        string = str(string).encode('utf8')
    return hashlib.sha1(string).digest()

def split(args):
    l1 = args.replace('(', '( ')
    l2 = l1.replace(')', ' )')
    return l2.split()
    

def infix_postfix(tokens):
    stack = []
    output = []
    for item in tokens:
        if item in ops:
            while stack and prec[stack[-1]] >= prec[item]:
                output.append(stack.pop())
            stack.append(item)
        elif item == "(":
            stack.append("(")
        elif item == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
        else:
            output.append(item)
    while stack:
        output.append(stack.pop())
    return output

def create_folders():
    if not os.path.isdir("secure/"):
        os.mkdir("secure", 0o700)
        print("\nSecure Folder Created!\n")

    # Create state.json file in secure folder if it does not exist
    if not os.path.isfile("secure/state.json"):
        with open("secure/state.json", "w") as f:
            f.write("{}")
        print("\nState file created!\n")


    if not os.path.isdir("download/"):
        os.mkdir("download", 0o700)
        print("\nDownload Folder Created!\n")
