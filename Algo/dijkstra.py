from math import log


def h_len(graph, start, target):
    dist_table, path = h_dijkstra(graph, start, target, lambda x, y: 1, None)
    return -1 * (len(path) -1)


def h_prob(graph, start, target):
    dist_table, path = h_dijkstra(graph, start, target, lambda g, p: -1 * log(g.prob[p]), None)
    h_val = 0
    for p in path:
        h_val += -1 * log(graph.prob[p])
    return h_val


def h_reward_len(graph, start, target):
    dist_table, path = h_dijkstra(graph, start, target, lambda x, y: 1, None)
    h_val = 30
    h_val += -1 * (len(path) - 1)
    return h_val


def h_reward_prob(graph, start, target):
    dist_table, path = h_dijkstra(graph, start, target, lambda g, p: -1 * log(g.prob[p]), None)
    live = 1
    death = 1
    for p in path:
        live *= (1 - graph.prob[p])
        death *= graph.prob[p]
    h_val = live * 30 + death * -100
    return h_val


def h_dijkstra(graph, start, target, weghit_func, h_func):
    max_len = len(graph.prob.keys())
    dist = {p: max_len for p in graph.graph}
    q = set()
    q.add((start, None))
    qd = set()
    dist[start] = 0
    path = {}
    while q:
        u, prev_u = min(q, key=lambda p: dist[p[0]])
        if prev_u:
            path[u] = prev_u
        if u == target:
            break
        q.remove((u, prev_u))
        qd.add(u)
        for p in graph.graph[u]:
            if p and p not in qd:
                q.add((p, u))
                alt = dist[u] + weghit_func(graph, p)
                if alt < dist[p]:
                    dist[p] = alt
    ret_path = [target]
    while ret_path[-1] != start:
        ret_path.append(path[ret_path[-1]])
    ret_path.reverse()
    return dist, ret_path


def calculate_optimal_probability(graph, target):
    max_len = len(graph.prob.keys())
    dist = {p: max_len for p in graph.graph}
    prob = {p: max_len for p in graph.graph}
    q = set(graph.graph.keys())
    dist[target] = 0
    prob[target] = 1
    while q:
        u = min(q, key=lambda p: dist[p])
        q.remove(u)
        for p in graph.graph[u]:
            if p and p in q:
                alt = dist[u] + (-1 * log(1 - graph.prob[p]))
                if alt < dist[p]:
                    dist[p] = alt
                    prob[p] = prob[u] * graph.prob[p]
    return dist, prob
