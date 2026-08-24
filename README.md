# Mancala Adversarial Search (CSE318 Assignment 3)

A Mancala (Kalah-variant) game player built with minimax search and alpha-beta
pruning, plus four heuristics of increasing sophistication to compare via
computer-vs-computer experiments.

## Files

| File | What it does |
|---|---|
| `board.py` | The `MancalaBoard` class: board setup, legal moves, sowing/capture/extra-turn rules, game-over detection. |
| `heuristics.py` | `heuristic_1` .. `heuristic_4`, matching the four evaluation functions from the assignment. |
| `ai.py` | Minimax search with alpha-beta pruning (`minimax_alpha_beta`, `choose_move`). |
| `game.py` | Console game you can play: Human vs AI, or watch AI vs AI. |
| `experiment.py` | Runs many AI vs AI games between two heuristics and reports win/loss/tie ratios. |

## Mancala rules used

- 14 board slots: indices 0-5 are Player 1's pits, 6 is Player 1's store,
  7-12 are Player 2's pits, 13 is Player 2's store. Each pit starts with 4 stones.
- On your turn, pick one of your own non-empty pits. Its stones are sown one
  by one into the following pits/store, going counter-clockwise and
  **skipping the opponent's store**.
- If your last stone lands in **your own store**, you get an extra turn.
- If your last stone lands in an **empty pit on your own side**, you capture
  that stone plus everything in the opposite pit, and they go to your store.
- The game ends when one player's 6 pits are all empty. Whoever still has
  stones on their side sweeps them all into their own store. Whoever has more
  stones in their store wins.

## Heuristics

All four look at the board from one player's point of view (higher = better for them):

- **heuristic_1**: `my_store - opponent_store`
- **heuristic_2**: adds `stones_on_my_side - stones_on_opponent_side`
- **heuristic_3**: adds a bonus if the move earned an extra turn
- **heuristic_4**: adds a bonus for stones captured by the move

Each has tunable weights (`w1`, `w2`, ...) with sensible defaults, so you can
experiment with different weightings without touching the rest of the code.

## How to run it

**Play a game (human vs AI, or watch AI vs AI):**
```
python game.py
```
You'll be asked whether you want to play, and which heuristic(s) the AI
should use.

**Compare heuristics automatically:**
```
python experiment.py
```
This plays every pairwise matchup among the four heuristics (20 games each
by default) and prints win/loss/tie counts and percentages. Edit
`num_games` and `search_depth` at the bottom of `experiment.py` to run more
games or search deeper (deeper search = slower but stronger play).

## A note on determinism

Minimax always picks the best move for a fixed heuristic from a fixed
position, so a given heuristic-vs-heuristic matchup produces the **same
result in every game** when both players always start from the identical
opening board. That's why `experiment.py`'s results currently look like
20-0 rather than a spread of scores. If you want real variance across games
(useful for a report), two easy options:

- Alternate which heuristic plays Player 1 vs Player 2 across games.
- Add slight randomness when breaking ties between equally-good moves.

## Requirements

Just Python 3 (no external libraries needed).
