from Board.board import read_board
from Board.board import gen_board
from Board.graph import Graph
from Algo.dijkstra import dijkstra
from Algo.vi import VI
from Algo.vi import evaluate_policy
import time
import csv
import json


def print_result_csv(file_name, graph, vi, ID, limit, prob_range, start, target, vi_time, quality, board):
    with open(file_name, 'w', newline='') as result_fd:
        writer = csv.writer(result_fd)
        writer.writerow(["position", "values"])
        for pos, v in vi.table.items():
            row = [pos]
            row.extend(v)
            writer.writerow(row)
        print(f"time, {vi_time}", file=result_fd)
        print(f"quality,  {quality}%", file=result_fd)
        print(f"agents, {len(next(iter(vi.table.keys())))}", file=result_fd)
        print(f"ID, {ID}", file=result_fd)
        print(f"expected utility, {vi.table[start][-1]}", file=result_fd)
        print(f"probability range, ({prob_range[0]}, {prob_range[1]})", file=result_fd)
        print(f"board size, {len(board[0]) - 2} X {len(board) - 2}", file=result_fd)
        if limit:
            print(f"number of iteration, {limit}", file=result_fd)
        else:
            print(f"number of iteration, until converge", file=result_fd)
        for row in board:
            print(", ".join([p if p == '#' else str(graph.prob[p]) for p in row]), file=result_fd)

        opt_avg = 0
        for s,g in zip(start, target):
            opt_avg += dijkstra(graph, s)[g]
        print(f"average optimal {opt_avg / len(start)}", file=result_fd)


def print_result_json(file_name, graph, vi, ID, limit, prob_range, start, target, vi_time, quality, board):
    result = dict()
    # result['VI_table'] = vi.table
    #
    result["time"] = vi_time
    result["quality"] = quality
    result["agents"] = len(next(iter(vi.table.keys())))
    result["ID"] = ID
    result["expected utility"] = vi.table[start][-1]
    result["min range"] = prob_range[0]
    result["max range"] = prob_range[1]
    result["board size"] = f"{len(board[0]) - 2} X {len(board) - 2}"
    result["number of iteration"] = -1
    if limit:
        result["number of iteration"] = limit
    result["board"] = board

    opt_avg = 0
    for s, g in zip(start, target):
        opt_avg += dijkstra(graph, s)[g]
    result["average optimal"] = opt_avg / len(start)

    with open(file_name, 'w', newline='') as result_fd:
        json.dump(result, result_fd)


if __name__ == '__main__':
    ID = "sad"
    board, prob = gen_board(3, 4, 0.5, 0.8)
    mdp = Graph(board, prob)
    vi_g = VI(mdp)
    start = time.time()
    vi_g.vi(("0|0", "2|3"), limit=4)
    end = time.time()
    vi_time = end - start
    for t,v in vi_g.table.items():
        print(t,v)
    print(vi_time)
    vi_g.vi_policy(("0|0", "2|3"))
    print(vi_g.policy_path(("1|1", "1|2"), ("0|0", "2|3")))
    for m, v in vi_g.policy.items():
        print(m, v)
    quality = evaluate_policy(mdp, vi_g, ("1|1", "1|2"), ("0|0", "2|3"), 1000)

    print_result_json(f"{ID}.json", mdp, vi_g, ID, 4, (0.5, 0.8), ("1|1", "1|2"), ("0|0", "2|3"), vi_time, quality * 100, board)

