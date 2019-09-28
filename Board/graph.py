from typing import List, Dict
import csv
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


def print_result_csv(graph, vi, file_name, ID, limit, num_agents, prob_range, exp_utility, vi_time, quality, board):
    with open(file_name, 'w', newline='') as result_fd:
        writer = csv.writer(result_fd)
        writer.writerow(["position", "values"])
        for pos, v in vi.table.items():
            row = [pos]
            row.extend(v)
            writer.writerow(row)
        print(f"time, {vi_time}", file=result_fd)
        print(f"quality,  {quality}%", file=result_fd)
        for row in board:
            print(", ".join([p if p == '#' else str(graph.prob[p]) for p in row]), file=result_fd)
