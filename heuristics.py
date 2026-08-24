

from board import PITS, STORE, other_player


def store_difference(board, player):

    opponent = other_player(player)
    return board.slots[STORE[player]] - board.slots[STORE[opponent]]


def side_difference(board, player):

    opponent = other_player(player)

    my_store = 0
    opp_store = 0
    for p in PITS[player]:
        my_store += board.slots[p]
    for p in PITS[opponent]:
        opp_store += board.slots[p]
    return my_store - opp_store

def heuristic_1(board, player, extra_turn=False, captured=0):

    return store_difference(board, player)


def heuristic_2(board, player, extra_turn=False, captured=0, w1=5.5, w2=0.25):

    return w1 * store_difference(board, player) + w2 * side_difference(board, player)


def heuristic_3(board, player, extra_turn=False, captured=0, w1=5.5, w2=0.25, w3=0.2):

    score = w1 * store_difference(board, player) + w2 * side_difference(board, player)
    score += w3 * (1 if extra_turn else 0)
    return score


def heuristic_4(board, player, extra_turn=False, captured=0, w1=5.5, w2=0.25, w3=0.2, w4=2):

    score = w1 * store_difference(board, player) + w2 * side_difference(board, player)
    score += w3 * (1 if extra_turn else 0)
    score += w4 * captured
    return score



ALL_HEURISTICS = {
    "heuristic_1": heuristic_1,
    "heuristic_2": heuristic_2,
    "heuristic_3": heuristic_3,
    "heuristic_4": heuristic_4,
}
