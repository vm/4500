from collections import namedtuple

"""
a FeedingResult is one of:
    - FatTissueResult
    - VegetarianResult
    - CarnivoreResult
    - None (indicates player does not wish to feed)
"""


class FatTissueResult(
        namedtuple('FatTissueResult', ['species', 'num_tokens'])):
    """implements a FatTissueResult

    :attr species: species
    :type species: Species

    :attr num_tokens: number of tokens requested
    :type num_tokens: int
    """

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.species == other.species and
                self.num_tokens == other.num_tokens)

    def to_json(self):
        """creates a JSON representation of the result

        :returns: [species, num tokens asked for]
        :rtype: [Species+, Nat]
        """

        return [self.species.to_json(), self.num_tokens]


class VegetarianResult(namedtuple('VegetarianResult', ['species'])):
    """implements a VegetarianResult

    :attr species: species
    :type species: Species
    """

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.species == other.species)

    def to_json(self):
        """creates a JSON representation of the result

        :returns: [species]
        :rtype: [Species+]
        """

        return [self.species.to_json()]


class CarnivoreResult(
        namedtuple('CarnivoreResult', ['species', 'player', 'to_attack'])):
    """implements a CarnivoreResult

    :attr species: species attacking
    :type species: Species

    :attr player: player to attack
    :type player: BasePlayer

    :attr to_attack: species defending
    :type to_attack: Species
    """

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.species == other.species and
                self.player == other.player and
                self.to_attack == other.to_attack)

    def to_json(self):
        """creates a JSON representation of the result

        :returns: [attacker species, player to attack, species to attack]
        :rtype: [Species+, Player, Species+]
        """

        return [self.species.to_json(), self.player.to_json(),
                self.to_attack.to_json()]


class NoFeedingResult:
    """implements a NoFeedingResult"""

    def to_json(self):
        """creates a JSON representation of the result

        :returns: False
        :rtype: bool
        """

        return False
