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

    mod_attacker = modify_with_traits(attacker.copy(), Role.attacker)
    mod_defender = modify_with_traits(defender.copy(), Role.defender)

    situation = Situation(
        mod_attacker, mod_defender, left_neighbor, right_neighbor)

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


def modify_with_traits(species, is_attacking):
    """modifies the species with the modify function of each species trait

    :param species: species to modify
    :type species: Species

    :param is_attacking: whether the species is attacking
    :type is_attacking: bool

    :returns: modified species
    :rtype: Species
    """

    for trait in species.traits:
        species = trait.modify(species, is_attacking)
    return species
