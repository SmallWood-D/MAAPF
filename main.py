from typing import List
from typing import Iterator
from typing import Dict
from typing import Tuple
import csv
import itertools
import time
import random
import os

EMPTY_SYM = "#"


def read_board(file_path: str) -> List[List[str]]:
    """
    read the table file and parse it to textual board
    :param file_path:
    :return: textual representation of board as list of lists
    """
    board = []
    prob = {}
    with open(file_path, 'r') as board_fd:
        lines = board_fd.readlines()
    max_row_len = 0
    for idx, line in enumerate(lines):
        line = line.rstrip(os.linesep)
        board_line = list()
        for jdx, pos in enumerate(line.split(',')):
            if pos:
                loc_sym = f"{idx}|{jdx}"
                board_line.append(loc_sym)
                prob[loc_sym] = float(pos)
            else:
                board_line.append(EMPTY_SYM)
        line_len = len(board_line)
        max_row_len = line_len if max_row_len < line_len else max_row_len
        board.append(board_line)

    board.insert(0, [EMPTY_SYM] * max_row_len)
    board.append([EMPTY_SYM] * max_row_len)
    for line in board:
        line_len = len(line)
        if max_row_len - line_len > 0:
            line.extend([EMPTY_SYM for i in range(max_row_len - line_len)])
        line.insert(0, EMPTY_SYM)
        line.append(EMPTY_SYM)
    return board, prob


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
    def vi(self, target, limit=None, delta=0.000001):
        self._init_table()
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


def apply(state_a, state_b, prob_table):
    death_prob = 1
    next_state = None
    for s in state_b:
        death_prob *= prob_table[s]

    if random.choices([True, False], weights=[1 - death_prob, death_prob])[0]:
        next_state = state_b
    return next_state


def evaluate_policy(mdp, start, goal, num_of_experiments):
    wins = 0
    loses = 0
    for i in range(num_of_experiments):
        world_state = start
        while True:
            action = random.choices(mdp.policy[world_state])[0]
            world_state = apply(world_state, action, mdp.prob)
            if not world_state:
                loses += 1
                break
            if world_state == goal:
                wins += 1
                break
    return wins/num_of_experiments

if __name__ == '__main__':
    board, prob = read_board('board')
    mdp = Graph(board, prob)
    start = time.time()
    mdp.vi(("1|1", "2|1"))
    end = time.time()
    vi_time = end - start
    print(vi_time)
    mdp.vi_policy(("1|1", "2|1"))
    quality = evaluate_policy(mdp, ("0|1", "1|0"), ("1|1", "2|1"), 1000)
    mdp.print_result_csv("a.csv", vi_time, quality * 100, board)


