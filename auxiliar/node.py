import heapq
from operator import itemgetter


class Node:
    def __init__(self, node_id, ip=None, port=None):
        self.id = node_id
        self.ip = ip
        self.port = port
        self.long_id = int(node_id.hex(), 16)

    def same_home_as(self, node):
        return self.ip == node.ip and self.port == node.port

    def distance_to(self, node):
        return self.long_id ^ node.long_id

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
        self.contacted = set()
        self.maxsize = maxsize

    def remove(self, peers):
        peers = set(peers)
        if not peers:
            return
        nheap = []
        for distance, node in self.heap:
            if node.id not in peers:
                heapq.heappush(nheap, (distance, node))
        self.heap = nheap

    def get_node(self, node_id):
        for _, node in self.heap:
            if node.id == node_id:
                return node
        return None

    def have_contacted_all(self):
        return len(self.get_uncontacted()) == 0

    def get_ids(self):
        return [n.id for n in self]

    def mark_contacted(self, node):
        self.contacted.add(node.id)

    def popleft(self):
        return heapq.heappop(self.heap)[1] if self else None

    def push(self, nodes):
        if not isinstance(nodes, list):
            nodes = [nodes]

        for node in nodes:
            if node not in self:
                distance = self.node.distance_to(node)
                heapq.heappush(self.heap, (distance, node))

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

    def get_uncontacted(self):
        return [n for n in self if n.id not in self.contacted]
