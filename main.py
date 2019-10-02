import time
from Board.board import gen_board
from Board.graph import Graph
from Algo.vi import VI, evaluate_policy
from expres import print_result_json, collect_res_csv

if __name__ == '__main__':
    for i in range(10):
        ID = f"{i}_{time.time()}"
        board, prob = gen_board(3, 4, 0.5, 0.8)
        mdp = Graph(board, prob)
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

        print_result_json(mdp, vi_g, ID, 4, (0.5, 0.8), ("1|1", "1|2"), ("0|0", "2|3"), vi_time, quality * 100, board)

    collect_res_csv(f"results_{time.time()}.csv")
