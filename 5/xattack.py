import sys

from attack import is_attackable
from species import Species
from trait import trait_name_to_class

"""
A Situation is [JSONSpecies, JSONSpecies, OptJSONSpecies, OptJSONSpecies].

A JSONSpecies is
    [["food",Nat],
     ["body",Nat],
     ["population",Nat],
     ["traits",LOT]]

A LOT is one of:
    []
    [JSONTrait]
    [JSONTrait, JSONTrait]
    [JSONTrait, JSONTrait, JSONTrait]

An OptJSONSpecies is one of:
    false
    Species

A JSONTrait is one of:
    "carnivore", "ambush", "burrowing", "climbing", "cooperation", "fat-tissue",
    "fertile", "foraging", "hard-shell", "herding", "horns", "long-neck",
    "pack-hunting", "scavenger", "symbiosis", or "warning-call".

A Nat is a JSON number interpretable as a natural number between 0 and 7
(inclusive).
"""

def main():
    situation_json = json.load(sys.stdin)
    [
        attacker,
        defender,
        left_neighbor,
        right_neighbor
    ] = convert_situation(situation_json)

    return is_attackable(attacker, defender, left_neighbor, right_neighbor)


def convert_situation(json_situation):
    """
    :param json_situation:
    :type json_situation: Situation

    :returns:
    :rtype: list of Species
    """

    return map(convert_species, situation)


def convert_species(json_species):
    """
    :param json_species: JSON representation of species
    :type json_species: JSONSpecies

    :returns: internal representation of species
    :rtype: Species
    """

    if not json_species:
        return None

    [[_, food], [_, body], [_, population], [_, traits]] = json_species
    converted_traits = map(convert_trait, traits)

    return Species(food, body, population, converted_traits)


def convert_trait(json_trait):
    """
    :param json_trait: JSON representation of trait
    :type json_trait: JSONTrait

    :returns: internal representation of trat
    :rtype: Trait
    """

    default_tokens = 0

    TraitClass = trait_name_to_class[json_trait]
    return TraitClass(default_tokens)


if __name__ == '__main__':
    main()
