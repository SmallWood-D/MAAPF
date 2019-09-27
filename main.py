from Board.board import read_board
from Board.board import gen_board
from Board.graph import Graph
import time
import random


EMPTY_SYM = "#"



def apply(state_a, state_b, prob_table):
    death_prob = 1
    next_state = None
    for s in state_b:
        death_prob *= prob_table[s]

    if random.choices([True, False], weights=[1 - death_prob, death_prob])[0]:
        next_state = state_b
    return next_state


def evaluate_policy(mdp, start, goal, num_of_experiments):
    wins = 0
    loses = 0
    for i in range(num_of_experiments):
        world_state = start
        while True:
            action = random.choices(mdp.policy[world_state])[0]
            world_state = apply(world_state, action, mdp.prob)
            if not world_state:
                loses += 1
                break
            if world_state == goal:
                wins += 1
                break
    return wins/num_of_experiments

if __name__ == '__main__':
    board, prob = read_board('board_try')
    mdp = Graph(board, prob)
    mdp.dijkstra("1|1")

    # print(mdp.graph)
    # start = time.time()
    # mdp.vi(("0|0", "2|3"))
    # end = time.time()
    # vi_time = end - start
    # for t,v in mdp.table.items():
    #     print(t,v)
    # print(vi_time)
    # mdp.vi_policy(("0|0", "2|3"))
    # print(mdp.policy_path(("1|1", "1|2"), ("0|0", "2|3")))
    # for m, v in mdp.policy.items():
    #     print(m, v)
    # quality = evaluate_policy(mdp, ("1|1", "1|2"), ("0|0", "2|3"), 1000)
    # mdp.print_result_csv("a.csv", vi_time, quality * 100, board)
    print(gen_board(2,3, 0, 1))

