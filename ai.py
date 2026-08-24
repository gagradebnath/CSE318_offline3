import random

from board import other_player


def minimax_alpha_beta(board, depth, alpha, beta, player, heuristic_fn,last_extra_turn=False, last_captured=0):

    if depth == 0 or board.is_game_over():
        value = heuristic_fn(board, player, extra_turn=last_extra_turn, captured=last_captured)
        return value, None

    mover = board.turn
    moves = board.valid_moves(mover)
    maximizing = (mover == player)

    best_move = moves[0]
    best_value = float("-inf") if maximizing else float("inf")

    for move in moves:
        child = board.copy()
        extra_turn, captured = child.apply_move(move)

        value, _ = minimax_alpha_beta(
            child, depth - 1, alpha, beta, player, heuristic_fn,
            last_extra_turn=extra_turn, last_captured=captured,
        )

        if maximizing:
            if value > best_value or (value == best_value and random.random() < 0.5):
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        else:
            if value < best_value or (value == best_value and random.random() < 0.5):
                best_value = value
                best_move = move
            beta = min(beta, best_value)

        if beta <= alpha:
            break  

    return best_value, best_move


def choose_move(board, player, heuristic_fn, depth=5):

    _, move = minimax_alpha_beta(
        board, depth, float("-inf"), float("inf"), player, heuristic_fn
    )
    return move
