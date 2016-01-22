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
    d = Dealer([MockPlayer(), MockPlayer()])

    stacks = [[Card(4, 1)], [Card(5, 1)], [Card(6, 1)], [Card(7, 1)]]
    card = Card(3, 4)
    assert d.get_closest_smaller_card(card, stacks) is None

    stacks[0] = [Card(2, 1)]
    assert d.get_closest_smaller_card(card, stacks) == 0


def test_get_opponent_points():
    players = [MockPlayer(), MockPlayer()]
    players[0].remove_points(10)
    players[1].remove_points(3)
    d = Dealer(players)

    assert d.get_opponent_points(players) == [[-3], [-10]]


def test_get_card_placement_order():
    d = Dealer([MockPlayer(), MockPlayer()])
    cards = [Card(10, 1), Card(2, 1), Card(6, 1), Card(5, 1)]

    assert d.get_card_placement_order(cards) == [1, 3, 2, 0]


def test_simulate_game():
    """tests that the dealer properly simulates a game"""

    players = [MockPlayer() for _ in range(4)]
    dealer = Dealer(players)

    winning_player_name, winning_player_points = dealer.simulate_game()
    min_winning_score = -66

    assert winning_player_points <= min_winning_score
    assert all(p.get_points() <= 0 for p in dealer.players)
