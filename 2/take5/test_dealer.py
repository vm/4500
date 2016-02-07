import os
import sys

PATH_TO_PLAYER = '../../3/'
sys.path.append(os.path.join(os.path.dirname(__file__), PATH_TO_PLAYER))

import pytest

from dealer import Dealer
from player import Card, BasePlayer

class MockPlayer(BasePlayer):
    def pick_card(self, stacks, opponent_points):

        return self._hand.pop(0)

    def pick_stack(self, stacks, opponent_points, remaining_cards):
        return 0


def test_dealer_creation():
    """tests that the dealer does not accept invalid input"""

    with pytest.raises(ValueError):
        low_players = [MockPlayer()]
        Dealer(low_players)

    with pytest.raises(ValueError):
        high_players = [MockPlayer() for _ in range(11)]
        Dealer(high_players)

    low_valid_players = [MockPlayer() for _ in range(2)]
    Dealer(low_valid_players)

    high_valid_players = [MockPlayer() for _ in range(10)]
    Dealer(high_valid_players)

    valid_deck = [Card(i, (i%6) + 2) for i in range(1, 105)]
    Dealer(high_valid_players, valid_deck)

    with pytest.raises(ValueError):
        short_deck = [Card(i, 2) for i in range(1, 100)]
        Dealer(high_valid_players, short_deck)

    with pytest.raises(ValueError):
        wrong_face_values_deck = [Card(i, 2) for i in range(0, 104)]
        Dealer(high_valid_players, wrong_face_values_deck)

    with pytest.raises(ValueError):
        wrong_bull_values_deck = [Card(i, 0) for i in range(1, 105)]
        Dealer(high_valid_players, wrong_bull_values_deck)

    d = Dealer(high_valid_players)
    assert d._initial_deck == valid_deck


def test_get_closest_smaller_card():
    """tests dealer's get_closest_smaller_card"""

    d = Dealer([MockPlayer(), MockPlayer()])

    stacks = [[Card(4, 1)], [Card(5, 1)], [Card(6, 1)], [Card(7, 1)]]
    card = Card(3, 4)
    assert d.get_closest_smaller_card(card, stacks) is None

    stacks[0] = [Card(2, 1)]
    assert d.get_closest_smaller_card(card, stacks) == 0


def test_get_opponent_points():
    """tests that getting opponent's points returns correct output"""

    players = [MockPlayer(), MockPlayer()]
    players[0].remove_points(10)
    players[1].remove_points(3)
    d = Dealer(players)

    assert d.get_opponent_points(players) == [[-3], [-10]]


def test_get_card_placement_order():
    """tests that getting card placement order returns correct output"""

    d = Dealer([MockPlayer(), MockPlayer()])
    cards = [Card(10, 1), Card(2, 1), Card(6, 1), Card(5, 1)]

    assert d.get_card_placement_order(cards) == [1, 3, 2, 0]


def test_add_card_to_stacks():
    """tests adding a card to stacks

    cases:
        - all top-cards of stacks are larger than given card
          leads to player picking stack based on pick_stack,
          removes sum of bull points in stack, and replaces stack
          with given card

        - any top-cards of stacks are smaller leads to closest smaller card
          stack being picked
            - if that stack is 5 cards, remove sum of bull points in stack
              and replace stack with given card
            - otherwise, place given card on stack
    """

    players = [MockPlayer() for _ in range(2)]
    d = Dealer(players)

    # all top-cards of stacks are larger
    card = Card(3, 6)
    player = players[0]
    initial_stacks = [
        [Card(28, 3), Card(17, 5)],
        [Card(4, 2), Card(1, 3)],
        [Card(100, 4), Card(90, 3)] ,
        [Card(101, 4), Card(91, 3)],
    ]

    expected_stacks = [
        [card],
        [Card(4, 2), Card(1, 3)],
        [Card(100, 4), Card(90, 3)] ,
        [Card(101, 4), Card(91, 3)],
    ]

    d._stacks = initial_stacks
    d.add_card_to_stacks(player, card, [], [])
    assert d._stacks == expected_stacks

    # top-cards of stacks are smaller, smallest-closest stack is 5 cards
    card = Card(9, 6)
    player = players[0]
    initial_stacks = [
        [Card(28, 3), Card(17, 5)],
        [Card(7, 3), Card(5, 3), Card(4, 2), Card(2, 6), Card(1, 3)],
        [Card(100, 4), Card(90, 3)] ,
        [Card(101, 4), Card(91, 3)],
    ]

    expected_stacks = [
        [Card(28, 3), Card(17, 5)],
        [card],
        [Card(100, 4), Card(90, 3)] ,
        [Card(101, 4), Card(91, 3)],
    ]

    d._stacks = initial_stacks
    d.add_card_to_stacks(player, card, [], [])
    assert d._stacks == expected_stacks

    # top-cards of stacks are smaller, smallest-closest stack is not 5 cards
    card = Card(5, 6)
    player = players[0]
    initial_stacks = [
        [Card(28, 3), Card(17, 5)],
        [Card(4, 2), Card(1, 3)],
        [Card(100, 4), Card(90, 3)] ,
        [Card(101, 4), Card(91, 3)],
    ]

    expected_stacks = [
        [Card(28, 3), Card(17, 5)],
        [Card(5, 6), Card(4, 2), Card(1, 3)],
        [Card(100, 4), Card(90, 3)] ,
        [Card(101, 4), Card(91, 3)],
    ]

    d._stacks = initial_stacks
    d.add_card_to_stacks(player, card, [], [])
    assert d._stacks == expected_stacks


def test_is_game_over():
    """tests that the game only says it's over iff it's over"""

    players = [MockPlayer() for _ in range(2)]

    d = Dealer(players)
    assert not d.is_game_over()

    for p in players:
        p._points = -66

    d.players = players
    assert d.is_game_over()


def test_deal_hand():
    """tests that dealing hands deals hands"""

    players = [MockPlayer() for _ in range(2)]
    d = Dealer(players)
    d._deck = d._initial_deck[:]

    full_deck_len = len(d._deck)
    dealt_hand = d.deal_hand()

    assert len(dealt_hand) == 10
    assert len(d._deck) == (full_deck_len - len(dealt_hand))


def test_get_new_stacks():
    """tests that creating stacks creates good stacks"""

    players = [MockPlayer() for _ in range(2)]
    d = Dealer(players)
    d._deck = d._initial_deck[:]

    new_stacks = d.get_new_stacks()

    assert len(new_stacks) == 4
    assert all(len(s) == 1 for s in new_stacks)


def test_get_discarded_cards():
    """tests getting discarded cards from each player"""

    players = [MockPlayer() for _ in range(2)]
    d = Dealer(players)
    d._deck = d._initial_deck[:]

    for p in d.players:
        p._hand = [Card(6, 3)]

    discarded_cards = d.get_discarded_cards()

    assert discarded_cards == [Card(6,3), Card(6,3)]


def test_simulate_game():
    """tests that the dealer properly simulates a game"""

    players = [MockPlayer() for _ in range(4)]
    dealer = Dealer(players)

    winning_player_name, winning_player_points = dealer.simulate_game()[0]
    min_winning_score = -66

    assert winning_player_points <= min_winning_score
    assert all(p.get_points() <= 0 for p in dealer.players)
