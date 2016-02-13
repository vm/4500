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

    attacker_prevents = species_prevents_attack(
        attacker, situation, Role.attacker)

    defender_prevents = species_prevents_attack(
        defender, situation, Role.defender)

    left_neighbor_prevents = species_prevents_attack(
        left_neighbor, situation, Role.left_neighbor)

    right_neighbor_prevents = species_prevents_attack(
        right_neighbor, situation, Role.right_neighbor)

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


def species_prevents_attack(species, situation, role):
    """whether a species prevents the attack in the situation

    :param species: species
    :type species: Species or None

    :param situation: situation
    :type situation: Situation

    :param role: role of the species in the situation
    :type role: Role

    :returns: whether the species prevents an attack in the situation
    :rtype: bool
    """

    if species is None:
        return False

    return any(
        trait.prevents_attack(situation, role)
        for trait in species.traits)
