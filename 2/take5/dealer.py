import random

import os
import sys

PATH_TO_PLAYER = '../../3/'
sys.path.append(os.path.join(os.path.dirname(__file__), PATH_TO_PLAYER))

from player import Card


class Dealer:
    """class that implements a dealer for 6 Nimmt!

    :inv: _initial_deck is immutable
    """

    def __init__(self, players, initial_deck=None, card_handout_order=None):
        """creates a Dealer

        :param players: players to play the game.
        :type players: list of BasePlayer

        :param initial_deck: cards making up a deck
        :type initial_deck: list of Card or None

        :param card_handout_order: order in which cards are handed to players
        :type card_handout_order: list of int or None
        """

        expected_deck_len = 104

        if len(players) < 2 or len(players) > 10:
            raise ValueError('number of players must be in interval [2, 10]')

        self.players = players

        if initial_deck is None:
            self._initial_deck = [Card(i, (i % 6) + 2) for i in range(1, 105)]
        else:
            if len(initial_deck) != expected_deck_len:
                raise ValueError('Incorrect deck size')

            faces = set(card.face for card in initial_deck)
            if len(faces) != len(initial_deck):
                raise ValueError('Contains two cards with the same face value')

            if faces != set(range(1, 105)):
                raise ValueError('Must have only one of every face value')

            if any(card.bull < 2 or card.bull > 7 for card in initial_deck):
                raise ValueError('Deck bull values must be in interval [2,7]')

            self._initial_deck = initial_deck

        if card_handout_order is None:
            self._card_handout_order = range(len(self.players))
        else:
            if len(card_handout_order) != len(self.players):
                raise ValueError("card handout order must"
                                 "match size of players")

            if set(card_handout_order) != set(range(len(self.players))):
                raise ValueError("card handout order must contain "
                                 "one and only one of each player name")

            self._card_handout_order = card_handout_order

        self._deck = None
        self._stacks = None

    def simulate_game(self):
        """simulates one complete game

        :returns: winning player
        :rtype: BasePlayer
        """

        while not self.is_game_over():
            self.play_round()

        return self.get_results()

    def play_round(self):
        """plays a single round"""

        self._deck = self._initial_deck[:]
        random.shuffle(self._deck)

        for player_name in self._card_handout_order:
            self.players[player_name].set_hand(self.deal_hand())

        self._stacks = self.get_new_stacks()

        while self.players_have_cards(self.players):
            self.play_turn()

    @staticmethod
    def players_have_cards(players):
        """determines whether players still have cards

        assumes players have the same number of cards at the start of the turn

        :param players: players to check
        :type players: list of BasePlayer

        :returns: whether players have cards
        :rtype: bool
        """

        return any(p.get_num_cards_in_hand() > 0 for p in players)

    def play_turn(self):
        """plays a single turn"""

        discarded_cards = self.get_discarded_cards()
        self.add_all_cards_to_stacks(discarded_cards)

    def add_all_cards_to_stacks(self, discarded_cards):
        """places the given cards on the stacks and removes points if necessary

        :param discarded_cards: cards to discard, ordered the same as players
        :type discarded_cards: list of Card
        """

        ordered_player_names = self.get_card_placement_order(discarded_cards)
        all_opponent_points = self.get_opponent_points(self.players)
        remaining_cards = {i: c for i, c in enumerate(discarded_cards)}

        for player_name in ordered_player_names:
            card = discarded_cards[player_name]
            player = self.players[player_name]

            opponent_points = all_opponent_points[player_name]
            del remaining_cards[player_name]

            self.add_card_to_stacks(
                player, card, opponent_points, remaining_cards.values())

    def add_card_to_stacks(
            self, player, card, opponent_points, remaining_cards):
        """places a player's card on the stacks and adjust points

        places card on stacks with closest smaller top card
        if this stack has 5 cards, the player loses the sum of the bull points

        if no top cards are smaller, player chooses a stack to place on
        the player loses the sum of the bull points in this stack

        :param player: the player whose card is getting places on the stacks
        :type player: BasePlayer

        :param card: the card to be placed
        :type card: Card

        :param opponent_points: points of opponents
        :type opponent_points: list of int

        :param remaining_cards: discarded cards yet to be played
        :type remaining_cards: list of Card
        """

        closest_smaller_card_stack = self.get_closest_smaller_card(
            card, self._stacks)

        if closest_smaller_card_stack is None:
            chosen_stack_index = player.pick_stack(
                self._stacks, opponent_points, remaining_cards)

            chosen_stack = self._stacks[chosen_stack_index]
            player.remove_points(sum(c.bull for c in chosen_stack))
            self._stacks[chosen_stack_index] = [card]

        else:
            chosen_stack = self._stacks[closest_smaller_card_stack]
            if len(chosen_stack) == 5:
                player.remove_points(sum(c.bull for c in chosen_stack))
                self._stacks[closest_smaller_card_stack] = [card]
            else:
                self._stacks[closest_smaller_card_stack].insert(0, card)

    @staticmethod
    def get_closest_smaller_card(card, stacks):
        """gets index of stack whose top card is smaller and closest to card

        :param card: card to place on stack
        :type card: Card

        :param stacks: stacks to choose from
        :type stacks: list of list of Card

        :returns: index of stack if any cards are smaller else None
        :rtype: int or None
        """

        first_of_stacks = [s[0] for s in stacks]
        closest_smaller_card_stack = None
        closest_smaller_card_delta = float('inf')

        for i, top_card in enumerate(first_of_stacks):
            if card.face > top_card.face:
                card_delta = card.face - top_card.face
                if card_delta < closest_smaller_card_delta:
                    closest_smaller_card_stack = i
                    closest_smaller_card_delta = card_delta

        return closest_smaller_card_stack

    @staticmethod
    def get_opponent_points(players):
        """gets a list of points for all opponents of each player

        example: if there are 3 players with points [-1,-2,-3], respectively,
        this function returns [[-2,-3], [-1,-3], [-1, -2]]

        :param players: players in the came
        :type players: list of BasePlayer

        :returns: list of points for each player's opponents
        :rtype: list of list of int
        """

        all_points = [p.get_points() for p in players]

        all_opponent_points = []
        for i in range(len(players)):
            opponent_points = all_points[:i] + all_points[i+1:]
            all_opponent_points.append(opponent_points)

        return all_opponent_points

    def is_game_over(self):
        """says if the game is over now

        :returns: whether the game is over
        :rtype: bool
        """

        return any(player.get_points() <= -66 for player in self.players)

    def deal_hand(self):
        """gets the first 10 cards of the deck

        :returns: hand to set to a player
        :rtype: list of Card
        """

        cards_in_hand = 10

        if self._deck is None or len(self._deck) < cards_in_hand:
            raise ValueError('invalid deck')

        hand = self._deck[:cards_in_hand]
        self._deck = self._deck[cards_in_hand:]

        return hand

    def get_new_stacks(self):
        """creates new stacks

        :returns: 4 new stacks with 1 card in each
        :rtype: list of list of Card
        """

        num_stacks = 4

        stack_cards = self._deck[:num_stacks]
        self._deck = self._deck[num_stacks:]

        return [[c] for c in stack_cards]

    @staticmethod
    def get_card_placement_order(cards):
        """gets the indices that would sort the cards

        :param cards: cards to order
        :type cards: list of Card

        :returns: indices that would sort the cards
        :rtype: list of int
        """

        return sorted(range(len(cards)), key=lambda i: cards[i].face)

    def get_discarded_cards(self):
        """gathers discarded cards from players

        :returns: discarded cards from players
        :rtype: list of Card
        """

        all_opponent_points = self.get_opponent_points(self.players)

        discarded_cards = []
        for i, player in enumerate(self.players):
            opponent_points = all_opponent_points[i]

            card = player.pick_card(self._stacks, opponent_points)
            discarded_cards.append(card)

        return discarded_cards

    def get_results(self):
        """gets index numbers and points for players in increasing order

        :returns: list of (winning player name, points of winning player)
        :rtype: list of (int, int)
        """

        return sorted(
            [(i, p.get_points()) for i, p in enumerate(self.players)],
            key=lambda x: x[1])
