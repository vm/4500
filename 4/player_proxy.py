import os
import sys

PATH_TO_PLAYER = '../3/'
sys.path.append(os.path.join(os.path.dirname(__file__), PATH_TO_PLAYER))

import json
import socket

from player import Player

SERVER = 'localhost'
PORT = 45678


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
            ret = get_reply(player, msg)
            send(sock, ret)
    finally:
        sock.close()


def read(sock, bufsize=16):
    """reads a message from a socket and returns it as JSON

    :param sock: socket connection
    :type sock: Socket

    :param bufsize: buffer size for reading from the socket
    :type bufsize: int

    :returns: JSON message parsed into a python object
    :rtype: JSON
    """

    msg = ''

    while not is_valid_json(msg):
        msg += sock.recv(bufsize)

    return json.loads(msg)


def is_valid_json(s):
    """determines if a message is valid JSON

    :param s: string to check
    :type s: string

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

    :param player: player to player the game
    :type player: Player

    :param deck: deck of stacks for each turn
    :type deck: Deck

    :returns: card the player wishes to player
    :rtype: Card
    """

    raise NotImplementedError()


def choose(player, deck):
    """chooses a stack

    :param player: player to player the game
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
    :type sock: Socket

    :param reply: reply message
    :type reply: JSON
    """

    raise NotImplementedError()


if __name__ == "__main__":
    run(SERVER, PORT)
