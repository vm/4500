from collections import namedtuple
from enum import Enum


Situation = namedtuple(
    'Situation', ['attacker', 'defender', 'left_neighbor', 'right_neighbor'])
"""represents a situation in the Evolution game

:param attacker: attacker
:type attacker: Species

:param defender: defender
:type defender: Species

:param left_neighbor: left_neighbor
:type left_neighbor: Species or None

:param right_neighbor: right_neighbor
:type right_neighbor: Species or None
"""


class Role(Enum):
    """represents roles in a Situation"""

    attacker = 'attacker',
    defender = 'defender',
    left_neighbor = 'left_neighbor',
    right_neighbor = 'right_neighbor'
