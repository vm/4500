import pytest

from dealer import Dealer
from player import Card, BasePlayer

class MockPlayer(BasePlayer):
    def pick_card(self, stacks, opponent_points):
        return self._hand[0]

    def pick_stacks(self, stacks, opponent_points, remaining_cards):
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

    high_valid_players = [MockPlayer() for _ in range(11)]
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
    assert d.deck == valid_deck

def test_simulate_game():
    """tests that the dealer properly simulates a game"""

    players = [MockPlayer() for _ in range(4)]
    dealer = Dealer(players)

    winning_player = dealer.simulate_game()
    min_winning_score = -66

    assert winning_player in players
    assert winning_player.get_points() <= min_winning_score
    assert min(dealer.players, key=lambda p: p.get_points()) == winning_player
    assert all(p.get_points() <= 0 for p in dealer.players)
