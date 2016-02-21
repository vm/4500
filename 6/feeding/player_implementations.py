from feeding.attack import is_attackable
from feeding.player import BasePlayer
from feeding.result import (
    CarnivoreResult, FatTissueResult, NoFeedingResult, VegetarianResult)
from feeding.situation import Situation
from feeding.trait import FatTissueTrait
from feeding.utils import (
    get_or_else, max_order_preserving, sorted_with_default)


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
            if species.has_trait(FatTissueTrait) and
                get_fat_tissue_need(species) > 0
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

    @staticmethod
    def _next_carnivore_to_feed(hungry_boards, opponents):
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

        sorted_attacker_boards = sorted_with_default(
            carnivore_boards, range(len(carnivore_boards)))

        boards_opponents = (
            (species, opponent)
            for opponent in opponents
            for i, species in enumerate(opponent.boards)
        )

        sorted_boards_opponents = sorted(
            boards_opponents,
            key=lambda species_opponent: species_opponent[0],
            reverse=True)

        for attacker in sorted_attacker_boards:
            for defender, opponent in sorted_boards_opponents:

                defender_index = opponent.boards.index(defender)
                left_neighbor = get_or_else(opponent.boards, defender_index-1)
                right_neighbor = get_or_else(opponent.boards, defender_index+1)

                situation = Situation(
                    attacker, defender, left_neighbor, right_neighbor)

                if is_attackable(situation):
                    return CarnivoreResult(attacker, opponent, defender)

        return None
