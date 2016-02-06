import os
import sys

PATH_TO_PLAYER = '../../3/'
sys.path.append(os.path.join(os.path.dirname(__file__), PATH_TO_PLAYER))

import pytest

import player_proxy as proxy
from player import BasePlayer

CHOSEN_INDEX = 0


class TestPlayer(BasePlayer):
    def pick_card(self, *args):
        return self._hand[CHOSEN_INDEX]

    def pick_stack(self, k):
        return CHOSEN_INDEX


def test_read():
    """tests read

    cases:
        - create TCP socket and write
        - valid
            - {}, [], 1, true
            - start-round, take-turn, choose
        - long waits
        - out of order action
    """

    pass


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
    assert proxy.is_valid_json('"\"\""')
    assert proxy.is_valid_json('"{\"ok: [{}, {}]}"')

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

    assert player._hand == hand


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

    pass
