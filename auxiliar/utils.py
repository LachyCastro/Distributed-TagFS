import asyncio
import hashlib

ops = ['or', 'and', 'not']
prec = { 'and': 1, 'or': 1, 'not': 2, '(': 0, ')': 0 }


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
