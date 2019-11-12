import time
from Board.board import gen_board, read_board
from Board.graph import Graph
from Algo.vi import VI
from Algo.rtdp import RTDP
from expres import print_result_json, collect_res_csv, evaluate_policy, print_heat_table
import Algo.dijkstra as dijkstra


def tests_a(start, target, prob_inter, board_size, test_num, suffix, heu=dijkstra.pron_w):
    for i in range(test_num):
        local_time = time.localtime()
        board_id = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        board, prob = gen_board(*board_size, *prob_inter)

        local_time = time.localtime()
        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        mdp = Graph(board, prob)
        vi_g = VI(mdp)
        print("VI")
        start_t = time.time()
        iter_num = vi_g.vi(target)
        path = vi_g.calc_policy(start, target)
        end_t = time.time()
        vi_time = end_t - start_t
        quality = evaluate_policy(mdp, vi_g, start, target, 1000)
        print_result_json(mdp, vi_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
                          board, board_id, suffix)

        local_time = time.localtime()
        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        mdp = Graph(board, prob)
        rtdp_g = RTDP(mdp)
        print("RTDP")
        start_t = time.time()
        try:
            iter_num = rtdp_g.rtdp(start, target, delta_limit=10, heuristic=heu)
        except Exception as e:
            print(e)
        end_t = time.time()
        vi_time = end_t - start_t
        try:
            path = rtdp_g.calc_policy(start, target)
        except Exception as e:
            print(e)
        else:
            quality = evaluate_policy(mdp, rtdp_g, start, target, 1000)
            print_result_json(mdp, rtdp_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
                              board, board_id, suffix, heuristic="dijkstra_probability")

    local_time = time.localtime()
    collect_res_csv(f"results_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}_{suffix}.csv", suffix)


def tests_a(board_file, start, target, prob_inter, test_num, suffix, heu=dijkstra.pron_w):
    local_time = time.localtime()
    board_id = f"{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
    board, prob = read_board(board_file)

    for i in range(test_num):
        local_time = time.localtime()
        # ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        # mdp = Graph(board, prob)
        # vi_g = VI(mdp)
        # print("VI")
        # start_t = time.time()
        # iter_num = vi_g.vi(target)
        # end_t = time.time()
        # vi_time = end_t - start_t
        # quality = evaluate_policy(mdp, vi_g, start, target, 1000)
        # print_result_json(mdp, vi_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
        #                   board, board_id, suffix)

        local_time = time.localtime()
        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}_prob"
        mdp = Graph(board, prob)
        rtdp_g = RTDP(mdp)
        print("RTDP")
        start_t = time.time()
        try:
            iter_num = rtdp_g.rtdp(start, target, delta_limit=10, heuristic=dijkstra.pron_w)
        except Exception as e:
            print(e)
        end_t = time.time()
        vi_time = end_t - start_t

        quality = evaluate_policy(mdp, rtdp_g, start, target, 1000)
        print_result_json(mdp, rtdp_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
                          board, board_id, suffix, heuristic="dijkstra_probability")
        print_heat_table(board, prob, rtdp_g.visit_table, suffix, rtdp_g.algo_name, ID, start, target)

        local_time = time.localtime()
        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}_len"
        mdp = Graph(board, prob)
        rtdp_g = RTDP(mdp)
        print("RTDP")
        start_t = time.time()
        try:
            iter_num = rtdp_g.rtdp(start, target, delta_limit=10, heuristic=dijkstra.dis_w)
        except Exception as e:
            print(e)
        end_t = time.time()
        vi_time = end_t - start_t

        quality = evaluate_policy(mdp, rtdp_g, start, target, 1000)
        print_result_json(mdp, rtdp_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
                          board, board_id, suffix, heuristic="dijkstra_distance")
        print_heat_table(board, prob, rtdp_g.visit_table, suffix, rtdp_g.algo_name, ID, start, target)

    local_time = time.localtime()
    collect_res_csv(f"results_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}_{suffix}.csv", suffix)


def tests_c(start, target, prob_inter, board_size, test_num, suffix, heu=dijkstra.pron_w):
    for i in range(test_num):
        local_time = time.localtime()
        board_id = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        board, prob = gen_board(*board_size, *prob_inter)

        local_time = time.localtime()
        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        mdp = Graph(board, prob)
        rtdp_g = RTDP(mdp)
        print("RTDP")
        start_t = time.time()
        try:
            iter_num = rtdp_g.rtdp(start, target, delta_limit=10, heuristic=dijkstra.dis_w)
        except Exception as e:
            print(e)
        end_t = time.time()
        print(iter_num)
        vi_time = end_t - start_t
        # try:
            # rtdp_g.calc_policy(start, target)
        # except Exception as e:
        #     print(e)
        # else:
        quality = evaluate_policy(mdp, rtdp_g, start, target, 1000)
        print_result_json(mdp, rtdp_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
                              board, board_id, suffix, heuristic="dijkstra_len")
        print_heat_table(board, prob, rtdp_g.visit_table, suffix, rtdp_g.algo_name, ID, start, target)


        local_time = time.localtime()
        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}_len"
        mdp = Graph(board, prob)
        rtdp_g = RTDP(mdp)
        print("RTDP")
        start_t = time.time()
        try:
            iter_num = rtdp_g.rtdp(start, target, delta_limit=10, heuristic=dijkstra.pron_w)
        except Exception as e:
            print(e)
        print(iter_num)
        end_t = time.time()
        vi_time = end_t - start_t
        # try:
        #     rtdp_g.calc_policy(start, target)
        # except Exception as e:
        #     print(e)
        # else:
        quality = evaluate_policy(mdp, rtdp_g, start, target, 1000)
        print_result_json(mdp, rtdp_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
                              board, board_id, suffix, heuristic="dijkstra_probability")
        print_heat_table(board, prob, rtdp_g.visit_table, suffix, rtdp_g.algo_name, ID, start, target)

    local_time = time.localtime()
    collect_res_csv(f"results_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}_{suffix}.csv", suffix)


def tests_b(start, target, prob_inter, board_size, test_num, trial_limit, suffix):
    for i in range(test_num):
        local_time = time.localtime()
        board_id = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        board, prob = gen_board(*board_size, *prob_inter)

        local_time = time.localtime()
        ID = f"{i}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
        mdp = Graph(board, prob)
        rtdp_g = RTDP(mdp)
        print("RTDP")
        start_t = time.time()
        iter_num = "time_limit"
        try:
            iter_num = rtdp_g.rtdp(start, target, delta_limit=10, limit=trial_limit)
        except Exception as e:
            print(e)
        end_t = time.time()
        vi_time = end_t - start_t
        try:
            rtdp_g.calc_policy(start, target)
        except Exception as e:
            print(e)
        else:
            quality = evaluate_policy(mdp, rtdp_g, start, target, 1000)
            print_result_json(mdp, rtdp_g, ID, iter_num, prob_inter, start, target, vi_time, quality * 100,
                                  board, board_id, suffix, heuristic="dijkstra_probability")

    local_time = time.localtime()
    collect_res_csv(f"results_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}_{suffix}.csv", suffix)


if __name__ == '__main__':
    g_start = ("1|1", "4|2")
    g_target = ("4|4", "3|4")
    g_prob_inter = (0.3, 0.6)
    g_board_size = (10, 10)
    g_test_num = 30

    print("10x10x2")
    g_prob_inter = (0.3, 0.6)
    # tests_c(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "10x10x2")

    g_start = ("1|1", "2|1")
    g_target = ("1|2", "2|2")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_try", g_start, g_target, g_prob_inter, g_test_num, "board_try")

    g_start = ("1|1", "1|2")
    g_target = ("3|0", "3|3")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_1", g_start, g_target, g_prob_inter, g_test_num, "board_1")

    g_start = ("1|1", "1|3")
    g_target = ("4|0", "4|3")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_2", g_start, g_target, g_prob_inter, g_test_num, "board_2")

    g_start = ("1|1", "1|3")
    g_target = ("4|3", "4|1")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_3", g_start, g_target, g_prob_inter, g_test_num, "board_3")

    g_start = ("0|0", "0|4")
    g_target = ("4|0", "4|3")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_4", g_start, g_target, g_prob_inter, g_test_num, "board_4")

    g_start = ("1|1", "1|3")
    g_target = ("5|0", "5|3")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_5", g_start, g_target, g_prob_inter, g_test_num, "board_5")

    g_start = ("1|1", "1|8")
    g_target = ("6|5", "6|9")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_6", g_start, g_target, g_prob_inter, g_test_num, "board_6")

    g_start = ("1|1", "1|8")
    g_target = ("8|1", "6|5")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_7", g_start, g_target, g_prob_inter, g_test_num, "board_7")

    g_start = ("1|1", "1|8", "8|4")
    g_target = ("6|5", "8|1", "8|8")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_8", g_start, g_target, g_prob_inter, g_test_num, "board_8")

    g_start = ("1|1", "1|8", "2|5")
    g_target = ("6|5", "8|1", "8|3")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_9", g_start, g_target, g_prob_inter, g_test_num, "board_9")

    g_start = ("1|1", "1|4")
    g_target = ("4|1", "4|4")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_10", g_start, g_target, g_prob_inter, g_test_num, "board_10")

    g_start = ("1|1", "1|4")
    g_target = ("4|1", "4|4")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_11", g_start, g_target, g_prob_inter, g_test_num, "board_11")

    g_start = ("1|1", "1|4")
    g_target = ("4|1", "4|4")
    g_prob_inter = (0, 1)
    g_test_num = 30

    tests_a("resources\\boards\\board_12", g_start, g_target, g_prob_inter, g_test_num, "board_12")


    # print("3x3x2")
    # g_prob_inter = (0.3, 0.6)
    # # tests_a(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "3x3x2")
    #
    # g_start = ("1|1", "2|1")
    # g_target = ("4|2", "3|4")
    # g_prob_inter = (0.3, 0.6)
    # g_board_size = (5, 5)
    # g_test_num = 5
    #
    # print("5x5x2")
    # g_prob_inter = (0.3, 0.6)
    # # tests_c(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "5x5x2")
    #
    # g_start = ("0|0", "0|1", "0|2")
    # g_target = ("2|0", "2|1", "2|2")
    # g_prob_inter = (0.1, 0.3)
    # g_board_size = (3, 3)
    # g_test_num = 5
    #
    # print("3x3x3")
    # g_prob_inter = (0.3, 0.6)
    # tests_c(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "3x3x3")
    #
    # g_start = ("1|1", "2|1", "3|3")
    # g_target = ("4|4", "3|4", "0|4")
    # g_prob_inter = (0.1, 0.3)
    # g_board_size = (5, 5)
    # g_test_num = 5
    #
    # print("5x5x3")
    # g_prob_inter = (0.7, 0.9)
    # tests_c(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "5x5x3")
    #
    #
    # g_start = ("1|1", "4|2")
    # g_target = ("4|4", "3|4")
    # g_prob_inter = (0.3, 0.6)
    # g_board_size = (6, 6)
    # g_test_num = 5
    #
    # print("6x6x2")
    # g_prob_inter = (0.3, 0.6)
    # tests_c(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "6x6x2")
    #
    #
    # g_start = ("1|1", "4|2")
    # g_target = ("4|4", "3|4")
    # g_prob_inter = (0.3, 0.6)
    # g_board_size = (10, 10)
    # g_test_num = 5
    #
    # print("10x10x2")
    # g_prob_inter = (0.3, 0.6)
    # tests_c(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "10x10x2")
    #
    # g_start = ("1|1", "4|2", "3|3", "0|3")
    # g_target = ("4|4", "3|4", "0|4", "2|1")
    # g_prob_inter = (0.3, 0.6)
    # g_board_size = (5, 5)
    # g_test_num = 5
    #
    # print("5x5x4")
    # g_prob_inter = (0.3, 0.6)
    # tests_c(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "5x5x4")
