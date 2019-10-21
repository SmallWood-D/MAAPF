from math import log


def dis_w(graph, start):
    max_len = len(graph.prob.keys())
    dist = {p: max_len for p in graph.graph}
    q = set(graph.graph.keys())
    dist[start] = 0
    while q:
        u = min(q, key=lambda p: dist[p])
        q.remove(u)
        for p in graph.graph[u]:
            if p and p in q:
                alt = dist[u] + 1
                if alt < dist[p]:
                    dist[p] = alt
    return dist


def pron_w(graph, start):
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
