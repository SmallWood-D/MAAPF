def start_single(n, m, c, t):
    state = single_agent_path(n, m, c, t, [])
    return state


def graph_builder(s, paths, target):
    graph = {s:set()}
    for path in paths:
        parent = s
        for pos in path[1:]:
            x = graph.get(parent, None)
            if x == None:
                graph[parent] = set()
            x = graph.get(parent, None)
            x.add(pos)
            parent = pos
    graph[target] = set()
    return graph


def single_agent_stop(n: int, m: int, c:tuple,  path: list):
    x = c[0]
    y = c[1]
    return n <= x or x < 0 or m <= y or y < 0 or c in path


def single_agent_path(n: int, m: int, c:tuple, t: tuple, path: list):
    if c == t:
        path.append(t)
        return [path]
    elif single_agent_stop(n, m, c, path):
        return []
    path.append(c)
    return single_agent_path(n, m, (c[0] + 1, c[1]), t, path.copy()) \
           + single_agent_path(n, m, (c[0] - 1, c[1]), t, path.copy()) \
           + single_agent_path(n, m, (c[0], c[1] + 1), t, path.copy()) \
           + single_agent_path(n, m, (c[0], c[1] - 1), t, path.copy())


def reward(x, y) :
    if x == (2,2):
        return 1
    return 0


def prob(x, y):
    return 0.1


def vi(graph, r, p, gamme):
    value_dict = {s: 1 for s in graph.keys()}
    EPSILON = 0.01
    delta = 1
    while delta > EPSILON:
        prev_value_dict = value_dict.copy()
        delta = 0
        for s in graph.keys():
            route_sum = []
            for ns in graph[s]:
                route_sum.append(p(s, ns) * value_dict[ns])
            if route_sum:
                value_dict[s] = r(s, 0) + gamme * max(route_sum)
            else:
                value_dict[s] = r(s,0)
            delta = max(delta, abs(value_dict[s] - prev_value_dict[s]))
    return value_dict


action = {
    0: lambda c: c,
    1: lambda c: (c[0] - 1, c[1]),
    2: lambda c: (c[0] + 1, c[1]),
    3: lambda c: (c[0], c[1] - 1),
    4: lambda c: (c[0], c[1] + 1),
}


def inc(list, base):
    for idx, e in enumerate(list):
        step = e + 1 if (e + 1) < base else 0
        list[idx] = step
        if step:
            break


def gen_options(start, base):
    target = [0] * len(start)
    while start != target:
        yield start
        inc(start, base)


def gen_states(start_state):
    base = 5
    start_option = [0] * len(start_state)
    start_option[0] = 1
    curr_state = start_state
    for option in gen_options(start_option, base):
        yield [action[o](s) for  o, s in zip(option, curr_state)]


def multi_agent_path(n: int, m: int, c: list, t: list, path: list):
    if c == t:
        path.append(t)
        return path
    elif multi_agent_stop(n, m, c, path):
        return None
    path.append(c)
    total_path = []
    for state in gen_states(c):
        res = multi_agent_path(n, m, state, t, path.copy())
        if res:
            total_path.extend(res)
    return total_path


def multi_agent_stop(n, m, cs, path):
    is_stop = False
    seen = []
    for i, c in enumerate(cs):
        x = c[0]
        y = c[1]
        if n <= x or x < 0 or m <= y or y < 0:
            is_stop = True
        elif c in seen:
            is_stop = True
        else:
            c_path = [p[i] for p in path]
            if c in c_path:
                is_stop = True
        seen.append(c)
    return is_stop


def start_multi(n, m, c, t):
    state = multi_agent_path(n, m, c, t, [])
    res = []
    temp_res = []
    for s in state:
        temp_res.append(s)
        if s == t:
            res.append(temp_res)
            temp_res = []

    return res


if __name__ == '__main__':
    states = start_multi(3, 3, [(0, 0), (1,1)], [(2, 2), (0, 0)])
    for s in states:
        print(s)
    # states = start_single(3, 3, (0, 0), (2, 2))
    # for s in states:
    #     print(s)

    # x = graph_builder((0,0), state, (2,2))
    # for k in x.keys():
    #     print (k)
    #     print('\t',end='')
    #     print(x[k])
    #
    # print(vi(x, reward, prob, 0))


