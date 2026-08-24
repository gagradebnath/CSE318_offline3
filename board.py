
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
    # return PLAYER_2 if player == PLAYER_1 else PLAYER_1
    if player == PLAYER_1:
        return PLAYER_2
    elif player == PLAYER_2:
        return PLAYER_1


class MancalaBoard:
    def __init__(self):
        # 2 ta store thakbe dui jon player er and baki 5 ta pit e 4 ta kore stone thakbe initially.
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
        """The game ends as soon as one side has no stones left to play."""
        # side1_empty = all(self.slots[p] == 0 for p in PITS[PLAYER_1])
        # side2_empty = all(self.slots[p] == 0 for p in PITS[PLAYER_2])
        # return side1_empty or side2_empty
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
        """When the game ends, any stones left on a side go to that side's store."""
        # for player in (PLAYER_1, PLAYER_2):
        #     leftover = sum(self.slots[p] for p in PITS[player])
        #     for p in PITS[player]:
        #         self.slots[p] = 0
        #     self.slots[STORE[player]] += leftover

        for player in (PLAYER_1, PLAYER_2):
            leftover = 0
            for p in PITS[player]:
                leftover += self.slots[p]
                self.slots[p] = 0
            self.slots[STORE[player]] += leftover
            

    def winner(self):
        """Call only after is_game_over() is True. Returns PLAYER_1, PLAYER_2, or None (tie)."""
        if not self.is_game_over():
            return None
        # Make sure leftover stones have been counted before comparing scores.
        self._sweep_remaining_stones()
        if self.slots[STORE[PLAYER_1]] > self.slots[STORE[PLAYER_2]]:
            return PLAYER_1
        if self.slots[STORE[PLAYER_2]] > self.slots[STORE[PLAYER_1]]:
            return PLAYER_2
        return None  # tie

    def apply_move(self, pit):
        """
        Sow the stones from `pit` around the board following Mancala rules.

        Returns (extra_turn, stones_captured):
          extra_turn      -> True if the mover's last stone landed in their own store
          stones_captured -> how many stones were captured on this move (0 if none)
        """
        player = self.turn
        own_store = STORE[player]
        opponent_store = STORE[other_player(player)]

        stones = self.slots[pit]
        self.slots[pit] = 0

        index = pit
        while stones > 0:
            index = (index + 1) % 14
            if index == opponent_store:
                continue  # never drop a stone in the opponent's store
            self.slots[index] += 1
            stones -= 1

        last_index = index
        extra_turn = (last_index == own_store)

        stones_captured = 0
        # Capture rule: last stone landed in an empty pit on my own side,
        # and it had exactly 1 stone right after landing (i.e. it was empty before).
        if last_index in PITS[player] and self.slots[last_index] == 1:
            opposite_index = 12 - last_index  # 0<->12, 1<->11, ..., 5<->7
            if self.slots[opposite_index] > 0:
                stones_captured = self.slots[opposite_index] + 1
                self.slots[own_store] += stones_captured
                self.slots[opposite_index] = 0
                self.slots[last_index] = 0

        if self.is_game_over():
            self._sweep_remaining_stones()

        # Whoever moves next: same player again if they earned an extra turn.
        self.turn = player if extra_turn else other_player(player)

        return extra_turn, stones_captured

    def print_board(self):
        # p2 = [self.slots[i] for i in reversed(BINS[PLAYER_2])]
        # p1 = [self.slots[i] for i in BINS[PLAYER_1]]
        # print("               " + "  ".join(f"{v:2}" for v in p2))
        # print(f"  P2 store {self.slots[STORE[PLAYER_2]]:2}" +
        #       " " * 26 + f"P1 store {self.slots[STORE[PLAYER_1]]:2}")
        # print("               " + "  ".join(f"{v:2}" for v in p1))
        # print("pit index:     " + "  ".join(f"{v:2}" for v in BINS[PLAYER_1]))
        p2 = [self.slots[i] for i in reversed(PITS[PLAYER_2])]
        p1 = [self.slots[i] for i in PITS[PLAYER_1]]

        print()
        print("          +----+----+----+----+----+----+")
        print(" P2       |", end=" ")

        for stones in p2:
            print(f"{stones:2} |", end=" ")

        print()
        print("          |    |    |    |    |    |    |")
        print(f"P2 Store  | {self.slots[STORE[PLAYER_2]]:2} |" +
            "                    " +
            f"| {self.slots[STORE[PLAYER_1]]:2} |  P1 Store")
        print("          |    |    |    |    |    |    |")

        print(" P1       |", end=" ")

        for stones in p1:
            print(f"{stones:2} |", end=" ")

        print()
        print("          +----+----+----+----+----+----+")
        print()


if __name__ == "__main__":
    # A few quick manual sanity checks.
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
