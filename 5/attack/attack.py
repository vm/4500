from attack.situation import Situation, Role


def is_attackable(attacker, defender, left_neighbor=None, right_neighbor=None):
    """determines if a species is attackable

    :param attacker: species doing the attacking
    :type attacker: Species

    :param defender: species being attacked
    :type defender: Species

    :param left_neighbor: left neighbor of the defending species
    :type left_neighbor: Species or None

    :param right_neighbor: right neighbor of the defending species
    :type right_neighbor: Species or None

    :returns: whether defender is attackable by attacker
    :rtype: bool
    """

    if not attacker.is_carnivore:
        raise ValueError('attacker must be a carnivore')

    mut_attacker = attacker.copy()
    mut_attacker.apply_traits(Role.attacker)

    mut_defender = defender.copy()
    mut_defender.apply_traits(Role.defender)

    situation = Situation(
        mut_attacker, mut_defender, left_neighbor, right_neighbor)

    attacker_prevents = attacker.prevents_attack(situation, Role.attacker)
    defender_prevents = defender.prevents_attack(situation, Role.defender)

    if left_neighbor:
        left_neighbor_prevents = left_neighbor.prevents_attack(
            situation, Role.left_neighbor)
    else:
        left_neighbor_prevents = False

    if right_neighbor:
        right_neighbor_prevents = right_neighbor.prevents_attack(
            situation, Role.right_neighbor)
    else:
        right_neighbor_prevents = False

    return not (attacker_prevents or
                defender_prevents or
                left_neighbor_prevents or
                right_neighbor_prevents)
