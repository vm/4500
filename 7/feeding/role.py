from enum import Enum


class Role(Enum):
    """represents roles in a Situation"""

    defender = 'defender',
    attacker = 'attacker',
    left_neighbor = 'left_neighbor',
    right_neighbor = 'right_neighbor'
