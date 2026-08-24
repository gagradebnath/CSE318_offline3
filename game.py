"""
Play a game of Mancala from the console: Human vs AI, or AI vs AI.
Run with:  python game.py
"""

from board import MancalaBoard, PLAYER_1, PLAYER_2, other_player
from ai import choose_move
from heuristics import ALL_HEURISTICS


def ask_yes_no(question):
    answer = input(question + " (y/n): ").strip().lower()
    return answer.startswith("y")


def pick_heuristic(prompt):
    names = list(ALL_HEURISTICS.keys())
    print(prompt)
    for i, name in enumerate(names, start=1):
        print(f"  {i}) {name}")
    choice = int(input("Choose a number: ").strip())
    return ALL_HEURISTICS[names[choice - 1]]


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

    while not board.is_game_over():
        mover = board.turn
        print(f"\n--- Player {mover}'s turn ---")

        if mover == PLAYER_1 and player1_is_human:
            pit = human_turn(board)
        else:
            heuristic_fn = heuristic_p1 if mover == PLAYER_1 else heuristic_p2
            pit = choose_move(board, mover, heuristic_fn, depth=search_depth)
            print(f"AI (Player {mover}) plays pit {pit}")

        extra_turn, captured = board.apply_move(pit)
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


if __name__ == "__main__":
    human_playing = ask_yes_no("Do you want to play as Player 1 against the AI?")

    if human_playing:
        ai_heuristic = pick_heuristic("Pick the heuristic for the AI (Player 2):")
        play_game(player1_is_human=True, heuristic_p1=None, heuristic_p2=ai_heuristic)
    else:
        print("AI vs AI mode.")
        h1 = pick_heuristic("Pick the heuristic for Player 1:")
        h2 = pick_heuristic("Pick the heuristic for Player 2:")
        play_game(player1_is_human=False, heuristic_p1=h1, heuristic_p2=h2)
