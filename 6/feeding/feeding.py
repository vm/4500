from collections import namedtuple

from feeding.player import BasePlayer
from feeding.trait import FatTissueTrait


Feeding = namedtuple('Feeding', ['player', 'watering_hole', 'opponents'])
"""represents a feeding

:param player: player that is feeding
:type player: Player

:param watering_hole: number of tokens remaining in the watering hole
:type watering_hole: int

:param opponents: opponents of the player that is feeding
:type opponents: list of Player
"""


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
        hungry_boards = [s for s in self.boards if s.is_hungry())]

        fat_tissue_result = self._next_fat_tissue_to_feed(hungry_boards)
        if fat_tissue_result is not None:
            return fat_tissue_result

        vegetarian_result = self._next_vegetarian_to_feed(hungry_boards)
        if vegetarian_result is not None:
            return vegetarian_result

        carnivore_result = self._next_carnivore_to_feed(hungry_boards)
        if carnivore_result is not None:
            return carnivore_result

        return NoFeedingResult()

    @staticmethod
    def _next_fat_tissue_to_feed(hungry_boards):
        """gets a player’s next species to feed that has fat tissue if any

        :param hungry_boards: boards that are hungry
        :type hungry_boards: list of Species

        :returns: fat tissue result or None if not found
        :rtype: FatTissueResult or None
        """

        hungry_los_with_fat_tissue = [
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
            sorted_boards_by_need = reversed(sorted(
                hungry_boards, get_fat_tissue_need))

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
                selected_species, get_fat_tissue_need(selected_species))

        return None

    @staticmethod
    def _next_vegetarian_to_feed(hungry_species):
        """gets a player’s next species to feed that is vegetarian if any

        :param hungry_species: species that are hungry
        :type hungry_species: list of Species

        :returns: vegetarian result or None if not found
        :rtype: VegetarianResult or None
        """

        vegetarian_species = [
            s for s in hungry_species
            if not s.is_carnivore()
        ]

        if not vegetarian_species:
            return None

        return max(vegetarian_species)

    def select_attack(self, opponents):
        raise NotImplementedError


def get_feeding_result(feeding):
    """gets the result of a feeding

    :param feeding: feeding to evaluate
    :type feeding: Feeding

    :returns: result of the feeding
    :rtype: FeedingResult
    """

    player, opponents, watering_hole = feeding
    return player.next_species_to_feed(opponents, watering_hole)
