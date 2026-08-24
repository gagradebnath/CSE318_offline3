
import random

from board import MancalaBoard, PLAYER_1, PLAYER_2
from ai import choose_move
from heuristics import ALL_HEURISTICS


def play_one_game(heuristic_p1, heuristic_p2, search_depth=4):

    board = MancalaBoard()
    while not board.is_game_over():
        mover = board.turn
        heuristic_fn = heuristic_p1 if mover == PLAYER_1 else heuristic_p2
        pit = choose_move(board, mover, heuristic_fn, depth=search_depth)
        board.apply_move(pit)
    return board.winner()


def play_match(name_a, heuristic_a, name_b, heuristic_b, num_games=100, search_depth=4, verbose=True):

    wins = {name_a: 0, name_b: 0}
    ties = 0

    for _ in range(num_games):
        if random.random() < 0.5:
            p1_name, p1_fn, p2_name, p2_fn = name_a, heuristic_a, name_b, heuristic_b
        else:
            p1_name, p1_fn, p2_name, p2_fn = name_b, heuristic_b, name_a, heuristic_a

        winner = play_one_game(p1_fn, p2_fn, search_depth)
        if winner == PLAYER_1:
            wins[p1_name] += 1
        elif winner == PLAYER_2:
            wins[p2_name] += 1
        else:
            ties += 1

    if verbose:
        print(f"{name_a} vs {name_b}  over {num_games} games (starting player randomized):")
        print(f"  {name_a} wins: {wins[name_a]}  ({100 * wins[name_a] / num_games:.1f}%)")
        print(f"  {name_b} wins: {wins[name_b]}  ({100 * wins[name_b] / num_games:.1f}%)")
        print(f"  ties:           {ties}  ({100 * ties / num_games:.1f}%)")

    return wins[name_a], wins[name_b], ties


def run_experiment(name_p1, name_p2, num_games=100, search_depth=4):
    """Play `num_games` games between two named heuristics and report the results."""
    heuristic_p1 = ALL_HEURISTICS[name_p1]
    heuristic_p2 = ALL_HEURISTICS[name_p2]
    return play_match(name_p1, heuristic_p1, name_p2, heuristic_p2, num_games, search_depth)


if __name__ == "__main__":
    names = list(ALL_HEURISTICS.keys())
    num_games = 50       
    search_depth = 4     

    print(f"Running every pairwise matchup, {num_games} games each, search depth {search_depth}.\n")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            run_experiment(names[i], names[j], num_games=num_games, search_depth=search_depth)
            print()
