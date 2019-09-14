from typing import List
from typing import Iterator
from typing import Dict
from typing import Tuple
import itertools
import os

EMPTY_SYM = "#"


def read_board(file_path: str) -> List[List[str]]:
    """
    read the table file and parse it to textual board
    :param file_path:
    :return: textual representation of board as list of lists
    """
    board = []
    with open(file_path, 'r') as board_fd:
        lines = board_fd.readlines()
    max_row_len = 0
    for line in lines:
        line = line.rstrip(os.linesep)
        line = line.replace(" ", EMPTY_SYM)
        line_len = len(line)
        max_row_len = line_len if max_row_len < line_len else max_row_len
        board.append(list(line))

    board.insert(0, [EMPTY_SYM] * max_row_len)
    board.append([EMPTY_SYM] * max_row_len)
    for line in board:
        line_len = len(line)
        if max_row_len - line_len > 0:
            line.extend(list(EMPTY_SYM * (max_row_len - line_len)))
        line.insert(0, EMPTY_SYM)
        line.append(EMPTY_SYM)
    return board


def read_prob(file_path: str) -> Dict[str, float]:
    """
    read the probabilities file
    :param file_path:
    :return: dictionary  with the probabilities for each position in the board
    """
    prob = {}
    with open(file_path, 'r') as board_fd:
        lines = board_fd.readlines()
    for line in lines:
        line = line.strip()
        val = line.split()
        prob[val[0]] = float(val[1])
    return prob


class Graph:
    def __init__(self, board: List[List[str]], prob: Dict[str, float]):
        """
        building an adjacency list of the board.
        :param board: the output of read_table function
        :return: dictionary with adjacency list
        """
        self._table = {}
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
                            # print(m, prob[m], table[pos][-1], next_step)
                            calc.append(((1 - self._prob[m]) * self._table[pos][-1]) + (self._prob[m] * sink_reward))
                    if next_step:
                        steps.append(sum(calc))
                self._table[pos].append(max(steps) + -1)  # reward of step
            if not limit and self._check_delta(delta):
                break


if __name__ == '__main__':
    prob = read_prob('prob')
    board = read_board('board')
    mdp = Graph(board, prob)
    mdp.vi(("C","E"), 6)
    ts = mdp.table
    for t in ts.items():
        print(t)

