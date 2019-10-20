import itertools
from typing import List, Dict, Tuple, Iterator


class MDP:
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
        moves = map(lambda action: MDP.valid_action(pos, action), actions)
        return [move for move in moves if move is not None]

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
