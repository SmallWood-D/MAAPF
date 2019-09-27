from typing import List, Dict, Tuple, Iterator
from math import log
import itertools
import csv

EMPTY_SYM = "#"


class Graph:
    def __init__(self, board: List[List[str]], prob: Dict[str, float]):
        """
        building an adjacency list of the board.
        :param board: the output of read_table function
        :return: dictionary with adjacency list
        """
        self._table = {}
        self._policy = {}
        self._prob = prob
        row = len(board)
        col = len(board[0])
        self._graph = {}
        for i in range(row):
            for j in range(col):
                if board[i][j] == EMPTY_SYM:
                    continue
                self._graph[board[i][j]] = [None if board[i][j - 1] == EMPTY_SYM else board[i][j - 1],
                                            None if board[i + 1][j] == EMPTY_SYM else board[i+1][j],
                                            None if board[i][j + 1] == EMPTY_SYM else board[i][j + 1],
                                            None if board[i - 1][j] == EMPTY_SYM else board[i - 1][j]]

        assert self._graph.keys() == prob.keys(), "the probability and board file doesn't match"

    @property
    def graph(self) -> List[List[str]]:
        return self._graph

    @property
    def table(self) -> Dict[str, List[float]]:
        return self._table

    @property
    def policy(self) -> Dict[Tuple[str, str], Tuple[str, str]]:
        return self._policy

    @property
    def prob(self) -> Dict[str, float]:
        return self._prob

    def _init_table(self):
        """
        initialize the table to store the V values
        :return: table for VI calculation
        """
        self._table = {}
        positions = list(self._graph.keys()) # all the positions on the board
        for pair in itertools.product(positions, repeat=2):
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
            curr_actions = self._graph[p]
            curr_actions.append(None)
            passable_actions.append(curr_actions)
        actions = set(itertools.product(*passable_actions))
        moves = map(lambda action: Graph.valid_action(pos, action), actions)
        return [move for move in moves if move is not None]

    def _check_delta(self, delta: float) -> bool:
        """
        check if the latest VI iteration change is smaller then delta.
        :param delta: the maximal difference between two value iterations.
        :return: True if all the values in the table didn't change more then delta
        """
        stop = False
        for row in self._table.values():
            if len(row) > 1 and abs(row[-1] - row[-2]) > delta:
                break
        else:
            stop = True
        return stop

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
        return next_pos if valid else None

    # V(s) = max_a [sum_s' (prob(s,a,s')*V(s')] + R(s)
    def vi(self, target, limit=None, delta=0.0001):
        self._init_table()
        print(self.table)
        for pos in self._table.keys():
            self._table[pos].append(-1)
        self._table[target] = [1]
        sink_reward = -30
        iter_limit = limit if limit else 1000
        for i in range(iter_limit):
            for pos in self._table.keys():
                steps = []
                if pos == target:
                    continue
                for next_step in self._get_actions(pos):
                    calc = []
                    for c, m in zip(pos, next_step):
                        if c != m:
                            calc.append(((1 - self._prob[m]) * self._table[pos][-1]) + (self._prob[m] * sink_reward))
                    if next_step:
                        steps.append(sum(calc))
                self._table[pos].append(max(steps) + -1)  # reward of step
            if not limit and self._check_delta(delta):
                break

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

    def print_result_csv(self, file_name, vi_time, quality, board):
        with open(file_name, 'w', newline='') as result_fd:
            writer = csv.writer(result_fd)
            writer.writerow(["position", "values"])
            for pos, v in self.table.items():
                row = [pos]
                row.extend(v)
                writer.writerow(row)
            print(f"time, {vi_time}", file=result_fd)
            print(f"quality,  {quality}%", file=result_fd)
            for row in board:
                print(", ".join([p if p == '#' else str(self.prob[p]) for p in row]), file=result_fd)

    def dijkstra(self, start):
        max_len = len(self.prob.keys())
        dist = {p: max_len for p in self.graph}
        q = set(self.graph.keys())
        dist[start] = 0
        while q:
            u = min(q, key=lambda p: dist[p])
            q.remove(u)
            for p in self._graph[u]:
                if p and p in q:
                    alt = dist[u] + (-1 * log(1 - self.prob[p]))
                    if alt < dist[p]:
                        dist[p] = alt
        print( dist)
