class Agraph:
    """ The class receive size of a matrix, list of block positions and start locations of the agents.
    Then the class can build a graph with all the possibilities.
    Right now assuming movement is possible only in 2D and 4 directions."""
    def __init__(self, pos):
        self.__pos = pos
        self.__vertices = []  # vertex id : int -> Vertex object.
        self.__weight = []  # vertex id : int -> Vertex object.

    @property
    def vertices(self):
        return self.__vertices

    @property
    def pr(self):
        return self.__weight

    def add(self, v,  w=1):
        self.__vertices.append(v)
        self.__weight.append(w)

    def print_graph(self, tab=1):
        path = str(self.__pos)
        tabs = tab * '\t'
        for v in self.__vertices:
            path += '\n' + tabs + v.print_graph(tab + 1)
        return path


def gen_all_positions(l_pos, ):
    l = []
    _gen_all_positions(l_pos[:], [], l)
    return l


def _gen_all_positions(l_pos, visited, l):
    if not l_pos:
        l.append(visited)
        return

    pos = l_pos.pop(0)
    new_poss = [
        (pos[0] - 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] + 1),
        (pos[0], pos[1])
    ]
    for new_pos in new_poss:
        new_visited = visited[:]
        new_visited.append(new_pos)
        _gen_all_positions(l_pos[:], new_visited, l)


def build_states(l_pos, n, l_target):
    visited = [[] for i in l_pos]
    graph = Agraph(l_pos)
    g = _build_states_rec(l_pos, n, l_target, visited, graph)
    print(g.print_graph())
    return visited


def _build_states_rec(l_pos, n, l_target, visited, graph):
    if l_pos == l_target:
        print("asasas")
        return Agraph(l_target)

    all_poss = gen_all_positions(l_pos)
    for idx, pos in enumerate(l_pos):
        visited[idx].append(pos)

    for new_pos in all_poss:
        if check_all_positions(new_pos, n, visited):
            new_graph = Agraph(new_pos)
            new_visited = [asd[:] for asd in visited]
            graph.add(_build_states_rec(new_pos, n, l_target, new_visited, new_graph))
    return graph


def check_pos(pos, n, visited):
    return n > pos[0] >= 0 and n > pos[1] >= 0 and pos not in visited


def check_all_positions(poses, n, visited):
    valid = True
    for idx, pos in enumerate(poses):
        valid &= check_pos(pos, n, visited[idx])
    return valid
