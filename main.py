from Board.board import read_board
from Board.board import gen_board
from Board.graph import Graph
from Board.graph import print_result_csv
from Algo.dijkstra import dijkstra
from Algo.vi import VI
from Algo.vi import evaluate_policy
import time

if __name__ == '__main__':
    ID = "sad"
    board, prob = gen_board(3, 4, 0.5, 0.8)
    mdp = Graph(board, prob)
    dijkstra(mdp, "1|1")
    vi_g = VI(mdp)
    start = time.time()
    vi_g.vi(("0|0", "2|3"), limit=4)
    end = time.time()
    vi_time = end - start
    for t,v in vi_g.table.items():
        print(t,v)
    print(vi_time)
    vi_g.vi_policy(("0|0", "2|3"))
    print(vi_g.policy_path(("1|1", "1|2"), ("0|0", "2|3")))
    for m, v in vi_g.policy.items():
        print(m, v)
    quality = evaluate_policy(mdp, vi_g, ("1|1", "1|2"), ("0|0", "2|3"), 1000)
    print_result_csv(mdp, vi_g, "a.csv", vi_time, quality * 100, board)

