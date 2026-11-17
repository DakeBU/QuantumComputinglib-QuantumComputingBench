"""Compare tree scheduling by global matching enumeration and by local slot assignment."""
from functools import cache
from itertools import permutations, product
import json


def all_matchings(edges):
    choices = [()]
    for u, v in edges:
        choices += [old + ((u, v),) for old in choices
                    if all(u not in edge and v not in edge for edge in old)]
    return choices


def globally_reachable(parents, budget):
    edges = [(u, v) for v, u in enumerate(parents, start=1)]
    layers = all_matchings(edges)
    states = {1}
    by_depth = [states]
    for _ in range(budget):
        following = set()
        for before in states:
            for matching in layers:
                after = before
                for u, v in matching:
                    pair = (1 << u) | (1 << v)
                    if before & pair:
                        after |= pair
                following.add(after)
        states = following
        by_depth.append(states)
    return by_depth


def subtree_recurrence(parents, weights, budget):
    children = [[] for _ in weights]
    for v, u in enumerate(parents, start=1):
        children[u].append(v)

    @cache
    def optimum(v, time):
        kids = children[v]
        count = min(time, len(kids))
        # Nonnegative masses allow first contacts to move to the earliest
        # available slots. Include zero-weight children when slots are spare.
        return weights[v] + max(
            sum(optimum(child, time - slot) for slot, child in enumerate(order, 1))
            for order in permutations(kids, count)
        )

    return [optimum(0, time) for time in range(budget + 1)]


def check():
    trees = instances = 0
    for n in range(1, 7):
        for parents in product(*(range(v) for v in range(1, n))):
            trees += 1
            reachable = globally_reachable(parents, 4)
            profiles = [[1] * n, [int(i == n-1) for i in range(n)],
                        [((2*i + n) % 5 - 2)**2 for i in range(n)]]
            for weights in profiles:
                expected = []
                for states in reachable:
                    expected.append(max(sum(w for i, w in enumerate(weights)
                                            if state & (1 << i)) for state in states))
                assert expected == subtree_recurrence(parents, weights, 4)
                instances += len(expected)
    return {'rooted_increasing_trees': trees, 'maximum_vertices': 6,
            'layer_budgets': [0, 1, 2, 3, 4], 'integer_weight_profiles_per_tree': 3,
            'optimum_comparisons': instances,
            'method': 'Enumerate all whole-tree matching layers and reachable sets. Independently maximize the local recurrence by child-slot permutations. Compare integer mass optima exactly.',
            'scope': 'Finite schedule-mass checks. Signed amplitude routing and the general circuit optimum are established in the packet proofs.'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
