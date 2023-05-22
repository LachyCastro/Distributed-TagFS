# Add this file to protocol folder

import asyncio
import heapq
import operator
import time
from collections import OrderedDict
from itertools import chain

from routing_utils import bytes_to_bit_string, shared_prefix


class RoutingTable:

    def __init__(self, node, ksize, protocol ) -> None:
        self.node = node
        self.protocol = protocol
        self.ksize = ksize
        self.buckets = [KBucket(0, 2 ** 160, self.ksize)]
    
    def add_contact(self, node):
        index = self.get_bucket_for(node)
        bucket = self.buckets[index]

        if bucket.add_node(node):
            return

        if bucket.has_in_range(self.node) or bucket.depth() % 5 != 0:
            self.split_bucket(index)
            self.add_contact(node)
        else:
            asyncio.ensure_future(self.protocol.call_ping(bucket.head()))

    def remove_contact(self, node):
        index = self.get_bucket_for(node)
        self.buckets[index].remove_node(node)
    
    def get_bucket_for(self, node):
        for index, bucket in enumerate(self.buckets):
            if node.long_id < bucket.range[1]:
                return index
        return None
    
    def split_bucket(self, index):
        one, two = self.buckets[index].split()
        self.buckets[index] = one
        self.buckets.insert(index + 1, two)

    def lonely_buckets(self):
        hour_ago = time.monotonic() - 3600
        return [b for b in self.buckets if b.last_updated < hour_ago]
    
    def is_new_node(self, node):
        index = self.get_bucket_for(node)
        return self.buckets[index].is_new_node(node)
    
    def find_neighbors(self, node, k=None, exclude=None):
        k = k or self.ksize
        nodes = []
        for neighbor in TableTraverser(self, node):
            not_excluded = exclude is None or not neighbor.same_home_as(exclude) #<-- exclude or node ??
            if neighbor.id != node.id and not_excluded:
                heapq.heappush(nodes, (node.distance_to(neighbor), neighbor))
            if len(nodes) == k:
                break

        return list(map(operator.itemgetter(1), heapq.nsmallest(k, nodes)))

    
class KBucket:
    def __init__(self, rangeLower, rangeUpper, ksize):
        self.range = (rangeLower, rangeUpper)
        self.nodes = OrderedDict()
        self.replacement_nodes = OrderedDict()
        self.touch_last_updated()
        self.ksize = ksize

    def touch_last_updated(self):
        self.last_updated = time.monotonic()

    def add_node(self, node):

        if node.id in self.nodes:
            del self.nodes[node.id]
            self.nodes[node.id] = node
        elif len(self) < self.ksize:
            self.nodes[node.id] = node
        else:
            if node.id in self.replacement_nodes:
                del self.replacement_nodes[node.id]
            self.replacement_nodes[node.id] = node
            return False
        return True
    
    def remove_node(self, node):
        if node.id in self.replacement_nodes:
            del self.replacement_nodes[node.id]

        if node.id in self.nodes:
            del self.nodes[node.id]

            if self.replacement_nodes:
                newnode_id, newnode = self.replacement_nodes.popitem()
                self.nodes[newnode_id] = newnode

    
    def has_in_range(self, node):
        return self.range[0] <= node.long_id <= self.range[1]
    
    def split(self):
        midpoint = (self.range[0] + self.range[1]) / 2
        one = KBucket(self.range[0], midpoint, self.ksize)
        two = KBucket(midpoint + 1, self.range[1], self.ksize)
        nodes = chain(self.nodes.values(), self.replacement_nodes.values())
        for node in nodes:
            bucket = one if node.long_id <= midpoint else two
            bucket.add_node(node)

        return (one, two)
    
    def depth(self):
        vals = self.nodes.values()
        sprefix = shared_prefix([bytes_to_bit_string(n.id) for n in vals])
        return len(sprefix)
    
    def is_new_node(self, node):
        return node.id not in self.nodes
    
    def head(self):
        return list(self.nodes.values())[0]
    
    def get_nodes(self):
        return list(self.nodes.values())
    
    def __getitem__(self, node_id):
        return self.nodes.get(node_id, None)

    def __len__(self):
        return len(self.nodes)


class TableTraverser:
    def __init__(self, table, startNode):
        index = table.get_bucket_for(startNode)
        table.buckets[index].touch_last_updated()
        self.current_nodes = table.buckets[index].get_nodes()
        self.left_buckets = table.buckets[:index]
        self.right_buckets = table.buckets[(index + 1):]
        self.left = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_nodes:
            return self.current_nodes.pop()

        if self.left and self.left_buckets:
            self.current_nodes = self.left_buckets.pop().get_nodes()
            self.left = False
            return next(self)

        if self.right_buckets:
            self.current_nodes = self.right_buckets.pop(0).get_nodes()
            self.left = True
            return next(self)

        raise StopIteration