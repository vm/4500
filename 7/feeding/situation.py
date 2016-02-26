from collections import namedtuple
from enum import Enum


class Situation(namedtuple(
        'Situation',
        ['defender', 'attacker', 'left_neighbor', 'right_neighbor'])):
    """represents a situation in the Evolution game

    :param defender: defender
    :type defender: Species

    :param attacker: attacker
    :type attacker: Species

    :param left_neighbor: left_neighbor
    :type left_neighbor: Species or None

    :param right_neighbor: right_neighbor
    :type right_neighbor: Species or None
    """

    @classmethod
    def from_json(cls, json_situation):
        """creates a Situation from a JSON representation

        :param json_situation: JSON situation
        :type json_situation: JSONSituation

        :returns: situation
        :rtype: Situation
        """

        if isinstance(json_situation, list) and len(json_situation) == 4:
            [
                json_defender,
                json_attacker,
                json_left_neighbor,
                json_right_neighbor
            ] = json_situation

            defender = Species.from_json(json_defender)
            attacker = Species.from_json(json_attacker)
            left_neighbor = Species.from_json(json_left_neighbor)
            right_neighbor = Species.from_json(json_right_neighbor)

            return cls(defender, attacker, left_neighbor, right_neighbor)
        else:
            raise ValueError('not a valid json situation')


class Role(Enum):
    """represents roles in a Situation"""

    defender = 'defender',
    attacker = 'attacker',
    left_neighbor = 'left_neighbor',
    right_neighbor = 'right_neighbor'
