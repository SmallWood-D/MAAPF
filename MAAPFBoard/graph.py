from graphviz import Digraph


class Board:
    default_threat = 0
    default_time = 1

    def __init__(self):
        self.__edges = dict()  # Vertex id : int -> Edge object.
        self.__vertices = dict()  # vertex id : int -> Vertex object.

    @classmethod
    def build_board(cls, file):
        """Build the graph from file.
        The file supposed to contain pairs of strings separate by white spaces, each pair in a new line.
        Each pair is an edge between two vertices in the graph (s, t).
        Example: 1 2
                 2 3"""
        board = cls()
        with open(file, 'r') as board_file:
            lines = board_file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    vertices = line.split()
                    board.add_edge(vertices[0], vertices[1])
        return board

    def add_position(self, v_id, threat: float=default_threat):
        v = Board.Vertex(v_id, threat)
        self.__vertices[v_id] = v
        self.__edges[v_id] = set()
        return v

    def remove_position(self, v_id):
        if v_id in self.__vertices:
            self.__vertices.pop(v_id)
            del self.__edges[v_id]

    def add_edge(self, s_id, t_id, threat: float = default_threat, time: int = default_time):
        """Add new age to the graph.
         If one of the vertices don't exists create it first."""
        s_v = self.__vertices.get(s_id)
        t_v = self.__vertices.get(t_id)
        if not s_v:
            s_v = self.add_position(s_id, Board.default_threat)
        if not t_v:
            t_v = self.add_position(t_id, Board.default_threat)
            t_v = self.add_position(t_id, Board.default_threat)

        self.__edges[s_id].add(Board.Edge(s_id, t_id, time, threat))

    def get_vertex(self, v_id):
        vertex = None
        v = self.__vertices[v_id]
        if v:
            vertex = v, self.__edges[v_id]
        return vertex

    def get_vertices(self):
        return self.__vertices.keys()

    def print_board(self):
        for k, v in self.__vertices.items():
            edges = self.__edges[k]
            print(f'{k} -> ', end='')
            for e in edges:
                print(f'{e.target} ', end='')
            print()
        print()

    def render_board(self):
        """create picture of the graph in pdf format.
         Using graphviz and dot format.
         graphviz must be install first!."""
        dot = Digraph(comment='MAAPF board.')
        for k, v in self.__vertices.items():
            dot.node(f'{k}')
            edges= self.__edges[k]
            for e in edges:
                dot.edge(f'{k}', f'{e.target}', constraint='false')
        dot.render('test-output/maapf-board.gv', view=True)

    def get_neighbors(self, vertex):
        """return all the neighbors of the input vertex."""
        return map(lambda e: e.target, self.__edges[vertex])

    def get_edge(self, s_id: str, t_id: str):
        return next((e for e in self.__edges[s_id] if e.target == t_id), None)

    class Vertex:
        """contain the information on a Vertex in the graph."""
        def __init__(self, v_id: str, threat: float):
            self.__id = v_id
            self.__threat = threat
            assert 0 <= self.__threat <= 1

        @property
        def threat(self):
            """The possibility the robot will be destroyed on the vertex."""
            return self.__threat

        @property
        def v_id(self):
            return self.__id

        def __eq__(self, other):
            return isinstance(other, Board.Vertex) and self.__id == other.__id

        def __hash__(self):
            # use the hashcode of self.ssn since that is used
            # for equality checks as well
            return hash(self.__id)

        def __str__(self):
            return str(self.v_id)

    class Edge:
        """contain the information on a Edge in the graph weights source and target."""
        def __init__(self, s, t, time: int, threat: float):
            self.__start = s
            self.__target = t
            self.__time = time
            self.__threat = threat
            assert 0 < self.__time
            assert 0 <= self.__threat <= 1

        @property
        def start(self):
            """Source vertex."""
            return self.__start

        @property
        def target(self):
            """Target vertex."""
            return self.__target

        @property
        def threat(self):
            """The possibility the robot will be destroyed while traveling the edge."""
            return self.__threat

        @property
        def time(self):
            """time to traverse the edge."""
            return self.__time

        def __eq__(self, other):
            return (isinstance(other, Board.Edge)
                    and self.__start == other.__start
                    and self.__target == other.__target)

        def __hash__(self):
            # use the hashcode of self.ssn since that is used
            # for equality checks as well
            return hash((self.__start, self.__target))

        def __str__(self):
            return f'{self.__start} -> {self.__target}'
