import json
import os
import socket
import sys
from multiprocessing import Process, Queue

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

    write_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    write_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    write_sock.bind((server, port))
    write_sock.listen(1)

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

    Process(target=run_server, args=(write_sock,)).start()
    read_sock = socket.create_connection((server, port))

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
        assert proxy.read(read_sock) == ex

    hand = [[0, 0], [1, 1], [2, 2]]
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
        Process(target=wait_message, args=(write_sock, message)).start()
        assert proxy.read(read_sock) == message

    message_queue.put("".join(map(json.dumps, messages)))
    assert proxy.read(read_sock) == messages[0]
    assert proxy.read(read_sock) == messages[1]
    assert proxy.read(read_sock) == messages[2]

    write_sock.close()


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

    stack = [[0, 0], [1, 1], [2, 2]]
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

    hand = [[0, 0], [1, 1], [2, 2]]
    deck = [
        [[4, 4], [5, 5]],
        [[6, 6], [7, 7]]
    ]

    start_round_msg = ["start_round", hand]
    take_turn_msg = ["take_turn", deck]
    choose_msg = ["choose", deck]

    assert (proxy.get_reply(player, start_round_msg) ==
            proxy.start_round(player, hand))
    assert (proxy.get_reply(player, take_turn_msg) ==
            proxy.take_turn(player, deck))
    assert (proxy.get_reply(player, choose_msg) ==
            proxy.choose(player, deck))
    assert (proxy.get_reply(player, take_turn_msg) ==
            proxy.take_turn(player, deck))
    assert (proxy.get_reply(player, take_turn_msg) ==
            proxy.take_turn(player, deck))
    assert (proxy.get_reply(player, choose_msg) ==
            proxy.choose(player, deck))


def test_get_reply_invalid():
    """tests get_reply invalid cases

    cases:
        - bad message format leads to shutdown
        - timing violation returns false leads to shutdown
    """

    player = TestPlayer()

    hand = [[0, 0], [1, 1], [2, 2]]
    deck = [
        [[4, 4], [5, 5]],
        [[6, 6], [7, 7]]
    ]

    start_round_msg = ["start_round", hand]
    take_turn_msg = ["take_turn", deck]
    choose_msg = ["choose", deck]

    bad_msg = ["bad"]
    bad_start_round_msg = ["start_round"]
    bad_take_turn_msg = ["take_turn", deck, True]
    bad_choose_msg = ["choose", "choose again"]

    proxy.get_reply(player, start_round_msg)

    with pytest.raises(ValueError):
        proxy.get_reply(player, bad_msg)

    assert proxy.get_reply(player, choose_msg) is False

    assert (proxy.get_reply(player, take_turn_msg) ==
            proxy.take_turn(player, deck))

    assert proxy.get_reply(player, start_round_msg) is False


def test_start_round():
    """tests start_round

    cases:
        - valid start_round with test player
    """

    player = TestPlayer()
    hand = [[0, 0], [1, 1], [2, 2], [3, 3]]
    proxy.start_round(player, hand)

    assert player._hand == [Card(*json_card) for json_card in hand]


def test_take_turn():
    """tests take_turn

    cases:
        - valid take_turn with test player
    """

    player = TestPlayer()
    card = [0, 0]
    hand = [card, [1, 1], [2, 2], [3, 3]]

    deck = [[[4, 4], [5, 5]]]

    player._hand = hand
    assert proxy.take_turn(player, deck) == card


def test_choose():
    """tests choose

    cases:
        - valid choose with test player
    """

    player = TestPlayer()
    deck = [
        [[0, 0], [1, 1], [2, 2], [3, 3]],
        [[1, 0], [1, 1], [2, 2], [3, 3]],
        [[2, 0], [1, 1], [2, 2], [3, 3]],
        [[3, 0], [1, 1], [2, 2], [3, 3]]
    ]

    assert proxy.choose(player, deck) == deck[CHOSEN_INDEX]


def test_send():
    """tests send

    cases:
        - JSON input equals string output on other socket reciever
    """

    server = socket.gethostname()
    port = 45678

    write_sock = socket.create_connection((server, port))
    read_sock = socket.create_connection((server, port))

    empty_hash = {}
    empty_list = []
    empty_string = ""
    single_number = 1
    single_bool = True

    examples = [
        empty_has, empty_list, empty_string,
        single_number, single_bool,
        {'hi': ['yo', 'what']},
        ['one', 2, {'three': 4}],
    ]

    for ex in examples:
        proxy.send(write_sock, ex)
        assert read_sock.recv(bufsize=len(ex)) == str(ex)
