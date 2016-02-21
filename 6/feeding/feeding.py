from collections import namedtuple

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


def get_feeding_result(feeding):
    """gets the result of a feeding

    :param feeding: feeding to evaluate
    :type feeding: Feeding

    :returns: result of the feeding
    :rtype: FeedingResult
    """

    player, opponents, watering_hole = feeding
    return player.next_species_to_feed(opponents, watering_hole)
