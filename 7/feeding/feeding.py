from collections import namedtuple

from feeding.attack import is_attackable
from feeding.player import BasePlayer
from feeding.result import (
    CarnivoreResult, FatTissueResult, NoFeedingResult, VegetarianResult)
from feeding.situation import Situation
from feeding.trait import FatTissueTrait
from feeding.utils import max_order_preserving, sorted_with_default


"""
A JSONFeeding is [JSONPlayer, Natural+, LOP]. The natural number in the
middle specifies how many tokens of food are left at the watering hole.
"""


class Feeding(namedtuple('Feeding', ['player', 'watering_hole', 'opponents'])):
    """represents a feeding

    :attr player: player that is feeding
    :type player: Player

    :attr watering_hole: number of tokens remaining in the watering hole
    :type watering_hole: int

    :attr opponents: opponents of the player that is feeding
    :type opponents: list of Player
    """

    MIN_PLAYERS = 3
    MAX_PLAYERS = 8

    MIN_OPPONENTS = MIN_PLAYERS - 1
    MAX_OPPONENTS = MAX_PLAYERS - 1

    MIN_WATERING_HOLE = 0
    MAX_WATERING_HOLE = float('inf')

    def __new__(cls, player, watering_hole, opponents):
        """creates a Feeding

        :param player: player that is feeding
        :type player: Player

        :param watering_hole: number of tokens remaining in the watering hole
        :type watering_hole: int

        :param opponents: opponents of the player that is feeding
        :type opponents: list of Player
        """

        is_valid_watering_hole = (
            isinstance(watering_hole, int) and
            cls.MIN_WATERING_HOLE <= watering_hole <= cls.MAX_WATERING_HOLE)

        if not is_valid_watering_hole:
            raise ValueError('invalid watering hole')

        if not (isinstance(opponents, list) and
                cls.MIN_OPPONENTS <= len(opponents) <= cls.MAX_OPPONENTS):
            raise ValueError('invalid opponents')

        opponent_ids = [opp.player_id for opp in opponents]
        if (player.player_id in opponent_ids or
                len(opponent_ids) != len(set(opponent_ids))):
            raise ValueError('invalid duplicate players')

        return super().__new__(cls, player, watering_hole, opponents)

    @classmethod
    def from_json(cls, json_feeding):
        """creates a Feeding from a JSON representation

        :param json_feedingt: JSON feeding
        :type json_feeding: JSONFeeding

        :returns: feeding
        :rtype: Feeding
        """

        if not isinstance(json_feeding, list):
            raise ValueError('json_feeding must be a list')

        [json_player, watering_hole, json_opponents] = json_feeding

        if not isinstance(json_opponents, list):
            raise ValueError('invalid opponents')

        player = Player.from_json(json_player)
        opponents = [
            Player.from_json(json_opponent)
            for json_opponent in json_opponents
        ]

        return cls(player, watering_hole, opponents)

    def to_json(self):
        """creates a JSON representation of the feeding

        :returns: JSON feeding
        :rtype: JSONFeeding
        """

        return [
            self.player.to_json(),
            self.watering_hole,
            [opponent.to_json() for opponent in self.opponents],
        ]


def get_feeding_result(feeding):
    """gets the result of a feeding

    :param feeding: feeding to evaluate
    :type feeding: Feeding

    :returns: result of the feeding
    :rtype: FeedingResult
    """

    player, opponents, watering_hole = feeding
    return player.next_species_to_feed(opponents, watering_hole)


class Player(BasePlayer):
    """implementation of a player"""

    def next_species_to_feed(self, watering_hole, opponents):
        """chooses the next species to feed

        uses the strategy specified in assignment 6
        """

        hungry_boards = [
            species for species in self.boards
            if species.is_hungry()
        ]

        fat_tissue_result = self._next_fat_tissue_to_feed(
            hungry_boards, watering_hole)
        if fat_tissue_result is not None:
            return fat_tissue_result

        vegetarian_result = self._next_vegetarian_to_feed(hungry_boards)
        if vegetarian_result is not None:
            return vegetarian_result

        carnivore_result = self._next_carnivore_to_feed(
            hungry_boards, opponents)
        if carnivore_result is not None:
            return carnivore_result

        return NoFeedingResult()

    @staticmethod
    def _next_fat_tissue_to_feed(hungry_boards, watering_hole):
        """gets a player’s next species to feed that has fat tissue if any

        :param hungry_boards: boards
        :type hungry_boards: list of Species

        :param watering_hole: tokens left in the watering hole
        :type watering_hole: int

        :returns: fat tissue result or None if not found
        :rtype: FatTissueResult or None
        """

        def get_fat_tissue_food(species):
            """gets the food stored on the fat tissue trait

            :param species: species to get fat tissue need for
            :type species: Species

            :returns: fat food
            :rtype: int
            """

            return species.get_trait(FatTissueTrait).get_fat_food()

        def get_fat_tissue_need(species):
            """gets the fat tissue need of the species

            :param species: species to get fat tissue need for
            :type species: Species

            :returns: fat tissue need
            :rtype: int
            """

            return species.body_size - get_fat_tissue_food(species)

        selected_species = None
        need = None

        fat_tissue_boards_needs = [
            (species, get_fat_tissue_need(species))
            for species in hungry_boards
            if (species.has_trait(FatTissueTrait) and
                get_fat_tissue_need(species) > 0)
        ]

        if not fat_tissue_boards_needs:
            return None

        if len(fat_tissue_boards_needs) == 1:
            selected_species, need = fat_tissue_boards_needs[0]
        else:
            selected_species, need = max(
                fat_tissue_boards_needs,
                key=lambda species_need: species_need[1])

        if selected_species is not None:
            return FatTissueResult(
                selected_species,
                min(need, watering_hole))

        return None

    @staticmethod
    def _next_vegetarian_to_feed(hungry_boards):
        """gets a player’s next species to feed that is vegetarian if any

        chooses based on lexicographic order

        if two species have the same lexicographic order, returns the first
        in the board order

        :param hungry_boards: boards
        :type hungry_boards: list of Species

        :returns: vegetarian result or None if not found
        :rtype: VegetarianResult or None
        """

        vegetarian_boards = [
            s for s in hungry_boards
            if not s.is_carnivore()
        ]

        if not vegetarian_boards:
            return None

        max_species = max_order_preserving(vegetarian_boards)
        return VegetarianResult(max_species)

    @classmethod
    def _next_carnivore_to_feed(cls, hungry_boards, opponents):
        """gets a player’s next species to feed that is carnivore if any

        chooses based on lexicographic order

        if two species have the same lexicographic order, returns the first
        in the board order

        :param hungry_boards: species that are hungry
        :type hungry_boards: list of Species

        :param opponents: opponent players
        :type opponents: list of BasePlayer

        :returns: carnivore result or None if not found
        :rtype: carnivoreResult or None
        """

        carnivore_boards = [
            species
            for species in hungry_boards
            if species.is_carnivore()
        ]

        if not carnivore_boards:
            return None

        board_opponent_pairs = (
            (species, opponent)
            for opponent in opponents
            for i, species in enumerate(opponent.boards)
        )

        return cls._choose_attack(carnivore_boards, board_opponent_pairs)

    @staticmethod
    def _choose_attack(attacker_boards, defender_opponent_pairs):
        """chooses the best species to attack

        :param attacker_boards: choices to attack
        :type attacker_boards: list of Species

        :param defender_opponent_pairs: species and its owner
        :type defender_opponent_pairs: list of (Species, BasePlayer)

        :returns: species to attack if any are attackable
        :rtype: CarnivoreResult or None
        """

        sorted_attacker_boards = sorted_with_default(
            attacker_boards, range(len(attacker_boards)))

        sorted_boards_opponents = sorted(
            defender_opponent_pairs,
            key=lambda species_opponent: species_opponent[0],
            reverse=True)

        for attacker in sorted_attacker_boards:
            for defender, opponent in sorted_boards_opponents:
                left, right = opponent.get_neighbors(defender)
                situation = Situation(defender, attacker, left, right)

                if is_attackable(situation):
                    return CarnivoreResult(attacker, opponent, defender)

        return None
