import json
import os
import signal

pids = []

def init(hosts):
    first_node = (hosts['host_0'][0], hosts['host_0'][1])
    inst = ['python3', 'first_node.py', first_node[0], first_node[1]]
    pid = os.fork()
    if pid:
        pids.append(pid)
        print(str(first_node) + " ---> " + str(pid))
    else:
        os.execvp(inst[0], inst)

    for i in range(1, len(hosts)):
        idx = 'host_' + str(i)
        inst = ['python3', 'tangled_node.py', hosts[idx][0], hosts[idx][1], first_node[0], first_node[1]]
        pid = os.fork()
        if pid:
            print(str((hosts[idx][0], hosts[idx][1])) + ' ---> ' + str(pid))
            pids.append(pid)
        else:
            os.execvp(inst[0], inst)

def run():
    with open("./hosts.json", "r") as f:
        hosts = json.load(f)

    print("<hosts> ----------------> <pid>")
    init(hosts)

def stop():
    for pid in pids:
        os.kill(pid, signal.SIGSTOP)

if __name__ == '__main__':
    run()
    print('>> running network successfuly!')
    while True:
        try:
            if str(input()) == 'stop':
                stop()
                print('>> stop network')
                break
        except KeyboardInterrupt:
            stop()
            print('>> stop network')
            break