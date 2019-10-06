import csv
import json
import glob
import os
import random
from Algo.dijkstra import dijkstra


def apply(state_a, state_b, prob_table):
    death_prob = 1
    next_state = None
    for s in state_b:
        death_prob *= prob_table[s]

    if random.choices([True, False], weights=[1 - death_prob, death_prob])[0]:
        next_state = state_b
    return next_state


def evaluate_policy(graph, vi, start, goal, num_of_experiments):
    wins = 0
    loses = 0
    for i in range(num_of_experiments):
        world_state = start
        while True:
            action = random.choices(vi.policy[world_state])[0]
            world_state = apply(world_state, action, graph.prob)
            if not world_state:
                loses += 1
                break
            if world_state == goal:
                wins += 1
                break
    return wins/num_of_experiments


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


def print_result_json(graph, vi, ID, limit, prob_range, start, target, vi_time, quality, board):
    result = dict()
    # result['VI_table'] = vi.table
    result["time"] = vi_time
    result["start"] = str(start)
    result["target"] = str(target)
    result["quality"] = quality
    result["probability"] = graph.prob
    result["agents"] = len(next(iter(vi.table.keys())))
    result["ID"] = ID
    result["expected utility"] = vi.table[start][-1]
    result["min range"] = prob_range[0]
    result["max range"] = prob_range[1]
    result["board size"] = f"{len(board[0]) - 2} X {len(board) - 2}"
    result["number of iteration"] = limit if limit else -1
    result["board"] = board

    opt_avg = 0
    for s, g in zip(start, target):
        opt_avg += dijkstra(graph, s)[g]
    result["average optimal"] = opt_avg / len(start)

    with open(f"results{os.path.sep}{ID}.json", 'w') as result_fd:
        json.dump(result, result_fd, sort_keys=True, indent=4)


def collect_res_csv(file_name):
    columns_titles = ["ID", "time", "quality", "agents", "expected utility", "min range", "max range",
                      "board size", "number of iteration", "average optimal"]
    with open(f"results{os.path.sep}{file_name}", 'w', newline='') as result_fd:
        writer = csv.DictWriter(result_fd, fieldnames=columns_titles)
        writer.writeheader()
        exp_json = glob.glob(f"results{os.path.sep}*.json")
        for exp_f in exp_json:
            with open(exp_f, 'r') as exp_fd:
                data = json.load(exp_fd)
                filter_data = {k: data[k] for k in data if k in columns_titles}
                writer.writerow(filter_data)
