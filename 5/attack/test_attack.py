import pytest

from attack import Species, TraitCard, TraitKind, is_attackable

"""
TODO

multiple of each trait that counter eachother
ex: 2 warning call, 1 ambush
"""

def test_not_carnivore():
    """tests that an error is raised when the attacker is not a carnivore"""

    attacker = Species()
    defender = Species()

    with pytest.raises(ValueError):
        is_attackable(attacker, defender, None, None)

def assert_case(case):
    """checks cases for attacker, defender, and neighbors return result

    :param case: JSON defining a case
    :type case: dict
    """

    result = cases['result']
    attacker = json_to_species(case['attacker'])
    defender = json_to_species(case['defender'])

    left_neighbor = json_to_species(case.get('left_neighbor'))
    right_neighbor = json_to_species(case.get('right_neighbor'))

    assert is_attackable(
        attacker, defender, left_neighbor, right_neighbor) is result


def json_to_species(json_species):
    """turns a JSON representation of a species in to a species object"""

    if json_species is None:
        return None

    species = Species()

    if 'traits' in json_species:
        num_tokens = 0
        trait_kinds = json_species['traits']

        species.traits = [TraitCard(tk, num_tokens) for tk in trait_kinds]

    species.body_size = json_species.get(
        'body_size', Species.DEFAULT_BODY_SIZE)
    species.population = json_species.get(
        'population', Species.DEFAULT_POPULATION)
    species.food_supply = json_species.get(
        'food_supply', Species.DEFAULT_FOOD_SUPPLY)

    return species

def test_ambush():
    """tests the Ambust trait"""

    cases = [
        {
            'attacker': {
                'traits': ['CARNIVORE', 'AMBUSH']
            },
            'defender': {
                'traits': ['WARNING_CALL']
            },
            'result': True
        },
        {
            'attacker': {
                'traits': ['CARNIVORE', 'AMBUSH']
            },
            'defender': {},
            'left_neighbor': {
                'traits': ['WARNING_CALL']
            },
            'result': True
        },
        {
            'attacker': {
                'traits': ['CARNIVORE', 'AMBUSH']
            },
            'defender': {},
            'right_neighbor': {
                'traits': ['WARNING_CALL']
            },
            'result': True
        },
    ]

    for case in cases:
        assert_case(case)


def test_burrowing():
    """tests the Burrowing trait

    cases:
        attacker:
            traits: [Carnivore]
        defender:
            traits: [Burrowing]
            population: 4
            food_supply: 4
        left_neighbor: none
        right_neighbor: none
        result: false

        attacker:
            traits: [Carnivore]
        defender:
            traits: [Burrowing]
            population: 4
            food_supply: 0
        left_neighbor: none
        right_neighbor: none
        result: true
    """

    raise NotImplementedError()

def test_climbing():
    """tests the Climbing trait

    cases:
        attacker:
            traits: [Carnivore]
        defender:
            traits: [Climbing]
        result: false

        attacker:
            traits: [Carnivore, Climbing]
        defender:
            traits: [Climbing]
        result: true
    """

    raise NotImplementedError()

def test_hard_shell():
    """tests the Hard Shell trait

    cases:
        attacker:
            traits: [Carnivore]
            body_size: 4
        defender:
            traits: [Hard Shell]
            body_size: 1
        result: false

        attacker:
            traits: [Carnivore]
            body_size: 5
        defender:
            traits: [Hard Shell]
            body_size: 1
        result: true
    """

    raise NotImplementedError()

def test_herding():
    """tests the Herding trait

    cases:
        attacker:
            traits: [Carnivore]
            population: 3
        defender:
            traits: [Herding]
            population: 4
        result: false

        attacker:
            traits: [Carnivore]
            population: 4
        defender:
            traits: [Herding]
            population: 4
        result: false

        attacker:
            traits: [Carnivore]
            population: 5
        defender:
            traits: [Herding]
            population: 4
        result: true
    """

    raise NotImplementedError()

def test_pack_hunting():
    """tests the Pack Hunting trait

    cases:
        attacker:
            traits: [Carnivore, Pack Hunting]
            body_size: 4
            population: 1
        defender:
            traits: [Hard Shell]
            body_size: 1
        result: true

        attacker:
            traits: [Carnivore, Pack Hunting]
            body_size: 3
            population: 1
        defender:
            traits: [Hard Shell]
            body_size: 1
        result: false
    """

    raise NotImplementedError()

def test_symbiosis():
    """tests the Symbiosis trait

    cases:
        attacker:
            traits: [Carnivore]
        defender:
            body_size: 2
            traits: [Symbiosis]
        right_neighbor:
            body_size: 4
        result: false

        attacker:
            traits: [Carnivore]
        defender:
            body_size: 6
            traits: [Symbiosis]
        right_neighbor:
            body_size: 4
        result: true

        attacker:
            traits: [Carnivore]
        defender:
            body_size: 2
            traits: [Symbiosis]
        left_neighbor:
            body_size: 4
        result: true

        attacker:
            traits: [Carnivore]
        defender:
            body_size: 6
            traits: [Symbiosis]
        left_neighbor:
            body_size: 4
        result: true
    """

    raise NotImplementedError()

def test_warning_call():
    """tests the Warning Call trait

    cases:
        attacker:
            traits: [Carnivore]
        defender:
            traits: [Warning Call]
        result: true

        attacker:
            traits: [Carnivore]
        defender:
        left_neighbor:
            traits: [Warning Call]
        result: false

        attacker:
            traits: [Carnivore]
        defender:
        right_neighbor:
            traits: [Warning Call]
        result: false
    """

    raise NotImplementedError()
