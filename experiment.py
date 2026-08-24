"""
Run computer-vs-computer Mancala games to compare heuristics, as asked for
in the assignment ("determine win-loss ratio by running 100 games").

Run with:  python experiment.py
"""

from board import MancalaBoard, PLAYER_1, PLAYER_2
from ai import choose_move
from heuristics import ALL_HEURISTICS


def play_one_game(heuristic_p1, heuristic_p2, search_depth=4):
    """Play one full AI vs AI game. Returns PLAYER_1, PLAYER_2, or None (tie)."""
    board = MancalaBoard()
    while not board.is_game_over():
        mover = board.turn
        heuristic_fn = heuristic_p1 if mover == PLAYER_1 else heuristic_p2
        pit = choose_move(board, mover, heuristic_fn, depth=search_depth)
        board.apply_move(pit)
    return board.winner()


def run_experiment(name_p1, name_p2, num_games=100, search_depth=4):
    """Play `num_games` games between two named heuristics and report the results."""
    heuristic_p1 = ALL_HEURISTICS[name_p1]
    heuristic_p2 = ALL_HEURISTICS[name_p2]

    p1_wins = 0
    p2_wins = 0
    ties = 0

    for _ in range(num_games):
        winner = play_one_game(heuristic_p1, heuristic_p2, search_depth)
        if winner == PLAYER_1:
            p1_wins += 1
        elif winner == PLAYER_2:
            p2_wins += 1
        else:
            ties += 1

    print(f"{name_p1} (P1) vs {name_p2} (P2)  over {num_games} games:")
    print(f"  {name_p1} wins: {p1_wins}  ({100 * p1_wins / num_games:.1f}%)")
    print(f"  {name_p2} wins: {p2_wins}  ({100 * p2_wins / num_games:.1f}%)")
    print(f"  ties:           {ties}  ({100 * ties / num_games:.1f}%)")
    return p1_wins, p2_wins, ties


if __name__ == "__main__":
    names = list(ALL_HEURISTICS.keys())
    num_games = 20        # keep this modest by default since minimax search is slow;
    search_depth = 4      # raise both once you've confirmed everything works.

    print(f"Running every pairwise matchup, {num_games} games each, search depth {search_depth}.\n")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            run_experiment(names[i], names[j], num_games=num_games, search_depth=search_depth)
            print()
