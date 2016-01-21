"""
This game exists.
"""

from player import Player


def main():
    num_players = int(input('Number of players.'))
    players = [Player() for _ in xrange(num_players)]

    dealer = Dealer()
    return
