from feeding.attack import is_attackable
from feeding.player import BasePlayer
from feeding.result import (
    CarnivoreResult, FatTissueResult, NoFeedingResult, VegetarianResult)
from feeding.situation import Situation
from feeding.trait import FatTissueTrait
from feeding.utils import get_or_else, max_order_preserving


class Player(BasePlayer):
    """implementation of a player"""

    def add_board(self, board):
        raise NotImplementedError

    def move_cards_to_boards(self, opponents):
        raise NotImplementedError

    def trade_cards_for_boards(self, opponents):
        raise NotImplementedError

    def trade_cards_for_body_size(self, opponents):
        raise NotImplementedError

    def trade_cards_for_population(self, opponents):
        raise NotImplementedError

    def cards_flipped(self):
        raise NotImplementedError

    def next_species_to_feed(self, watering_hole, opponents):
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

        hungry_with_fat_tissue = [
            species for species in hungry_boards
            if species.has_trait(FatTissueTrait) and
                (species.get_trait(FatTissueTrait).get_fat_food() <
                 species.body_size)
        ]

        if not hungry_with_fat_tissue:
            return None

        selected_species = None
        num_with_fat_tissue = len(hungry_with_fat_tissue)

        def get_fat_tissue_need(species):
            return (species.body_size -
                    species.get_trait(FatTissueTrait).get_fat_food())

        if num_with_fat_tissue == 1:
            selected_species = hungry_with_fat_tissue[0]

        if num_with_fat_tissue > 1:
            sorted_boards_by_need = sorted(
                hungry_boards,
                key=get_fat_tissue_need,
                reverse=True)

            most_need = get_fat_tissue_need(sorted_boards_by_need[0])
            most_needy_boards = [
                species for species in sorted_boards_by_need
                if get_fat_tissue_need(species) == most_need
            ]

            selected_species = max(most_needy_boards)

        if selected_species is not None:
            fat_tissue_food = (
                selected_species.get_trait(FatTissueTrait).get_fat_food())
            return FatTissueResult(
                selected_species,
                min(get_fat_tissue_need(selected_species), watering_hole))

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

        sorted_attacker_boards = map(
            lambda index_board: index_board[1],
            sorted(
                enumerate(carnivore_boards),
                key=lambda index_board: (index_board[1], -index_board[0]),
                reverse=True))

        enumerated_boards_and_opponents = [
            (i, species, opponent)
            for opponent in opponents
            for i, species in enumerate(opponent.boards)
        ]

        sorted_defender_index_boards_opponents = sorted(
            enumerated_boards_and_opponents,
            key=lambda index_species_opponent: index_species_opponent[1],
            reverse=True)

        for attacker in sorted_attacker_boards:
            for index, defender, opponent in sorted_defender_index_boards_opponents:
                left_neighbor = get_or_else(opponent.boards, index-1)
                right_neighbor = get_or_else(opponent.boards, index+1)

                situation = Situation(
                    attacker, defender, left_neighbor, right_neighbor)

                if is_attackable(situation):
                    return CarnivoreResult(attacker, opponent, defender)

        return None

    def select_attack(self, opponents):
        raise NotImplementedError
