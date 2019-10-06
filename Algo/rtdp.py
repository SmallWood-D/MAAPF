import random
import itertools
from typing import List, Dict, Tuple, Iterator
from Algo.dijkstra import dijkstra


class RTDP:
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
        moves = map(lambda action: RTDP.valid_action(pos, action), actions)
        return [move for move in moves if move is not None]

    def _greedy_action(self, state):
        actions = self._get_actions(state)
        min_action = [actions[0], self._q_value(state, actions[0])]
        actions.pop(0)
        for next_step in actions:
            val = self._q_value(state, next_step)
            if val > min_action[1]:
                min_action[0] = next_step
                min_action[1] = val
        return min_action[0]

    def _next_state(self, state, action):
        return action

    def _q_value(self, state, next_step):
        calc = []
        sink_reward = -100
        for c, m in zip(state, next_step):
            if c != m:
                calc.append(
                    ((1 - self._graph.prob[m]) * self._table[next_step][-1]) + (self._graph.prob[m] * sink_reward))

        return -5 + sum(calc)

    def _trial(self, start, target):
        curr_state = start
        while curr_state != target:
            action = self._greedy_action(curr_state)
            self.table[curr_state].append(self._q_value(curr_state, action))
            curr_state = self._next_state(curr_state, action)

    def rtdp(self, start, target, limit=1000, delta=0.0001):
        self._init_table(len(target))
        dijkstra_vals = [dijkstra(self._graph, pos) for pos in target]
        for state in self._table:
            h_state = 0
            for pos, dijkstra_val in zip(state, dijkstra_vals):
                assert pos in dijkstra_val
                h_state += dijkstra_val[pos]
            self._table[state].append(h_state)
        for i in range(limit):
            self._trial(start, target)

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
    def rtdp_policy(self, target):
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
            x = random.choices(self._policy[path[-1]])[0]
            print(x)
            path.append(x)

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
