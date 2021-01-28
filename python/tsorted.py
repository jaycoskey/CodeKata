#!/usr/bin/env python3

from typing import Dict
import unittest


# ----------------------------------------
# Decorators

def generator2list(f):
    def wrapped(*args, **kwargs):
        return list(f(*args, **kwargs))
    return wrapped

# ----------------------------------------

def is_tsorted(dep_rels:Dict, items):
    dep_keys = dep_rels.keys()
    prohibited = set()
    for item in items:
        if item in prohibited:
            # Came across a dependency after seeing the item it depended on
            return False
        if item in dep_keys:
            for dep in dep_rels[item]:
                prohibited.add(item)
    return True


@generator2list
def join(xs):
    for x in xs:
        if type(x) == list:
            yield from join(x)
        else:
            yield x


def print_tsorted(dep_rels:Dict, verbose=True):
    s = show_tsorted(dep_rels, verbose)
    print(s)


def show_tsorted(dep_rels:Dict, verbose=True):
    if verbose:
        print(f'Original items: {list(dep_rels.keys())}')
        for item in dep_rels.keys():
            print(f'\tDependency: {item:9s} --> {dep_rels[item]}')
    return tsorted(dep_rels)


def tsorted(dep_rels:Dict, verbose=True):
    """Returns a topologically sorted list of nodes.
    dep_rels - Dict: keys=all nodes ("start nodes"), values=dependencies
    """
    def add_followers(item):
        nonlocal dep_rels, seen_nodes, result
        if item not in seen_nodes:
            seen_nodes.add(item)
            for follower in dep_rels[item]:
                add_followers(follower)
            result.append(item)

    if not dep_rels:
        return []
    required_nodes = set(dep_rels.keys())
    after_nodes = set(join(dep_rels.values()))
    non_key_values = after_nodes.difference(required_nodes)
    if non_key_values:
        raise ValueError(f'Some values depending others are not listed as items to be tsorted: {non_key_values}')
    unseen_roots = required_nodes.difference(after_nodes)
    if not unseen_roots:
        raise ValueError("Cycle detected")
    node_count = len(required_nodes.union(after_nodes))
    seen_nodes = set()
    result = []
    while unseen_roots:
        add_followers(unseen_roots.pop())
    if len(result) < node_count:
        raise ValueError("Cycle detected: Not all nodes reachable from start nodes")
    return list(reversed(result))

# ----------------------------------------

class TestIsTsorted(unittest.TestCase):
    def test_is_tsorted(self):
        dep_rels = { 'a': ['b']
                   , 'b': ['c']
                   , 'c': []
                   }
        actual = tsorted(dep_rels)
        expected = ['a', 'b', 'c']
        self.assertEqual(actual, expected)


class TestJoin(unittest.TestCase):
    def test_join_lists(self):
        xss = [ [ [1,2,3], [4,5,[6,7,8]], [9] ] ]
        actual = join(xss)
        expected = list(range(1, 10))
        self.assertEqual(actual, expected)


class TestTsorted2(unittest.TestCase):
    def test_tsorted2(self):
        cycle_dep_rels = { 'a': []
                         , 'b': ['a']
                         }
        actual = tsorted(cycle_dep_rels)
        expected = ['b', 'a']
        self.assertEqual(actual, expected)


class TestTsortedCycle2(unittest.TestCase):
    def test_tsorted_cycle2(self):
        cycle_dep_rels = { 'a': ['b']
                         , 'b': ['a']
                         }
        self.assertRaises(ValueError, tsorted, cycle_dep_rels)


class TestTsortedCycle3(unittest.TestCase):
    def test_tsorted_cycle3(self):
        cycle_dep_rels = { 'a': ['b']
                         , 'b': ['c']
                         , 'c': ['a']
                         }
        self.assertRaises(ValueError, tsorted, cycle_dep_rels)


class TestTsortedClothing(unittest.TestCase):
    dep_rels = { 'belt': ['coat']
               , 'coat': []
               , 'pants': ['belt', 'shoes']
               , 'shirt': ['belt', 'coat']
               , 'shoes': []
               , 'socks': ['shoes']
               , 'underwear': ['pants']
               , 'watch': []
               }

    def test_tsorted_clothing(self):
        result = tsorted(self.__class__.dep_rels)
        self.assertTrue(is_tsorted(self.__class__.dep_rels, result))


class TestTsortedIncomplete(unittest.TestCase):
    def test_tsorted_incomplete(self):
        dep_rels = { 'a': ['b']
                   , 'b': ['c']
                   }
        self.assertRaises(ValueError, tsorted, dep_rels)

# ----------------------------------------

def demo_tsorted():
    print('===== tsorted demo =====')
    print_tsorted(TestTsortedClothing.dep_rels, verbose=True)


if __name__ == '__main__':
    # demo_tsorted()
    unittest.main()
