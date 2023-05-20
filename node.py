from operator import itemgetter
import heapq


class Node:
    def __init__(self, node_id, ip=None, port=None):
        self.id = node_id
        self.ip = ip
        self.port = port
        self.long_id = int(node_id.hex(), 16)

    

    '''
    Kedemlia XOR distance metric distance
    '''
    def distance_to(self, node):
        return self.long_id ^ node.long_id
    
    def same_ip_port(self, node):
        return self.ip == node.ip and self.port == node.port

    def __iter__(self):
        return iter([self.id, self.ip, self.port])

    def __repr__(self):
        return repr([self.long_id, self.ip, self.port])

    def __str__(self):
        return "%s:%s" % (self.ip, str(self.port))
    

class NodeHeap:
    def __init__(self, node, maxsize):
        self.node = node
        self.heap = []
        self.maxsize = maxsize
        self.contacted = set()

    def get_node(self, node_id):
        for _, node in self.heap:
            if node.id == node_id:
                return node
        return None

    def remove(self, nodes):
        nodes = set(nodes)
        if not nodes:
            return
        nheap = []
        for distance, node in self.heap:
            if node.id not in nodes:
                heapq.heappush(nheap, (distance, node))
        self.heap = nheap


    def push(self, nodes):
        if not isinstance(nodes, list):
            nodes = [nodes]

        for node in nodes:
            if node not in self:
                distance = self.node.distance_to(node)
                heapq.heappush(self.heap, (distance, node))

    def pop(self):
        return heapq.heappop(self.heap)[1] if self else None

    
    def __len__(self):
        return min(len(self.heap), self.maxsize)

    def __iter__(self):
        nodes = heapq.nsmallest(self.maxsize, self.heap)
        return iter(map(itemgetter(1), nodes))

    def __contains__(self, node):
        for _, other in self.heap:
            if node.id == other.id:
                return True
        return False

    
