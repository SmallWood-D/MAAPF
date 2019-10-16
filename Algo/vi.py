import random
import itertools
from typing import List, Dict, Tuple, Iterator


class VI:
    def __init__(self, graph):
        self._policy = {}
        self._table = {}
        self._graph = graph

    @property
    def table(self) -> Dict[str, List[float]]:
        return self._table

    @property
    def policy(self) -> Dict[Tuple[str, str], Tuple[str, str]]:
        return self._policy

    def _init_table(self, num_agents):
        """
        initialize the table to store the V values
        :return: table for VI calculation
        """
        self._table = {}
        positions = list(self._graph.graph.keys())  # all the positions on the board
        for pair in itertools.product(positions, repeat=num_agents):
            if len(pair) == len(set(pair)):
                self._table[pair] = []

    def _get_actions(self, pos: Tuple[str, str]) -> Iterator[Tuple[str, str]]:
        """
        return all the possible actions from pos.
        :param pos: the current position
        :return: iterator of all possible actions (may contain illegal actions).
        """
        passable_actions = []
        for p in pos:
            curr_actions = self._graph.graph[p]
            curr_actions.append(None)
            passable_actions.append(curr_actions)
        actions = set(itertools.product(*passable_actions))
        moves = map(lambda action: VI.valid_action(pos, action), actions)
        return [move for move in moves if move is not None]

    # V(s) = max_a [sum_s' (prob(s,a,s')*V(s')] + R(s)
    def vi(self, target, limit=None, delta=0.0001):
        self._init_table(len(target))
        for pos in self._table.keys():
            self._table[pos].append(-1)
        self._table[target] = [1]
        sink_reward = -100
        iter_limit = limit if limit else 1000
        for i in range(iter_limit):
            for pos in self._table.keys():
                steps = []
                if pos == target:
                    continue
                for next_step in self._get_actions(pos):
                    calc = []
                    for c, m in zip(pos, next_step):
                        # if c != m:
                        calc.append(((1 - self._graph.prob[m]) * self._table[next_step][-1]) + (self._graph.prob[m] * sink_reward))
                    if next_step:
                        steps.append(sum(calc))
                self._table[pos].append(max(steps) + -1)  # reward of step
            if not limit and self._check_delta(delta):
                break

    def _check_delta(self, delta: float) -> bool:
        """
        check if the latest VI iteration change is smaller then delta.
        :param delta: the maximal difference between two value iterations.
        :return: True if all the values in the table didn't change more then delta
        """
        stop = False
        for row in self.table.values():
            if len(row) > 1 and abs(row[-1] - row[-2]) > delta:
                break
        else:
            stop = True
        return stop

    # T(s) = argmax_a [sum_s' (prob(s,a,s')*V(s')] + R(s)
    def vi_policy(self, target):
        self._policy = {}
        for pos in self._table.keys():
            if pos == target:
                continue
            max_val = max([self.table[p][-1] for p in self._get_actions(pos)])
            self._policy[pos] = [p for p in self._get_actions(pos) if self.table[p][-1] == max_val]

    def policy_path(self, source, target):
        path = list()
        path.append(source)
        limit = 10 * len(self._table)
        while path[-1] != target:
            if not limit:
                raise Exception("Fail to find path")
            limit -= 1
            path.append(random.choices(self._policy[path[-1]])[0])

        return path

    @staticmethod
    def valid_action(pos: Tuple[str, str], action: Tuple[str, str]) -> bool:
        """
        check if the move from prev to curr is valid
        :param pos: previous position
        :param action: current action
        :return:True if move is valid
        """
        next_pos = tuple(a if a else p for p, a in zip(pos, action))
        valid = len(next_pos) == len(set(next_pos)) and next_pos != pos
        pos_map = {p: idx for idx, p in enumerate(pos)}
        for idx, a in enumerate(action):
            if a in pos_map and action[pos_map[a]] == pos[idx]:
                valid = False
                break
        return next_pos if valid else None



