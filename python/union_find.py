#!/usr/bin/env python

# TODO: Add path compression.

VERBOSE = True

class UFNode:
    def __init__(self, val):
        self.val = val
        self.rank = 0
        self.parent = None
        self.children = []

    def __str__(self):
        children_vals = [child.val for child in self.children]
        result = f'value={self.val},rank={self.rank}; parent={self.parent}, children={",".join(map(str, children_vals))}'
        return result


class UnionFind:
    def __init__(self, arg):
        if isinstance(arg, int) and arg > 1:
            vals = range(arg)
        else:
            assert(isinstance(arg, list))
            vals = arg
        self.nodes: Dict[Any, UFNode] = {val: UFNode(val) for val in vals}
        self._assert_invariant()

    def _adopt(self, root_p: UFNode, root_c: UFNode):
        self._assert_invariant()
        assert(root_p.val in self.nodes)
        assert(root_c.val in self.nodes)
        root_c.parent = root_p
        root_p.rank = max(root_c.rank + 1, root_p.rank)
        root_p.children += [root_c] + root_c.children
        # root_c.children = []

    def _assert_invariant(self):
        assert(isinstance(self.nodes, dict))

    def find_root(self, x) -> UFNode:
        self._assert_invariant()
        p: UFNode = self.nodes[x]
        while True:
            if p.parent:
                p = p.parent
            else:
                break
        assert(p)
        return p

    def is_equiv(self, x, y) -> bool:
        self._assert_invariant()
        return self.find_root(x) == self.find_root(y)

    def print(self, msg):
        self._assert_invariant()
        print(msg)
        for node in [node for node in self.nodes.values() if node.parent is None]:
            children_values = [child.val for child in node.children]
            print(f'\tUFNode: Children of {node.val}: {children_values}')

    def union(self, x, y):
        self._assert_invariant()
        root_x = self.find_root(x)
        root_y = self.find_root(y)
        if root_x == root_y:
            return
        else:
            if root_x.rank >= root_y.rank:
                self._adopt(root_x, root_y)
            else:
                self._adopt(root_y, root_x)


if __name__ == '__main__':
    uf = UnionFind(20)

    # First merge
    for other in range(1, 10):
        uf.union(0, other)

    # Second merge
    for other in range(11, 20):
        uf.union(10, other)

    uf.print('UnionFind contents in two disjoint sets:')
    uf.union(0, 10)
    uf.print('UnionFind contents merged into one set:')
