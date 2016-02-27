from collections import namedtuple

"""
a JSONFeedingResult is one of:
    - JSONFatTissueResult
    - JSONVegetarianResult
    - JSONCarnivoreResult
    - JSONNoFeedingResult

 SpeciesIndex is a Natural representing the index of a species
 PlayerIndex is a Natural representing the index of a player
 FoodTokens is a Nat representing a number of food tokens

 JSONFatTissueResult is a [SpeciesIndex, FoodTokens]
 JSONVegetarianResult is a SpeciesIndex
 JSONCarnivoreResult is a [SpeciesIndex, PlayerIndex, SpeciesIndex]
 JSONNoFeedingResult is false

a FeedingResult is one of:
    - FatTissueResult
    - VegetarianResult
    - CarnivoreResult
    - NoFeedingResult
    - None (if feeding is not possible)
"""


class FatTissueResult(
        namedtuple('FatTissueResult', ['species', 'num_tokens'])):
    """implements a FatTissueResult

    :attr species: species index
    :type species: int

    :attr num_tokens: number of tokens requested
    :type num_tokens: int
    """

    def __eq__(self, other):
        return (self.species == other.species and
                self.num_tokens == other.num_tokens)

    def to_json(self):
        """creates a JSON representation of the result

        :returns: [species, num tokens asked for]
        :rtype: JSONFatTissueResult
        """

        return [self.species, self.num_tokens]


class VegetarianResult(namedtuple('VegetarianResult', ['species'])):
    """implements a VegetarianResult

    :attr species: species index
    :type species: int
    """

    def __eq__(self, other):
        return self.species == other.species

    def to_json(self):
        """creates a JSON representation of the result

        :returns: [species]
        :rtype: JSONVegetarianResult
        """

        return [self.species]


class CarnivoreResult(
        namedtuple('CarnivoreResult', ['species', 'player', 'to_attack'])):
    """implements a CarnivoreResult

    :attr species: species attacking index
    :type species: int

    :attr player: player to attack index
    :type player: int

    :attr to_attack: species defending index
    :type to_attack: int
    """

    def __eq__(self, other):
        return (self.species == other.species and
                self.player == other.player and
                self.to_attack == other.to_attack)

    def to_json(self):
        """creates a JSON representation of the result

        :returns: [attacker species, player to attack, species to attack]
        :rtype: JSONCarnivoreResult
        """

        return [self.species, self.player, self.to_attack]


class NoFeedingResult:
    """implements a NoFeedingResult"""

    def to_json(self):
        """creates a JSON representation of the result

        :returns: False
        :rtype: JSONNoFeedingResult
        """

        return False
