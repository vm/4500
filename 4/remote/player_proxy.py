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

SERVER = 'localhost'
PORT = 45678

MIN_FACE, MAX_FACE = 1, 104
MIN_BULL, MAX_BULL = 2, 7


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


class TimingValidator:
    """class for tracking request timing"""

    valid_next_states = {
        None: {'start-round'},
        'start-round': {'take-turn'},
        'take-turn': {'take-turn', 'choose'},
        'choose': {'take-turn'},
    }

    def __init__(self):
        self._latest_request = None

    def is_valid_transition(self, next_request):
        """checks if the next request is will be valid

        :param next_request: request to check
        :type next_request: str

        :returns: whether the request satisfies the timing specification
        :rtype: bool
        """

        return next_request in self.valid_next_states[self._latest_request]

    def update(self, request):
        """updates the latest request

        :param request: new request
        :type request: str
        """

        if not request in self.valid_next_states:
            raise ValueError('Unknown request type')

        self._latest_request = request

def run(server, port):
    """opens a socket and plays a game over the socket

    :param server: server to open the socket on
    :type server: str

    :param port: port to open the socket on
    :type port: int
    """

    sock = socket.create_connection((server, port))
    player = Player()
    validator = TimingValidator()

    try:
        while True:
            msg = read(sock)

            try:
                reply = get_reply(player, validator, msg)
            except ValueError:
                break

            send(sock, reply)

            if reply is False:
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

    while not is_valid_json(msg.strip()):
        msg += sock.recv(1).decode('utf-8')

    return json.loads(msg.strip())


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


def get_reply(player, validator, msg):
    """gets a player's reply to a message

    :param player: player playing the game
    :type player: Player

    :param validator: request order validator
    :type validatior: TimingValidator

    :param msg: message
    :type msg: JSON

    :returns: player reply to a message
    :rtype: JSON
    """

    request_type_to_fn = {
        'start-round': start_round,
        'take-turn': take_turn,
        'choose': choose
    }

    if not isinstance(msg, list) or not msg:
        raise ValueError('Incorrect message format')

    request_type, *params = msg

    if request_type not in request_type_to_fn:
        raise ValueError('Incorrect message format')

    if not validator.is_valid_transition(request_type):
        return False

    request_fn = request_type_to_fn[request_type]
    validator.update(request_type)

    return request_fn(player, *params)


def validate_request_input(validators):
    """validates function input with validators

    :param validators: list of validator functions in argument order
    :type validators: list of func: JSON -> bool

    :returns: request function with input validation
    :rtype: func

    :raises: ValueError if input is invalid
    """

    def wrap(fn):
        def request(player, *args):
            all_valid_inputs = all(
                validator(arg) for validator, arg in zip(validators, args))
            if not all_valid_inputs:
                raise ValueError('Invalid argument type')
            return fn(player, *args)
        return request
    return wrap


def is_json_card(maybe_json_card):
    """check if the input is a valid JSON card

    :param maybe_json_card: input to check
    :type maybe_json_card: JSON

    :returns: whether input is a JSONCard
    :rtype: bool
    """

    if isinstance(maybe_json_card, list) and len(maybe_json_card) == 2:
        [face, bull] = maybe_json_card

        return (isinstance(face, int) and
                isinstance(bull, int) and
                MIN_FACE <= face <= MAX_FACE and
                MIN_BULL <= bull <= MAX_BULL)

    return False


def is_lcard(maybe_lcard):
    """checks if the input is a valid LCard

    :param maybe_lcard: input to check
    :type maybe_lcard: JSON

    :returns: whether input is an LCard
    :rtype: bool
    """

    return isinstance(maybe_lcard, list) and all(map(is_json_card, maybe_lcard))


def is_deck(maybe_deck):
    """checks if the input is a valid deck

    :param maybe_deck: input to check
    :type maybe_deck: JSON

    :returns: whether input is an Deck
    :rtype: bool
    """

    return isinstance(maybe_deck, list) and all(map(is_lcard, maybe_deck))


@validate_request_input([is_lcard])
def start_round(player, hand):
    """starts a round

    :param player: player to player the game
    :type player: Player

    :param hand: hand for a player
    :type hand: LCard

    :returns: True to acknowledge the message
    :rtype: bool
    """

    player.set_hand([json_card_to_internal(json_card) for json_card in hand])
    return True


@validate_request_input([is_deck])
def take_turn(player, deck):
    """takes a turn

    :param player: player to play the game
    :type player: Player

    :param deck: deck of stacks for each turn
    :type deck: Deck

    :returns: card the player wishes to play
    :rtype: Card
    """

    internal_deck = [lcard_to_internal(stack) for stack in deck]
    card = player.pick_card(internal_deck, None)

    return json_card_from_internal(card)


@validate_request_input([is_deck])
def choose(player, deck):
    """chooses a stack

    :param player: player to play the game
    :type player: Player

    :param deck: deck of stacks
    :type deck: Deck

    :returns: stack the player wishes to take
    :rtype: Stack
    """

    internal_deck = [lcard_to_internal(stack) for stack in deck]
    stack_index = player.pick_stack(internal_deck, None, None)

    return deck[stack_index]


def send(sock, reply):
    """sends a reply over the socket

    :param sock: socket connection
    :type sock: socket.SocketType

    :param reply: reply message
    :type reply: JSON
    """

    sock.sendall(str.encode(json.dumps(reply)))


def json_card_to_internal(json_card):
    """convert a JSONCard to a Card

    :param json_card: json card to convert
    :type json_card: JSONCard

    :returns: internal representation of Card
    :rtype: Card
    """

    [face, bull] = json_card
    return Card(face, bull)


def lcard_to_internal(lcard):
    """convert an LCard to a list of Card

    :param lcard: json cards to convert
    :type lcard: LCard

    :returns: internal representation of Cards
    :rtype: list of Card
    """

    return [json_card_to_internal(json_card) for json_card in lcard]


def json_card_from_internal(card):
    """convert a Card to a JSONCard

    :param card: card to convert
    :type card: Card

    :returns: json representation of Card
    :rtype: JSONCard
    """

    return [card.face, card.bull]


if __name__ == "__main__":
    run(SERVER, PORT)
