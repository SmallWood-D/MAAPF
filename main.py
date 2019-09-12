import itertools
import random
import os

EMPTY_SYM = "#"

def read_table(fd):
    board = []
    with open(fd, 'r') as board_fd:
        lines = board_fd.readlines()
    max = 0
    for line in lines:
        line = line.rstrip(os.linesep)
        line = line.replace(" ", EMPTY_SYM)
        line_len = len(line)
        max = line_len if max < line_len else max
        board.append(list(line))

    board.insert(0, [EMPTY_SYM] * max)
    board.append([EMPTY_SYM] * max)
    for line in board:
        line_len = len(line)
        if max - line_len > 0:
            line.extend(list(EMPTY_SYM * (max - line_len)))
        line.insert(0, EMPTY_SYM)
        line.append(EMPTY_SYM)
    return board

def read_prob(fd):
    prob = {}
    with open(fd, 'r') as board_fd:
        lines = board_fd.readlines()
    for line in lines:
        line = line.strip()
        val = line.split()
        prob[val[0]] = float(val[1])
    return prob



def build_graph(board):
    row = len(board)
    col = len(board[0])
    graph = {}
    for i in range(row):
        for j in range(col):
            if  board[i][j] == EMPTY_SYM:
                continue
            graph[board[i][j]] = [None if board[i][j - 1] == EMPTY_SYM else board[i][j - 1],
                                  None if board[i + 1][j] == EMPTY_SYM else board[i+1][j],
                                  None if board[i][j + 1] == EMPTY_SYM else board[i][j + 1],
                                  None if board[i - 1][j] == EMPTY_SYM else board[i - 1][j]]
    return graph


def build_table(my_list):
    table = {}
    for pair in itertools.product(my_list, repeat=2):
        if len(pair) == len(set(pair)):
            table[pair] = []
    return table


def get_actions(graph, pos):
    passable_actions = []
    for p in pos:
        curr_actions = graph[p]
        curr_actions.append(None)
        passable_actions.append(curr_actions)

    actions = set(itertools.product(*passable_actions))
    return filter(lambda x : len(x) == len(set(x)), actions)

# V(s) = max_a [sum_s' (prob(s,a,s')*V(s')] + R(s)
def vi(graph, prob, target):
    table = build_table(list(graph.keys()))
    for pos in table.keys():
        table[pos].append(-1)
    table[target] = [1]
    table['sink'] = -100
    for t in table.items():
        print(t)
    print(graph)
    for i in range(1):
        for pos in table.keys():
            if pos == 'sink' or pos == target:
                continue
            for action in get_actions(graph, pos):
                pass
                # steps = [for pos in action]
            table[pos].append(max(steps) + -1)  # reward of step


def rtdp(graph, c, p, t):
    value_dict = {s: 0 for s in graph.keys()}
    for s in graph:
        while s != t:
            value_dict[s] = c(s) + min([p(s,s_2) * value_dict[s_2] for s_2 in graph[s]])
            s = random.sample(set(graph[s]), 1)[0]

    return value_dict


if __name__ == '__main__':
    prob = read_prob('prob')
    graph = build_graph(read_table('board'))
    assert graph.keys() == prob.keys(), "the probability and board file doesn't match"
    # vi(graph, prob, ("A","D"))
    print(list(get_actions(graph, ("A","C"))))

