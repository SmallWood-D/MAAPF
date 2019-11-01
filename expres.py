import csv
import json
import glob
import os
import random
from math import log
from Algo.dijkstra import calculate_optimal_probability


def calculate_avg_optimal_probability(graph, start):
    max_len = len(graph.prob.keys())
    dist = {p: max_len for p in graph.graph}
    q = set(graph.graph.keys())
    dist[start] = 0
    while q:
        u = min(q, key=lambda p: dist[p])
        q.remove(u)
        for p in graph.graph[u]:
            if p and p in q:
                alt = dist[u] + (-1 * log(1 - graph.prob[p]))
                if alt < dist[p]:
                    dist[p] = alt
    return dist


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


def print_result_json(graph, exp_res, id, limit, prob_range, start, target, vi_time, quality, board, board_id, suffix,
                      heuristic="NA"):
    exp_id = f"{exp_res.algo_name}_{id}"
    result = dict()
    # result['VI_table'] = vi.table
    result["time"] = vi_time
    result["start"] = str(start)
    result["target"] = str(target)
    result["quality"] = quality
    result["probability"] = graph.prob
    result["agents"] = len(next(iter(exp_res.table.keys())))
    result["ID"] = exp_id
    result["algo"] = exp_res.algo_name
    result["expected utility"] = exp_res.table[start][-1]
    result["min range"] = prob_range[0]
    result["max range"] = prob_range[1]
    result["board size"] = f"{len(board[0]) - 2} X {len(board) - 2}"
    result["number of iteration"] = limit if limit != -1 else "-"
    result["board"] = board
    result["board_id"] = board_id
    result["heuristic"] = heuristic

    opt_avg = 0
    for s, g in zip(start, target):
        opt_avg += calculate_optimal_probability(graph, s)[0][g]
        # TODO can be improved
    result["average sum prob"] = opt_avg / len(start)

    opt_avg = 0

    for i, agent in enumerate(zip(start, target)):
        optimal_probability = calculate_optimal_probability(graph, agent[1])[1][agent[0]]
        result[f"prob_opt_{i}"] = optimal_probability
        opt_avg += optimal_probability
    result["average optimal"] = opt_avg / len(start)
    if not os.path.exists(f"results{os.path.sep}{suffix}"):
        os.makedirs(f"results{os.path.sep}{suffix}")
    with open(f"results{os.path.sep}{suffix}{os.path.sep}{exp_id}.json", 'w') as result_fd:
        json.dump(result, result_fd, sort_keys=True, indent=4)


def collect_res_csv(file_name, suffix):
    columns_titles = {"ID": "experiments ID",
                      "time": "algorithm run time",
                      "quality": "the percentage of success travers of the path - no agent got destory",
                      "agents": "number of agents",
                      "expected utility": "the value of the start state.",  # TODO
                      "min range": "probability minimum range",
                      "max range": "probability maximum range",
                      "board size": "board size or board shape",
                      "number of iteration": "number of iteration the until the algorithm finsih",
                      "average sum prob": "average of the sums of -log(portability) for all agents",
                      "average optimal": "average of the probability of the shortest path for all agents",
                      "algo": "name of the algorithm",
                      "board_id": "board id",
                      "heuristic": "name of the heuristic fucntion"}
    with open(f"results{os.path.sep}{file_name}", 'w', newline='') as result_fd:
        writer = csv.DictWriter(result_fd, fieldnames=columns_titles.keys())
        writer.writeheader()
        exp_json = glob.glob(f"results{os.path.sep}{suffix}{os.path.sep}*.json")
        for exp_f in exp_json:
            with open(exp_f, 'r') as exp_fd:
                data = json.load(exp_fd)
                filter_data = {k: data[k] for k in data if k in columns_titles}
                writer.writerow(filter_data)
        for c, i in columns_titles.items():
            print(f"{c}, {i}", file=result_fd)
