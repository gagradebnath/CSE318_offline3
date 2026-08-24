"""
Heuristic (evaluation) functions for Mancala, as described in the assignment.

Every heuristic estimates how good the CURRENT board is for `player`.
Bigger number = better for `player`. They all reuse the same two basic
ingredients (store difference, side-stone difference) and add more terms
on top, matching heuristic-1 through heuristic-4 from the assignment PDF.
"""

from board import PITS, STORE, other_player


def store_difference(board, player):
    """(my stones in storage) - (opponent's stones in storage)."""
    opponent = other_player(player)
    return board.slots[STORE[player]] - board.slots[STORE[opponent]]


def side_difference(board, player):
    """(stones on my side's pits) - (stones on opponent's side's pits)."""
    opponent = other_player(player)
    # my_stones = sum(board.slots[p] for p in BINS[player])
    # opp_stones = sum(board.slots[p] for p in BINS[opponent])
    # return my_stones - opp_stones
    my_store = 0
    opp_store = 0
    for p in PITS[player]:
        my_store += board.slots[p]
    for p in PITS[opponent]:
        opp_store += board.slots[p]
    return my_store - opp_store

def heuristic_1(board, player, extra_turn=False, captured=0):
    """heuristic-1: just the store difference."""
    return store_difference(board, player)


def heuristic_2(board, player, extra_turn=False, captured=0, w1=1.0, w2=1.0):
    """heuristic-2: store difference + side-stone-count difference."""
    return w1 * store_difference(board, player) + w2 * side_difference(board, player)


def heuristic_3(board, player, extra_turn=False, captured=0, w1=1.0, w2=1.0, w3=1.0):
    """heuristic-3: heuristic-2 + a bonus if this move earned an extra turn."""
    score = w1 * store_difference(board, player) + w2 * side_difference(board, player)
    score += w3 * (1 if extra_turn else 0)
    return score


def heuristic_4(board, player, extra_turn=False, captured=0, w1=1.0, w2=1.0, w3=1.0, w4=1.0):
    """heuristic-4: heuristic-3 + a bonus for stones captured by this move."""
    score = w1 * store_difference(board, player) + w2 * side_difference(board, player)
    score += w3 * (1 if extra_turn else 0)
    score += w4 * captured
    return score


# Handy name -> function lookup, used by game.py and experiment.py.
ALL_HEURISTICS = {
    "heuristic_1": heuristic_1,
    "heuristic_2": heuristic_2,
    "heuristic_3": heuristic_3,
    "heuristic_4": heuristic_4,
}
