"""
Minimax search with alpha-beta pruning for Mancala.

Note on Mancala's "extra turn" rule: when a move lands the last stone in the
mover's own store, the SAME player moves again. So depending on the move,
the next node in the search tree can be another maximizing node (if it was
our extra turn) or a minimizing node (opponent's turn) - we don't need to
track this by hand, we just look at board.turn after applying the move.
"""

from board import other_player


def minimax_alpha_beta(board, depth, alpha, beta, player, heuristic_fn,
                        last_extra_turn=False, last_captured=0):
    """
    Search the game tree starting from `board`.

    player       -> whose point of view we are maximizing for
    heuristic_fn -> one of heuristic_1..heuristic_4 from heuristics.py
    last_extra_turn / last_captured -> info about the move that produced
        this board, needed by heuristic_3 / heuristic_4

    Returns (best_value, best_move). best_move is None at leaf nodes.
    """
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
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)

        if beta <= alpha:
            break  # alpha-beta cut-off

    return best_value, best_move


def choose_move(board, player, heuristic_fn, depth=5):
    """Convenience wrapper: pick the best move for `player` at the given search depth."""
    _, move = minimax_alpha_beta(
        board, depth, float("-inf"), float("inf"), player, heuristic_fn
    )
    return move
