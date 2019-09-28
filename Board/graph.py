from typing import List, Dict
from .board import EMPTY_SYM


class Graph:
    def __init__(self, board: List[List[str]], prob: Dict[str, float]):
        """
        building an adjacency list of the board.
        :param board: the output of read_table function
        :return: dictionary with adjacency list
        """
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
    def prob(self) -> Dict[str, float]:
        return self._prob
