The purpose of this project was to update the player implementation to reflect specification changes.

player.py: implementation of player according to the specification
mandatory.patch: patch for game implementation in /2 to reference player in /3
bugs.patch: patch to fix a bug
1.patch: patch to force players to pick up a stack if it is six cards deep instead of five
2.patch: patch to use 210 cards with face value between 1 and 210
3.patch: patch to deal players 9 cards instead of 10
4.patch: patch to increase minimum bull points from 2 to 3
5.patch: patch to implement player who places cards in increasing order of face value

justifications for multi-line patches:

mandatory.patch
- os and sys were imported to append to the PYTHONPATH in main.py, test_dealer.py
- moves player.py from /2 to /3

bugs.patch
- forgot to put `raise` before a `ValueError`

2.patch
- abstracts the maximum number of players to be based on number of cards in the deck, number of cards dealt to players, and number of stacks
- abstracts first face value and length of deck to change from 104 to 210 in all places

3.patch
- abstracts the maximum number of players to be based on number of cards in the deck, number of cards dealt to players, and number of stacks
- changes number of cards dealt to players from 9 to 10

4.patch
- abstracts the minimum and maximum bull point values as variables
- changes the minimum bull point value from 2 to 3

5.patch
- implements a player who places cards in increasing order

patch dependencies:

bugs.patch requires mandatory.patch
n.patch for n = 1...5 requires bugs.patch
