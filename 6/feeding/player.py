from feeding.species import Species
from feeding.result import (
    FatTissueResult, VegetarianResult, CarnivoreResult, NoFeedingResult)

"""
A JSONPlayer is
    [["id",Natural+],
     ["species",LOS],
     ["bag",Natural]]

A LOP is [JSONPlayer, ..., JSONPlayer]; the list might be empty.
"""


class BasePlayer:
    """base class for a Player

    :attr _food_bag: number of tokens in the food bag
    :type _food_bag: int

    :attr _cards: cards to be played
    :type _cards: list of Trait

    :attr _boards: species boards
    :type _boards: list of Species
    """

    def __init__(self, player_id, species=None, food_bag=0):
        """creates a BasePlayer

        :param food_bag: food bag represented by the number of tokens inside
        :type food_bag: int
        """

        self._player_id = player_id
        self._boards = species if species is not None else []
        self._food_bag = food_bag
        self._cards = []

    @classmethod
    def from_json(cls, json_player):
        """creates a Player from a JSON representation

        :param json_player: JSON player
        :type json_player: JSONPlayer

        :returns: player
        :rtype: Player
        """

        [[_, player_id], [_, json_species], [_, bag]] = json_player
        species = [Species.from_json(s) for s in json_species]

        return cls(player_id, species, bag)

    def to_json(self):
        """creates a JSON representation of the player

        :returns: JSON player
        :rtype: JSONPlayer
        """

        json_boards = [b.to_json() for b in self._boards]

        return [["id", self._player_id],
                ["species", json_boards],
                ["bag", self._food_bag]]

    @property
    def food_bag(self):
        """gets the number of tokens in the food bag

        :returns: number of tokens in the food bag
        :rtype: int
        """

        return self._food_bag

    @property
    def boards(self):
        """gets the player's boards

        :returns: boards
        :rtype: list of Species
        """

        return self._boards

    @property
    def score(self):
        """gets the player's current score

        A player’s score is the total of:
            - food tokens in the food bag
            - populations of his existing species
            - number of trait cards associated with these species

        :returns: score
        :rtype: int
        """

        return (self._food_bag +
                sum(s.population for s in self._boards) +
                sum(len(s.traits) for s in self._boards))

    def add_board(self, board):
        """adds a species board to the player's species

        a player adds new species (boards) at either end
        the order remains fixed and matters for some of the species traits

        :param board: board to add
        :type board: Species
        """

        raise NotImplementedError

    def add_cards(self, cards):
        """adds the cards to a player's cards

        :param cards: new cards
        :type cards: list of Trait
        """

        self._cards.extend(cards)

    def add_tokens(self, which_species, num_tokens):
        """gives tokens to a species

        :param which_species: index of the species to give tokens to
        :type which_species: int

        :param num_tokens: number of tokens to add
        :type num_tokens: int
        """

        species = self._boards[which_species]
        species.food_supply += num_tokens

        if species.food_supply > species.max_food_supply:
            species.food_supply = species.max_food_supply

    def remove_population(self, which_species, population_lost):
        """removes population from a species

        :param which_species: index of the species that was attacked
        :type which_species: int

        :param population_lost: number of population lost
        :type population_lost: int
        """

        species = self._boards[which_species]
        species.population -= population_lost

        if species.population <= 0:
            del self._boards[which_species]

    def move_cards_to_boards(self, opponents):
        """tells the player to move cards to its boards if desired

        :param opponents: opponents' states
        :type opponents: list of BasePlayer
        """

        raise NotImplementedError

    def trade_cards_for_boards(self, opponents):
        """trades cards for additional species boards if desired

        player must remove its own cards

        :param opponents: opponents' states
        :type opponents: list of BasePlayer

        :returns: number of cards to trade for boards
        :rtype: int
        """

        raise NotImplementedError

    def trade_cards_for_body_size(self, opponents):
        """tells the player to trade cards for increased body size if desired

        :param opponents: opponents' states
        :type opponents: list of BasePlayer
        """

        raise NotImplementedError

    def trade_cards_for_population(self, opponents):
        """tells the player to trade cards for increased population

        :param opponents: opponents' states
        :type opponents: list of BasePlayer
        """

        raise NotImplementedError

    def cards_flipped(self):
        """tells the player cards have been flipped"""

        raise NotImplementedError

    def next_species_to_feed(self, watering_hole, opponents):
        """determines a player’s next species to be fed

        :param watering_hole: tokens left in the watering hole
        :type watering_hole: int

        :param opponents: opponents
        :type opponents: list of BasePlayer

        :returns: player's feeding choice
        :rtype: FeedingResult
        """

        raise NotImplementedError

    def turn_is_over(self):
        """tells the player that the turn is over"""

        for species in self._boards:
            self._food_bag += species.food_supply
            species.food_supply = 0
