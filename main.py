import time
from Board.board import gen_board
from Board.graph import Graph
from Algo.vi import VI
from Algo.rtdp import RTDP
from expres import print_result_json, collect_res_csv, evaluate_policy

if __name__ == '__main__':
    start = ("1|1", "1|2")
    target = ("4|3", "2|4")
    prob_inter = (0.3, 0.6)
    board_size = (5, 5)
    test_num = 10

    for i in range(test_num):
        local_time = time.localtime()
        board_id = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        board, prob = gen_board(*board_size, *prob_inter)

        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        mdp = Graph(board, prob)
        vi_g = VI(mdp)
        print("VI")
        start_t = time.time()
        iter_num = vi_g.vi(target)
        end_t = time.time()
        vi_time = end_t - start_t
        vi_g.vi_policy(target)
        quality = evaluate_policy(mdp, vi_g, start, target, 1000)
        print_result_json(mdp, vi_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
                          board, board_id)

        local_time = time.localtime()
        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        mdp = Graph(board, prob)
        rtdp_g = RTDP(mdp)
        print("RTDP")
        start_t = time.time()
        iter_num = rtdp_g.rtdp(start, target, delta_limit=20)
        end_t = time.time()
        vi_time = end_t - start_t
        try:
            rtdp_g.policy_path(start, target)
        except Exception as e:
            print(e)
        quality = evaluate_policy(mdp, rtdp_g, start, target, 1000)
        print_result_json(mdp, rtdp_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
                          board, board_id, heuristic="dijkstra_probability")

    local_time = time.localtime()
    collect_res_csv(f"results_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}.csv")
