import json
import os
import socket
import sys
import time
from threading import Thread
from queue import Queue

PATH_TO_PLAYER = '../../3/'
sys.path.append(os.path.join(os.path.dirname(__file__), PATH_TO_PLAYER))

import pytest

import player_proxy as proxy
from player import BasePlayer, Card

CHOSEN_INDEX = 0


class TestPlayer(BasePlayer):
    def pick_card(self, stacks, opponent_points):
        return self._hand[CHOSEN_INDEX]

    def pick_stack(self, stacks, opponent_points, remaining_cards):
        return CHOSEN_INDEX


def test_read():
    """tests read

    cases:
        - {}, [], "", 1, true
        - combination
        - start-round, take-turn, choose
        - long waits
        - two writes in a row --> separate read results
    """

    server = 'localhost'
    port = 45678
    message_queue = Queue()

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((server, port))
    server_sock.listen(1)

    def run_server(sock):
        """runs the socket server and sends messages put in the queue

        :param sock: socket to write to
        :type sock: socket.SocketType
        """

        connection, _client_address = sock.accept()

        while True:
            item = str.encode(message_queue.get())
            connection.sendall(item)

        connection.close()

    thread = Thread(target=run_server, args=(server_sock,))
    thread.setDaemon(True)
    thread.start()

    client_sock = socket.create_connection((server, port))

    empty_hash = {}
    empty_list = []
    single_number = 1
    single_bool = True

    examples = [
        empty_hash, empty_list,
        single_number, single_bool,
        {'hi': ['yo', 'what']},
        ['one', 2, {'three': 4}],
    ]

    for ex in examples:
        message_queue.put(json.dumps(ex))
        assert proxy.read(client_sock) == ex

    hand = [[10, 10], [1, 1], [2, 2]]
    deck = [
        [[4, 4], [5, 5]],
        [[6, 6], [7, 7]]
    ]

    messages = [
        ["start-round", hand],
        ["take-turn", deck],
        ["choose", deck],
    ]

    def wait_message(sock, message):
        for char in json.dumps(message):
            message_queue.put(char)

    for message in messages:
        thread = Thread(target=wait_message, args=(server_sock, message))
        thread.setDaemon(True)
        thread.start()

        assert proxy.read(client_sock) == message

    message_queue.put("".join(map(json.dumps, messages)))
    assert proxy.read(client_sock) == messages[0]
    assert proxy.read(client_sock) == messages[1]
    assert proxy.read(client_sock) == messages[2]

    client_sock.close()
    server_sock.close()


def test_is_valid_json():
    """tests is_valid_json

    cases:
        - valid json parsing
        - invalid json parsing
        - valid messages
        - invalid messages
    """

    assert proxy.is_valid_json('[]')
    assert proxy.is_valid_json('{}')
    assert proxy.is_valid_json('true')
    assert proxy.is_valid_json('"'"'""'"'"')
    assert proxy.is_valid_json('"u\1111"')
    assert proxy.is_valid_json('"\\\/"')
    assert proxy.is_valid_json('{"ok": [{}, {}, "", ["[", "["]]}')

    assert not proxy.is_valid_json('[')
    assert not proxy.is_valid_json('{')

    stack = [[10, 10], [1, 1], [2, 2]]
    assert proxy.is_valid_json('["start-round", {}]'.format(stack))

    deck = [stack, stack, stack, stack]
    assert proxy.is_valid_json('["take-turn", {}]'.format(deck))
    assert proxy.is_valid_json('["choose", {}]'.format(deck))

    assert not proxy.is_valid_json('["start-rou')
    assert not proxy.is_valid_json('["start-round: [')


def test_get_reply_valid():
    """tests get_reply valid cases

    cases:
        - calls appropriate proxy method
    """

    player = TestPlayer()
    validator = proxy.TimingValidator()

    hand = [[10, 10], [1, 1], [2, 2]]
    deck = [
        [[4, 4], [5, 5]],
        [[6, 6], [7, 7]]
    ]

    start_round_msg = ["start-round", hand]
    take_turn_msg = ["take-turn", deck]
    choose_msg = ["choose", deck]

    assert (proxy.get_reply(player, validator, start_round_msg) ==
            proxy.start_round(player, hand))
    assert (proxy.get_reply(player, validator, take_turn_msg) ==
            proxy.take_turn(player, deck))
    assert (proxy.get_reply(player, validator, choose_msg) ==
            proxy.choose(player, deck))
    assert (proxy.get_reply(player, validator, take_turn_msg) ==
            proxy.take_turn(player, deck))
    assert (proxy.get_reply(player, validator, take_turn_msg) ==
            proxy.take_turn(player, deck))
    assert (proxy.get_reply(player, validator, choose_msg) ==
            proxy.choose(player, deck))


def test_get_reply_invalid():
    """tests get_reply invalid cases

    cases:
        - bad message format leads to shutdown
        - timing violation returns false leads to shutdown
    """

    player = TestPlayer()
    validator = proxy.TimingValidator()

    hand = [[10, 10], [1, 1], [2, 2]]
    deck = [
        [[4, 4], [5, 5]],
        [[6, 6], [7, 7]]
    ]

    start_round_msg = ["start-round", hand]
    take_turn_msg = ["take-turn", deck]
    choose_msg = ["choose", deck]

    bad_msg = ["bad", None]
    bad_start_round_msg = ["start-round"]
    bad_take_turn_msg = ["take-turn", deck, True]
    bad_choose_msg = ["choose", "choose again"]

    proxy.get_reply(player, validator, start_round_msg)

    with pytest.raises(ValueError):
        proxy.get_reply(player, validator, None)

    with pytest.raises(ValueError):
        proxy.get_reply(player, validator, bad_msg)

    assert proxy.get_reply(player, validator, choose_msg) is False

    assert (proxy.get_reply(player, validator, take_turn_msg) ==
            proxy.take_turn(player, deck))

    assert proxy.get_reply(player, validator, start_round_msg) is False

    with pytest.raises(ValueError):
        proxy.get_reply(player, validator,
                        ["this is totally not a request", None])

def test_start_round():
    """tests start_round

    cases:
        - valid start_round with test player
    """

    player = TestPlayer()
    hand = [[10, 10], [1, 1], [2, 2], [3, 3]]
    proxy.start_round(player, hand)

    assert player._hand == [Card(*json_card) for json_card in hand]


def test_take_turn():
    """tests take_turn

    cases:
        - valid take_turn with test player
    """

    player = TestPlayer()
    card = Card(10, 10)
    hand = [card, Card(1, 1), Card(2, 2), Card(3, 3)]

    deck = [[[4, 4], [5, 5]]]

    player._hand = hand
    assert proxy.take_turn(player, deck) == [card.face, card.bull]


def test_choose():
    """tests choose

    cases:
        - valid choose with test player
    """

    player = TestPlayer()
    deck = [
        [[10, 10], [1, 1], [2, 2], [3, 3]],
        [[1, 10], [1, 1], [2, 2], [3, 3]],
        [[2, 10], [1, 1], [2, 2], [3, 3]],
        [[3, 10], [1, 1], [2, 2], [3, 3]],
    ]

    assert proxy.choose(player, deck) == deck[CHOSEN_INDEX]


def test_send():
    """tests send

    cases:
        - JSON input equals string output on other socket reciever
    """

    server = 'localhost'
    port = 45678
    message_queue = Queue()
    max_message_len = 1000

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((server, port))
    server_sock.listen(1)

    def run_server(sock):
        """runs the socket server and sends messages put in the queue

        :param sock: socket to write to
        :type sock: socket.SocketType
        """

        connection, _client_address = sock.accept()

        while True:
            item = connection.recv(max_message_len)
            message_queue.put(item)

        connection.close()

    thread = Thread(target=run_server, args=(server_sock,))
    thread.setDaemon(True)
    thread.start()

    client_sock = socket.create_connection((server, port))

    empty_hash = {}
    empty_list = []
    single_number = 1
    single_bool = True

    examples = [
        empty_hash, empty_list,
        single_number, single_bool,
        {'hi': ['yo', 'what']},
        ['one', 2, {'three': 4}],
    ]

    for ex in examples:
        proxy.send(client_sock, ex)
        assert str.encode(json.dumps(ex)) == message_queue.get()

    hand = [[10, 10], [1, 1], [2, 2]]
    deck = [
        [[4, 4], [5, 5]],
        [[6, 6], [7, 7]]
    ]

    messages = [
        ["start-round", hand],
        ["take-turn", deck],
        ["choose", deck],
    ]

    for message in messages:
        proxy.send(client_sock, message)
        assert str.encode(json.dumps(message)) == message_queue.get()

    client_sock.close()
    server_sock.close()


def test_validate_request_input():
    """tests the validate request decorator

    cases:
        - doesn't raise on good input
        - raises on bad input
        - doesn't affect the output of the function on valid input
    """

    good_deck = [
        [[4, 4], [5, 5]],
        [[6, 6], [7, 7]]
    ]

    bad_deck = [
        [[4, 4], [5, 5]],
        [None]
    ]

    player = TestPlayer()
    inner_fn = lambda player, deck: (player, deck)
    dummy_fn = proxy.validate_request_input([proxy.is_deck])(inner_fn)

    assert dummy_fn(player, good_deck) == inner_fn(player, good_deck)

    with pytest.raises(ValueError):
        dummy_fn(player, bad_deck)
