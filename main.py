from MAAPFBoard import graph
from MAAPFBoard.A_star import MAAPFAlgorithms

if __name__ == '__main__':
    print('MAAPF solution.')
    b = graph.Board.build_board('graph_input.txt')
    b.print_board()

    h = lambda board: lambda s, t: int(t) - int(s)
    d = lambda board: lambda s, t: board.get_edge(s, t).time
    n = lambda board: lambda v_id: board.get_neighbors(v_id)
    algo = MAAPFAlgorithms(h(b), n(b), d(b))

    print(algo.a_star('7', '8'))
