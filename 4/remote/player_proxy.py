import os
import sys

PATH_TO_PLAYER = '../../3/'
sys.path.append(os.path.join(os.path.dirname(__file__), PATH_TO_PLAYER))

import json
import socket

from player import BasePlayer

SERVER = socket.gethostname()
PORT = 45678

class Player(BasePlayer):
    pass

"""
DATA DEFINITIONS

    A Name is a JSON string

    An Integer is a JSON number interpretable as a positive integer

    A Card is [Integer, Integer]
        - the first Integer is face value, as described by the requirements
          analysis for 6Nimmt!
        - the second Integer is bull point value, as described by the
          requirements analysis for 6Nimmt!

    A LCard is [Card, ..., Card]

    A Stack is an LCard that contains at least one Card

    A Deck is [Stack, ..., Stack]

    A JSON is one of:
        - int
        - str
        - list
        - dict
"""


def run(server, port):
    """opens a socket and plays a game over the socket

    :param server: server to open the socket on
    :type server: str

    :param port: port to open the socket on
    :type port: int
    """

    sock = socket.create_connection((server, port))
    player = Player()

    try:
        while True:
            msg = read(sock)

            try:
                ret = get_reply(player, msg)
            except ValueError:
                break

            send(sock, ret)

            if ret is False:
                break
    finally:
        sock.close()


def read(sock):
    """reads a message from a socket and returns it as JSON

    :param sock: socket connection
    :type sock: socket.SocketType

    :returns: JSON message parsed into a python object
    :rtype: JSON
    """

    msg = ''

    while not is_valid_json(msg):
        msg += sock.recv(1).decode('utf-8')

    return json.loads(msg)


def is_valid_json(msg):
    """determines if a message is valid JSON

    :param msg: message to check
    :type msg: string

    :returns: whether input is valid json
    :rtype: bool
    """

    try:
        json.loads(msg)
        return True
    except ValueError:
        return False


def get_reply(player, msg):
    """gets a player's reply to a message

    :param player: player playing the game
    :type player: Player

    :param msg: message
    :type msg: JSON

    :returns: player reply to a message
    :rtype: JSON
    """

    # check if the msg matches one of the spec requests
    # call the appropriate method
    # else ?? TODO

    raise ValueError("Invalid message")

    raise NotImplementedError()


def start_round(player, hand):
    """starts a round

    :param player: player to player the game
    :type player: Player

    :param hand: hand for a player
    :type hand: LCard

    :returns: True to acknowledge the message
    :rtype: bool
    """

    raise NotImplementedError()


def take_turn(player, deck):
    """takes a turn

    :param player: player to play the game
    :type player: Player

    :param deck: deck of stacks for each turn
    :type deck: Deck

    :returns: card the player wishes to play
    :rtype: Card
    """

    raise NotImplementedError()


def choose(player, deck):
    """chooses a stack

    :param player: player to play the game
    :type player: Player

    :param deck: deck of stacks
    :type deck: Deck

    :returns: stack the player wishes to take
    :rtype: Stack
    """

    raise NotImplementedError()


def send(sock, reply):
    """sends a reply over the socket

    :param sock: socket connection
    :type sock: socket.SocketType

    :param reply: reply message
    :type reply: JSON
    """

    raise NotImplementedError()


if __name__ == "__main__":
    run(SERVER, PORT)
