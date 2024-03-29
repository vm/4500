"""
This game exists.
"""

import os
import sys

PATH_TO_PLAYER = '../../3/'
sys.path.append(os.path.join(os.path.dirname(__file__), PATH_TO_PLAYER))

from player import DemoPlayer
from dealer import Dealer

def main():
    num_players = int(input('Number of players: '))
    players = [DemoPlayer() for _ in range(num_players)]

    dealer = Dealer(players)
    player_results = dealer.simulate_game()

    fmt = "player name: {}\nplayer score: {}\n"
    for name, score in player_results:
        print(fmt.format(name, score))

if __name__ == '__main__':
    main()
