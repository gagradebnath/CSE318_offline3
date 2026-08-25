

import argparse
from functools import partial

from board import MancalaBoard, PLAYER_1, PLAYER_2, other_player
from ai import choose_move
from heuristics import ALL_HEURISTICS

WEIGHT_COUNTS = {
    "heuristic_1": 0,
    "heuristic_2": 2,
    "heuristic_3": 3,
    "heuristic_4": 4,
}


def ask_yes_no(question):
    answer = input(question + " (y/n): ").strip().lower()
    return answer.startswith("y")


def pick_heuristic(prompt):
    
    names = list(ALL_HEURISTICS.keys())
    print(prompt)
    for i, name in enumerate(names, start=1):
        print(f"  {i}) {name}")
    choice = int(input("Choose a number: ").strip())
    return names[choice - 1]


def apply_weights(heuristic_name, weights_arg):
    
    heuristic_fn = ALL_HEURISTICS[heuristic_name]
    count = WEIGHT_COUNTS[heuristic_name]
    if count == 0:
        return heuristic_fn

    if weights_arg is not None:
        values = [float(v) for v in weights_arg.split(",")]
        if len(values) != count:
            raise ValueError(
                f"{heuristic_name} needs {count} weights, got {len(values)}: {weights_arg}"
            )
    else:
        raw = input(
            f"Enter {count} weights for {heuristic_name}, comma-separated "
            f"(blank = default 1.0 each): "
        ).strip()
        if raw:
            values = [float(v) for v in raw.split(",")]
            if len(values) != count:
                raise ValueError(f"{heuristic_name} needs {count} weights, got {len(values)}")
        else:
            values = [1.0] * count

    weight_kwargs = {f"w{i + 1}": v for i, v in enumerate(values)}
    return partial(heuristic_fn, **weight_kwargs)


def human_turn(board):
    valid = board.valid_moves(board.turn)
    print(f"Your valid pits: {valid}")
    while True:
        try:
            pit = int(input("Pick a pit index to play: ").strip())
        except ValueError:
            print("Please type a number.")
            continue
        if pit in valid:
            return pit
        print("That pit isn't a legal move, try again.")


def play_game(player1_is_human, heuristic_p1, heuristic_p2, search_depth=5):
    board = MancalaBoard()
    board.print_board()
    move_history = []

    while not board.is_game_over():
        mover = board.turn
        print(f"\n--- Player {mover}'s turn ---")
        is_ai = not (mover == PLAYER_1 and player1_is_human)

        if mover == PLAYER_1 and player1_is_human:
            pit = human_turn(board)
        else:
            heuristic_fn = heuristic_p1 if mover == PLAYER_1 else heuristic_p2
            pit = choose_move(board, mover, heuristic_fn, depth=search_depth)
            print(f"AI (Player {mover}) plays pit {pit}")

        extra_turn, captured = board.apply_move(pit)
        move_history.append({
            "player": mover,
            "pit": pit,
            "is_ai": is_ai,
            "captured": captured,
            "extra_turn": extra_turn,
        })
        if captured:
            print(f"Captured {captured} stones!")
        if extra_turn:
            print(f"Player {mover} earned an extra turn.")

        board.print_board()

    print("\n=== Game over ===")
    winner = board.winner()
    if winner is None:
        print("It's a tie!")
    else:
        print(f"Player {winner} wins!")

    ai_moves = [m for m in move_history if m["is_ai"]]
    print(f"\nAI moves this game ({len(ai_moves)}):")
    for i, m in enumerate(ai_moves, start=1):
        captured_note = f" (captured {m['captured']})" if m["captured"] else ""
        extra_note = " (extra turn)" if m["extra_turn"] else ""
        print(f"  {i}. Player {m['player']} -> pit {m['pit']}{captured_note}{extra_note}")

    return move_history


def parse_args():
    parser = argparse.ArgumentParser(description="Play Mancala from the console.")
    parser.add_argument("--mode", choices=["human", "ai"],
                         help="'human' = you play Player 1 against the AI; "
                              "'ai' = AI vs AI. Omit to be asked interactively.")
    parser.add_argument("--depth", type=int, help="AI search depth. Omit to be asked.")
    parser.add_argument("--p1-heuristic", choices=list(ALL_HEURISTICS.keys()),
                         help="Heuristic for Player 1 (only used in AI vs AI mode).")
    parser.add_argument("--p2-heuristic", choices=list(ALL_HEURISTICS.keys()),
                         help="Heuristic for Player 2 (the AI opponent in human mode).")
    parser.add_argument("--p1-weights", help="Comma-separated weights for Player 1's heuristic, "
                                              "e.g. 1,0.5,2")
    parser.add_argument("--p2-weights", help="Comma-separated weights for Player 2's heuristic, "
                                              "e.g. 1,1")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.mode is not None:
        human_playing = args.mode == "human"
    else:
        human_playing = ask_yes_no("Do you want to play as Player 1 against the AI?")

    if args.depth is not None:
        search_depth = args.depth
    else:
        raw_depth = input("Search depth for the AI (blank = 5): ").strip()
        search_depth = int(raw_depth) if raw_depth else 5

    if human_playing:
        print("Human (Player 1) vs AI (Player 2).")
        p2_name = args.p2_heuristic or pick_heuristic("Pick the heuristic for the AI (Player 2):")
        heuristic_p2 = apply_weights(p2_name, args.p2_weights)
        play_game(player1_is_human=True, heuristic_p1=None, heuristic_p2=heuristic_p2,
                  search_depth=search_depth)
    else:
        print("AI vs AI mode.")
        p1_name = args.p1_heuristic or pick_heuristic("Pick the heuristic for Player 1:")
        heuristic_p1 = apply_weights(p1_name, args.p1_weights)
        p2_name = args.p2_heuristic or pick_heuristic("Pick the heuristic for Player 2:")
        heuristic_p2 = apply_weights(p2_name, args.p2_weights)
        play_game(player1_is_human=False, heuristic_p1=heuristic_p1, heuristic_p2=heuristic_p2,
                  search_depth=search_depth)
