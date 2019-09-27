from typing import List, Dict, Tuple
from random import uniform
from os import linesep

EMPTY_SYM = "#"


def read_board(file_path: str) -> Tuple[List[List[str]], Dict[str, float]]:
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
        line = line.rstrip(linesep)
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


def gen_board(n, m, pl, ph):
    board = []
    prob = {}
    for i in range(n):
        row = []
        for j in range(m):
            p = uniform(pl, ph)
            k = f"{i}|{j}"
            row.append(k)
            prob[k] = p
        board.append(row)
    return board, prob
