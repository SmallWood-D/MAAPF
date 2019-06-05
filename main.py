# from MAAPFBoard.Graph import board
# from MAAPFBoard.A_star import MAAPFAlgorithms
from MAAPFBoard.Graph import all_graph

if __name__ == '__main__':
    x = all_graph.build_states([(1,0), (1,2)], 3,[(0,1),(1,2)])
