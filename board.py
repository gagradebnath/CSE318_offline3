
PLAYER_1 = 1
PLAYER_2 = 2


PITS = {
    PLAYER_1: [0, 1, 2, 3, 4, 5],
    PLAYER_2: [7, 8, 9, 10, 11, 12],
}
STORE = {
    PLAYER_1: 6,
    PLAYER_2: 13,
}


def other_player(player):

    if player == PLAYER_1:
        return PLAYER_2
    elif player == PLAYER_2:
        return PLAYER_1


class MancalaBoard:
    def __init__(self):

        self.slots = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.turn = PLAYER_1

    def copy(self):
        new_board = MancalaBoard()
        new_board.slots = self.slots[:]
        new_board.turn = self.turn
        return new_board

    def valid_moves(self, player):
        """Pit indices on `player`'s side that still have stones in them."""
        moves = []
        for pit in PITS[player]:
            if self.slots[pit] > 0:
                moves.append(pit)
        return moves
        

    def is_game_over(self):

        side1_empty = True
        for p in PITS[PLAYER_1]:
            if self.slots[p] > 0:
                side1_empty = False
                break
        side2_empty = True
        for p in PITS[PLAYER_2]:
            if self.slots[p] > 0:
                side2_empty = False
                break
        return side1_empty or side2_empty

    def _sweep_remaining_stones(self):

        for player in (PLAYER_1, PLAYER_2):
            leftover = 0
            for p in PITS[player]:
                leftover += self.slots[p]
                self.slots[p] = 0
            self.slots[STORE[player]] += leftover
            

    def winner(self):

        if not self.is_game_over():
            return None

        self._sweep_remaining_stones()
        if self.slots[STORE[PLAYER_1]] > self.slots[STORE[PLAYER_2]]:
            return PLAYER_1
        if self.slots[STORE[PLAYER_2]] > self.slots[STORE[PLAYER_1]]:
            return PLAYER_2
        return None  # tie

    def apply_move(self, pit):

        player = self.turn
        own_store = STORE[player]
        opponent_store = STORE[other_player(player)]

        stones = self.slots[pit]
        self.slots[pit] = 0

        index = pit
        while stones > 0:
            index = (index + 1) % 14
            if index == opponent_store:
                continue 
            self.slots[index] += 1
            stones -= 1

        last_index = index
        extra_turn = (last_index == own_store)

        stones_captured = 0

        if last_index in PITS[player] and self.slots[last_index] == 1:
            opposite_index = 12 - last_index
            if self.slots[opposite_index] > 0:
                stones_captured = self.slots[opposite_index] + 1
                self.slots[own_store] += stones_captured
                self.slots[opposite_index] = 0
                self.slots[last_index] = 0

        if self.is_game_over():
            self._sweep_remaining_stones()

        self.turn = player if extra_turn else other_player(player)

        return extra_turn, stones_captured

    def print_board(self):

        p2 = [self.slots[i] for i in reversed(PITS[PLAYER_2])]
        p1 = [self.slots[i] for i in PITS[PLAYER_1]]

        print()
        print("           +----+----+----+----+----+----+")
        print(" P2        |", end=" ")

        for stones in p2:
            print(f"{stones:2} |", end=" ")

        print()
        print("           |    |____|____|____|____|    |")
        print(f"P2 Store   | {self.slots[STORE[PLAYER_2]]:2} |"+"___________________" +
            f"| {self.slots[STORE[PLAYER_1]]:2} |  P1 Store")
        print("           |    |    |    |    |    |    |")

        print(" P1        |", end=" ")

        for stones in p1:
            print(f"{stones:2} |", end=" ")

        print()
        print("           +----+----+----+----+----+----+")
        print()


if __name__ == "__main__":
    b = MancalaBoard()
    b.print_board()

    print("\nPlayer 1 plays pit 2 (has 4 stones -> lands in pits 3,4,5,store) -> extra turn")
    extra, captured = b.apply_move(2)
    print("extra_turn:", extra, "captured:", captured, "turn is now:", b.turn)
    b.print_board()

    print("\nPlayer 1 plays pit 0 (1 stone -> lands in pit 1, not empty, no capture)")
    extra, captured = b.apply_move(0)
    print("extra_turn:", extra, "captured:", captured, "turn is now:", b.turn)
    b.print_board()
