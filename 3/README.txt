The purpose of this project was to update the game implementation and to add a player-protocol specification.

player-protocol.txt: communication protocol to interact with external players
take5/player.py: implementation of player according to the specification
take5/mandatory.patch: patch for game implementation in /2 to reference player in /3
take5/bugs.patch: fix a bug
take5/1.patch: force players to pick up a stack if it is six cards deep instead of five
take5/2.patch: use 210 cards with face value between 1 and 210
take5/3.patch: deal players 9 cards instead of 10
take5/4.patch: increase minimum bull points from 2 to 3
take5/5.patch: implement player who places cards in increasing order of face value

-------------------------------------
justifications for multi-line patches
-------------------------------------

mandatory.patch
- os and sys were imported to append to the PYTHONPATH in main.py, test_dealer.py
- moves player.py from /2 to /3

bugs.patch
- forgot to put `raise` before a `ValueError`

2.patch
- abstracts the maximum number of players to be based on number
  of cards in the deck, number of cards dealt to players, and number of stacks
- abstracts first face value and length of deck to change from 104 to 210
  in all places

3.patch
- abstracts the maximum number of players to be based on number
  of cards in the deck, number of cards dealt to players, and number of stacks
- changes number of cards dealt to players from 9 to 10

4.patch
- abstracts the minimum and maximum bull point values as variables
- changes the minimum bull point value from 2 to 3

5.patch
- implements a player who places cards in increasing order

------------------
patch dependencies
------------------

patches must be applied from the base directory (containing /2 and /3)
bugs.patch requires mandatory.patch
n.patch for n = 1...5 requires bugs.patch
