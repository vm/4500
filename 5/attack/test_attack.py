import pytest

from attack.attack import is_attackable
from attack.trait import Trait, trait_name_to_class
from attack.situation import Species

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

    result = case['result']
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
        trait_names = json_species['traits']
        species.traits = [
            trait_name_to_class[name](num_tokens)
            for name in trait_names
        ]

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
                'traits': ['carnivore', 'ambush']
            },
            'defender': {
                'traits': ['warning-call']
            },
            'result': True
        },
        {
            'attacker': {
                'traits': ['carnivore', 'ambush']
            },
            'defender': {},
            'left_neighbor': {
                'traits': ['warning-call']
            },
            'result': True
        },
        {
            'attacker': {
                'traits': ['carnivore', 'ambush']
            },
            'defender': {},
            'right_neighbor': {
                'traits': ['warning-call']
            },
            'result': True
        },
    ]

    for case in cases:
        assert_case(case)


def test_burrowing():
    """tests the Burrowing trait"""

    cases = [
        {
            'attacker': {
                'traits': ['carnivore']
            },
            'defender': {
                'traits': ['burrowing'],
                'population': 4,
                'food_supply': 4,
            },
            'result': False,
        },
        {
            'attacker': {
                'traits': ['carnivore']
            },
            'defender': {
                'traits': ['burrowing'],
                'population': 4,
                'food_supply': 0,
            },
            'result': True,
        }
    ]

    for case in cases:
        assert_case(case)


def test_climbing():
    """tests the Climbing trait"""

    cases = [
        {
            'attacker': {
                'traits': ['carnivore']
            },
            'defender': {
                'traits': ['climbing'],
            },
            'result': False,
        },
        {
            'attacker': {
                'traits': ['carnivore', 'climbing']
            },
            'defender': {
                'traits': ['climbing'],
            },
            'result': True,
        },
    ]

    for case in cases:
        assert_case(case)


def test_hard_shell():
    """tests the Hard Shell trait"""

    cases = [
        {
            'attacker': {
                'traits': ['carnivore'],
                'body_size': 4,
            },
            'defender': {
                'traits': ['hard-shell'],
                'body_size': 1,
            },
            'result': False,
        },
        {
            'attacker': {
                'traits': ['carnivore'],
                'body_size': 5,
            },
            'defender': {
                'traits': ['hard-shell'],
                'body_size': 1,
            },
            'result': True,
        },
    ]

    for case in cases:
        assert_case(case)


def test_herding():
    """tests the Herding trait"""

    cases = [
        {
            'attacker': {
                'traits': ['carnivore'],
                'population': 3,
            },
            'defender': {
                'traits': ['herding'],
                'population': 4,
            },
            'result': False,
        },
        {
            'attacker': {
                'traits': ['carnivore'],
                'population': 4,
            },
            'defender': {
                'traits': ['herding'],
                'population': 4,
            },
            'result': False,
        },
        {
            'attacker': {
                'traits': ['carnivore'],
                'population': 5,
            },
            'defender': {
                'traits': ['herding'],
                'population': 4,
            },
            'result': True,
        },
    ]

    for case in cases:
        assert_case(case)


def test_pack_hunting():
    """tests the Pack Hunting trait"""

    cases = [
        {
            'attacker': {
                'traits': ['carnivore', 'pack-hunting'],
                'body_size': 4,
                'population': 1,
            },
            'defender': {
                'traits': ['hard-shell'],
                'body_size': 1,
            },
            'result': True,
        },
        {
            'attacker': {
                'traits': ['carnivore', 'pack-hunting'],
                'body_size': 3,
                'population': 1,
            },
            'defender': {
                'traits': ['hard-shell'],
                'body_size': 1,
            },
            'result': False,
        },
    ]

    for case in cases:
        assert_case(case)


def test_symbiosis():
    """tests the Symbiosis trait"""

    cases = [
        {
            'attacker': {
                'traits': ['carnivore'],
            },
            'defender': {
                'traits': ['symbiosis'],
                'body_size': 2,
            },
            'right_neighbor': {
                'body_size': 4,
            },
            'result': False,
        },
        {
            'attacker': {
                'traits': ['carnivore'],
            },
            'defender': {
                'traits': ['symbiosis'],
                'body_size': 6,
            },
            'right_neighbor': {
                'body_size': 4,
            },
            'result': True,
        },
        {
            'attacker': {
                'traits': ['carnivore'],
            },
            'defender': {
                'traits': ['symbiosis'],
                'body_size': 2,
            },
            'left_neighbor': {
                'body_size': 4,
            },
            'result': True,
        },
        {
            'attacker': {
                'traits': ['carnivore'],
            },
            'defender': {
                'traits': ['symbiosis'],
                'body_size': 2,
            },
            'left_neighbor': {
                'body_size': 4,
            },
            'result': True,
        },
        {
            'attacker': {
                'traits': ['carnivore'],
            },
            'defender': {
                'traits': ['symbiosis'],
                'body_size': 6,
            },
            'left_neighbor': {
                'body_size': 4,
            },
            'result': True,
        },
    ]

    for case in cases:
        assert_case(case)


def test_warning_call():
    """tests the Warning Call trait"""

    cases = [
        {
            'attacker': {
                'traits': ['carnivore'],
            },
            'defender': {
                'traits': ['warning-call'],
            },
            'result': True,
        },
        {
            'attacker': {
                'traits': ['carnivore'],
            },
            'defender': {},
            'left_neighbor': {
                'traits': ['warning-call'],
            },
            'result': False,
        },
        {
            'attacker': {
                'traits': ['carnivore'],
            },
            'defender': {},
            'right_neighbor': {
                'traits': ['warning-call'],
            },
            'result': False,
        },
    ]

    for case in cases:
        assert_case(case)
