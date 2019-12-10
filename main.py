import time
from Board.board import gen_board, read_board
from Board.graph import Graph
from Algo.rtdp import RTDP
from expres import print_result_json, collect_res_csv, evaluate_policy, print_heat_table
import Algo.dijkstra as dijkstra


def test_static_board(board_file, start, target, prob_inter, test_num, suffix):
    local_time = time.localtime()
    board_id = f"{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
    board, prob = read_board(board_file)

    print(suffix)

    for i in range(test_num):
        # run_rtdp(i, board, prob, board_id, start, target, prob_inter, test_num, suffix, dijkstra.h_len, "len")
        # run_rtdp(i, board, prob, board_id, start, target, prob_inter, test_num, suffix, dijkstra.h_prob, "prob")
        # run_rtdp(i, board, prob, board_id, start, target, prob_inter, test_num, suffix, dijkstra.h_reward_len, "reward len")
        run_rtdp(i, board, prob, board_id, start, target, prob_inter, test_num, suffix, dijkstra.h_reward_prob, "reward prob")

    local_time = time.localtime()
    collect_res_csv(f"results_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}_{suffix}.csv", suffix)


def tests_generated_boards(start, target, prob_inter, board_size, test_num, suffix):
    local_time = time.localtime()
    board_id = f"{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
    board, prob = gen_board(*board_size, *prob_inter)

    print(suffix)

    for i in range(test_num):
        run_rtdp(i, board, prob, board_id, start, target, prob_inter, test_num, suffix, dijkstra.h_len, "len")
        run_rtdp(i, board, prob, board_id, start, target, prob_inter, test_num, suffix, dijkstra.h_prob, "prob")
        run_rtdp(i, board, prob, board_id, start, target, prob_inter, test_num, suffix, dijkstra.h_reward_len, "reward len")
        run_rtdp(i, board, prob, board_id, start, target, prob_inter, test_num, suffix, dijkstra.h_reward_prob, "reward prob")

    local_time = time.localtime()
    collect_res_csv(f"results_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}_{suffix}.csv", suffix)


def run_rtdp(idx, board, prob, board_id, start, target, prob_inter, test_num, suffix, heu, heu_name):
    local_time = time.localtime()
    ID = f"{idx}_{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}"
    mdp = Graph(board, prob)
    rtdp_g = RTDP(mdp)
    print("RTDP")
    start_t = time.time()
    iter_num = 0
    try:
        iter_num = rtdp_g.rtdp(start, target, limit=2000, heuristic=heu)
    except Exception as e:
        print(e)
    end_t = time.time()
    run_time = end_t - start_t

    exp_id = f"{rtdp_g.algo_name}_{ID}_{heu_name}"
    for t in rtdp_g.table.items():
        print(t)

    quality = evaluate_policy(mdp, rtdp_g, start, target, 1000)
    print_result_json(mdp, rtdp_g, exp_id, iter_num, prob_inter, start, target, run_time, quality * 100,
                      board, board_id, suffix, heuristic=heu_name)
    print_heat_table(board, prob, rtdp_g.visit_table, suffix, exp_id + "_visit", start, target)
    print_heat_table(board, prob, rtdp_g.next_table, suffix, exp_id + "_next", start, target)


if __name__ == '__main__':
    g_start = ("1|1", "2|1")
    g_target = ("1|2", "2|2")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_try", g_start, g_target, g_prob_inter, g_test_num, "board_try")

    g_start = ("1|1", "1|2")
    g_target = ("3|0", "3|3")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_1", g_start, g_target, g_prob_inter, g_test_num, "board_1")

    g_start = ("1|1", "1|3")
    g_target = ("4|0", "4|3")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_2", g_start, g_target, g_prob_inter, g_test_num, "board_2")

    g_start = ("1|1", "1|8")
    g_target = ("6|5", "6|9")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_6", g_start, g_target, g_prob_inter, g_test_num, "board_6")

    g_start = ("1|1", "1|8")
    g_target = ("8|1", "6|5")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_7", g_start, g_target, g_prob_inter, g_test_num, "board_7")

    g_start = ("1|1", "1|8", "8|4")
    g_target = ("6|5", "8|1", "8|8")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_8", g_start, g_target, g_prob_inter, g_test_num, "board_8")

    g_start = ("1|1", "1|8", "2|5")
    g_target = ("6|5", "8|1", "8|3")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_9", g_start, g_target, g_prob_inter, g_test_num, "board_9")

    g_start = ("1|1", "1|4")
    g_target = ("4|1", "4|4")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_10", g_start, g_target, g_prob_inter, g_test_num, "board_10")

    g_start = ("1|1", "1|4")
    g_target = ("4|1", "4|4")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_11", g_start, g_target, g_prob_inter, g_test_num, "board_11")

    g_start = ("1|1", "1|4")
    g_target = ("4|1", "4|4")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_12", g_start, g_target, g_prob_inter, g_test_num, "board_12")

    g_start = ("1|1", "1|3")
    g_target = ("4|3", "4|1")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_3", g_start, g_target, g_prob_inter, g_test_num, "board_3")

    g_start = ("0|0", "0|4")
    g_target = ("4|0", "4|3")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_4", g_start, g_target, g_prob_inter, g_test_num, "board_4")

    g_start = ("0|0", "0|3")
    g_target = ("3|2", "2|3")
    g_prob_inter = (0, 1)
    g_test_num = 3

    test_static_board("resources\\boards\\board_13", g_start, g_target, g_prob_inter, g_test_num, "board_13")

    g_start = ("0|0", "0|3")
    g_target = ("2|0", "2|3")
    g_prob_inter = (0, 1)
    g_test_num = 1

    test_static_board("resources\\boards\\board_5", g_start, g_target, g_prob_inter, g_test_num, "board_5")

    g_start = ("1|1", "4|2")
    g_target = ("4|4", "3|4")
    g_prob_inter = (0.3, 0.6)
    g_board_size = (10, 10)
    g_test_num = 1

    print("10x10x2")
    g_prob_inter = (0.3, 0.6)
    tests_generated_boards(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "10x10x2")


    # print("3x3x2")
    # g_prob_inter = (0.3, 0.6)
    # # tests_a(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "3x3x2")
    #
    # g_start = ("1|1", "2|1")
    # g_target = ("4|2", "3|4")
    # g_prob_inter = (0.3, 0.6)
    # g_board_size = (5, 5)
    # g_test_num = 3
    #
    # print("5x5x2")
    # g_prob_inter = (0.3, 0.6)
    # # tests_generated_boards(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "5x5x2")
    #
    # g_start = ("0|0", "0|1", "0|2")
    # g_target = ("2|0", "2|1", "2|2")
    # g_prob_inter = (0.1, 0.3)
    # g_board_size = (3, 3)
    # g_test_num = 3
    #
    # print("3x3x3")
    # g_prob_inter = (0.3, 0.6)
    # tests_generated_boards(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "3x3x3")
    #
    # g_start = ("1|1", "2|1", "3|3")
    # g_target = ("4|4", "3|4", "0|4")
    # g_prob_inter = (0.1, 0.3)
    # g_board_size = (5, 5)
    # g_test_num = 3
    #
    # print("5x5x3")
    # g_prob_inter = (0.7, 0.9)
    # tests_generated_boards(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "5x5x3")
    #
    #
    # g_start = ("1|1", "4|2")
    # g_target = ("4|4", "3|4")
    # g_prob_inter = (0.3, 0.6)
    # g_board_size = (6, 6)
    # g_test_num = 3
    #
    # print("6x6x2")
    # g_prob_inter = (0.3, 0.6)
    # tests_generated_boards(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "6x6x2")
    #
    #
    # g_start = ("1|1", "4|2")
    # g_target = ("4|4", "3|4")
    # g_prob_inter = (0.3, 0.6)
    # g_board_size = (10, 10)
    # g_test_num = 3
    #
    # print("10x10x2")
    # g_prob_inter = (0.3, 0.6)
    # tests_generated_boards(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "10x10x2")
    #
    # g_start = ("1|1", "4|2", "3|3", "0|3")
    # g_target = ("4|4", "3|4", "0|4", "2|1")
    # g_prob_inter = (0.3, 0.6)
    # g_board_size = (5, 5)
    # g_test_num = 3
    #
    # print("5x5x4")
    # g_prob_inter = (0.3, 0.6)
    # tests_generated_boards(g_start, g_target, g_prob_inter, g_board_size, g_test_num, "5x5x4")
