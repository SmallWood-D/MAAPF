# from MAAPFBoard.Graph import board
# from MAAPFBoard.A_star import MAAPFAlgorithms
from MAAPFBoard.Graph import all_graph

def f(x):
    x.append(1)
    print(x)
if __name__ == '__main__':
    # x = all_graph.build_single__states((1, 1), 3, (0, 0))
    # print (x)
    x = all_graph.build_states([(1,1),], 5,[(1,0)])

    all_graph.build_single_states((1,1), 5,(1,0))
    # print(x)

    # print('MAAPF solution.')
    # b = board.Board.build_board('graph_input.txt')
    # b.print_board()
    #
    # h = lambda board: lambda s, t: int(t) - int(s)
    # d = lambda board: lambda s, t: board.get_edge(s, t).time
    # n = lambda board: lambda v_id: board.get_neighbors(v_id)
    # algo = MAAPFAlgorithms(h(b), n(b), d(b))
    #
    # print(algo.a_star('7', '8'))
