"""
DATA DEFINITIONS

    A Name is a JSON string

    An Integer is a JSON number interpretable as a positive integer

    A JSONCard is [Integer, Integer]
        - the first Integer is face value, as described by the requirements
          analysis for 6Nimmt!
        - the second Integer is bull point value, as described by the
          requirements analysis for 6Nimmt!

    A LCard is [JSONCard, ..., JSONCard]

    A Stack is an LCard that contains at least one JSONCard

    A Deck is [Stack, ..., Stack]

    A JSON is one of:
        - int
        - str
        - list
        - dict
"""

import os
import sys

PATH_TO_PLAYER = '../../3/'
sys.path.append(os.path.join(os.path.dirname(__file__), PATH_TO_PLAYER))

import json
import socket

from player import BasePlayer, Card

SERVER = socket.gethostname()
PORT = 45678


class Player(BasePlayer):
    def pick_card(self, stacks, opponent_points):
        """picks a card to play and removes it from the player's hand

        :param stacks: current state of the stacks in the game
        :type stacks: list of list of Card

        :param opponent_points: number of points each opponent has
        :type opponent_points: list of int

        :returns: card to play from the player's hand
        :rtype: Card
        """

        remove_card_index = max(range(len(self._hand)),
                                key=lambda i: self._hand[i].face)
        return self._hand.pop(remove_card_index)

    def pick_stack(self, stacks, opponent_points, remaining_cards):
        """chooses a stack to pick up

        :param stacks: current state of the stacks in the game
        :type stacks: list of list of Card

        :param opponent_points: number of points each opponent has
        :type opponent_points: list of int

        :param remaining_cards: cards yet to be played in the turn
        :type remaining_cards: list of Card

        :returns: index of the stack to pick up
        :rtype: int
        """

        return min(range(len(stacks)),
                   key=lambda i: sum(card.bull for card in stacks[i]))


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


def start_round(player, hand):
    """starts a round

    :param player: player to player the game
    :type player: Player

    :param hand: hand for a player
    :type hand: LCard

    :returns: True to acknowledge the message
    :rtype: bool
    """

    player.set_hand([_json_card_to_internal(json_card) for json_card in hand])


def take_turn(player, deck):
    """takes a turn

    :param player: player to play the game
    :type player: Player

    :param deck: deck of stacks for each turn
    :type deck: Deck

    :returns: card the player wishes to play
    :rtype: Card
    """

    internal_deck = [_lcard_to_internal(stack) for stack in deck]
    card = player.pick_card(internal_deck, None)

    return _json_card_from_internal(card)


def choose(player, deck):
    """chooses a stack

    :param player: player to play the game
    :type player: Player

    :param deck: deck of stacks
    :type deck: Deck

    :returns: stack the player wishes to take
    :rtype: Stack
    """

    internal_deck = [_lcard_to_internal(stack) for stack in deck]
    stack_index = player.pick_stack(internal_deck, None, None)

    return deck[stack_index]


def send(sock, reply):
    """sends a reply over the socket

    :param sock: socket connection
    :type sock: socket.SocketType

    :param reply: reply message
    :type reply: JSON
    """

    raise NotImplementedError()


def _json_card_to_internal(json_card):
    """convert a JSONCard to a Card

    :param json_card: json card to convert
    :type json_card: JSONCard

    :returns: internal representation of Card
    :rtype: Card
    """

    face, bull = json_card[0], json_card[1]
    return Card(face, bull)


def _lcard_to_internal(lcard):
    """convert an LCard to a list of Card

    :param lcard: json cards to convert
    :type lcard: LCard

    :returns: internal representation of Cards
    :rtype: list of Card
    """

    return [_json_card_to_internal(json_card) for json_card in lcard]


def _json_card_from_interal(card):
    """convert a Card to a JSONCard

    :param card: card to convert
    :type card: Card

    :returns: json representation of Card
    :rtype: JSONCard
    """

    return [card.face, card.bull]


if __name__ == "__main__":
    run(SERVER, PORT)
