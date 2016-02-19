from feeding.situation import Situation, Role


def is_attackable(situation):
    """determines if the attacker in a situation can attack a defender

    :param situation: situation to evaluate
    :type situation: Situation

    :returns: whether defender is attackable by attacker
    :rtype: bool
    """

    attacker, defender, left_neighbor, right_neighbor = situation

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

    return not any([attacker_prevents,
                    defender_prevents,
                    left_neighbor_prevents,
                    right_neighbor_prevents])
