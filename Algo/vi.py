from typing import List, Dict, Tuple, Iterator
from Algo.mdp import MDP


class VI(MDP):
    def __init__(self, graph):
        super().__init__(graph, "VI")

    # V(s) = max_a [sum_s' (prob(s,a,s')*V(s')] + R(s)
    def vi(self, target, limit=None, delta=0.0001):
        self._init_table(len(target))
        for pos in self._table.keys():
            self._table[pos].append(-1)
        self._table[target] = [1]
        iter_limit = limit if limit else 1000
        for i in range(iter_limit):
            for pos in self._table.keys():
                steps = []
                if pos == target:
                    continue
                for next_step in self._get_actions(pos):
                    steps.append(self._q_value(pos, next_step))
                self._table[pos] = [self._table[pos][-1], max(steps)]  # reward of step
            if not limit and self._check_delta(delta):
                break
        return -1 if i == iter_limit - 1 else i
