import operator

from player import Card


class Dealer:
    """class that implements a dealer for 6 Nimmt!

    :inv: _initial_deck is immutable
    """

    def __init__(self, players, initial_deck=None):
        """creates a Dealer

        :param players: players to play the game.
        :type players: list of BasePlayer
        """

        if len(players) < 2 or len(players) > 10:
            raise ValueError('number of players must be in interval [2, 10]')

        if initial_deck is None:
            self._initial_deck = [Card(i, (i % 6) + 2) for i in range(1, 105)]
        else:
            if len(initial_deck) != expected_deck_len:
                raise ValueError('Incorrect deck size')

            if not set(card.face for card in initial_deck) == set(range(1, 105)):
                raise ValueError('Must have only one of every face value')

            self._initial_deck = full_deck

        self.players = players
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

        for player in self.players:
            player.set_hand(self.deal_hand())

        self._stacks = self.create_stacks()

        while self.players_have_cards():
            self.play_turn()

    def play_turn(self):
        """plays a single turn"""

        opponent_points = get_opponent_points(self.players)
        discarded_cards = self.get_discarded_cards(opponent_points)
        self.place_cards_on_stacks(discarded_cards, opponent_points)

    def place_cards_on_stacks(self, discarded_cards):
        """places the given cards on the stacks and removes points if necessary

        :param discarded_cards: cards to discard, ordered the same as players
        :type discarded_cards: list of Card
        """

        ordered_player_names = self.get_card_placement_order(discarded_cards)

        for player_name in ordered_player_names:
            card, player = discarded_cards[player_name], self.players[player_name]
            self._stacks = place_card_on_stacks(self._stacks)

    @staticmethod
    def place_card_on_stacks(player, card, stacks):
        """places a player's card on the stacks and adjust points. if any of
        the cards on top of the stacks are greater than card, TODO(DO STUFF)

        :param player: the player whose card is getting places on the stacks
        :type player: BasePlayer
        :param card: the card to be placed
        :type card: Card
        :param stacks: the stacks of cards
        :type stacks: list of list of Card

        :returns: the updated stacks
        :rtype: list of list of Card
        """

        closest_smaller_card_stack = self.get_closest_smaller_card(card, stacks)

        if closest_smaller_card_stack is None:
            opponent_points = toeuoeiajroairj
            remaining_cards = eoitiojt
            chosen_stack_index = player.pick_stack(
                stacks, opponent_points, remaining_cards)

        else:
            chosen_stack = stacks[closest_smaller_card_stack]
            if len(chosen_stack) == 5:
                player.remove_points(sum(c.bull for c in chosen_stack))
                chosen_stack = [card]
            else:
                chosen_stack.insert(0, card)

        return stacks

    @staticmethod
    def get_closest_smaller_card(card, stacks):
        """checks the first card of every stack and returns the index of the
        stack whose first face value is smaller than and closest to the given
        card

        :param card: card to place on stack
        :type card: Card
        :param stacks: stacks to choose from
        :type stacks: list of list of Card

        :returns: index of stack to place card on if there any of the top cards
            have a smaller face value
        :rtype: None or int
        """

        first_of_stacks = [s[0] for s in stacks]
        closest_smaller_card_stack = None
        closest_smaller_card_delta = float('inf')

        for i, top_card in enumerate(first_of_stacks):
            card_delta = card.face - top_card.face

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
            opponent_points = self.exclude_item(i, all_points)
            all_opponent_points.append(opponent_points)

        return all_opponent_points

    @staticmethod
    def exclude_item(i, xs):
        return xs.pop(i)

    def is_game_over(self):
        """says if the game is over now

        :returns: whether the game is over
        :rtype: bool
        """

        return any(player.points <= -66 for player in self.players)

    def deal_hand(self):

        # todo add error if deck is None or not enough cards
        raise NotImplementedError('meow')

    def create_stacks(self):
        """creates new stacks

        :returns: 4 new stacks with 1 card in each
        :rtype: list of list of Card
        """

        raise NotImplementedError('meow')

    @staticmethod
    def get_card_placement_order(cards):
        """gets the indices that would sort the cards

        :param cards: cards to order
        :type cards: list of Card

        :returns: indices that would sort the cards
        :rtype: list of int
        """

        return sorted(range(len(cards)), lambda i: cards[i].face)

    def get_discarded_cards(self):
        """gathers discarded cards from players

        :returns: discarded cards from players
        :rtype: list of Card
        """

        all_opponent_points = self.get_opponent_points(self._players)

        discarded_cards = []
        for i, player in enumerate(self.players):
            opponent_points = all_opponent_points[i]

            card = player.pick_cards(stacks, opponent_points)
            discarded_cards.append(card)

        return discarded_cards

    def get_results(self):
        raise NotImplementedError('meow')
