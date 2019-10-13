import time
from Board.board import gen_board
from Board.graph import Graph
from Algo.vi import VI
from Algo.rtdp import RTDP
from expres import print_result_json, collect_res_csv, evaluate_policy

if __name__ == '__main__':
    for i in range(10):
        local_time = time.localtime()
        board_id = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        board, prob = gen_board(3, 4, 0.1, 0.3)
        mdp = Graph(board, prob)
        vi_g = VI(mdp)
        start = time.time()
        vi_g.vi(("0|0", "2|3"))
        end = time.time()
        vi_time = end - start
        vi_g.vi_policy(("0|0", "2|3"))
        quality = evaluate_policy(mdp, vi_g, ("1|1", "1|2"), ("0|0", "2|3"), 1000)
        print_result_json(mdp, vi_g, ID, 4, (0.5, 0.8), ("1|1", "1|2"), ("0|0", "2|3"), vi_time, quality * 100,
                          board, "VI", board_id)

        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        mdp = Graph(board, prob)
        rtdp_g = RTDP(mdp)
        start = time.time()
        rtdp_g.rtdp(("1|1", "1|2"), ("0|0", "2|3"), limit=100)
        end = time.time()
        vi_time = end - start
        try:
            rtdp_g.policy_path(("1|1", "1|2"), ("0|0", "2|3"))
        except Exception as e:
            print(e)
        quality = evaluate_policy(mdp, rtdp_g, ("1|1", "1|2"), ("0|0", "2|3"), 1000)
        print_result_json(mdp, rtdp_g, ID, 4, (0.5, 0.8), ("1|1", "1|2"), ("0|0", "2|3"), vi_time, quality * 100,
                      board, "RTDP", board_id)

    local_time= time.localtime()
    collect_res_csv(f"results_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}.csv")
