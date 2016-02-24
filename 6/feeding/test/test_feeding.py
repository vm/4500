import json

import pytest

from feeding.attack import is_attackable
from feeding.feeding import Feeding, get_feeding_result, Player
from feeding.result import (
    CarnivoreResult, FatTissueResult, NoFeedingResult, VegetarianResult)
from feeding.situation import Situation
from feeding.species import Species
from feeding.trait import Trait, CarnivoreTrait, FatTissueTrait, HornsTrait


MIN_NUM_PLAYERS = 3
MAX_NUM_PLAYERS = 8


def test_invalid_json_feeding():
    """tests creating a feeding with invalid JSON

    cases:
        - not a list
        - wrong number of inputs
        - wrong input order
        - wrong types
            - player
            - watering hole
            - opponents
                - must be at least MIN_NUM_PLAYERS - 1
                - must be at most MAX_NUM_PLAYERS - 1
    """

    valid_player = Player(player_id=MAX_NUM_PLAYERS * 2).to_json()
    valid_watering_hole = 5

    valid_opponents = [
        Player(player_id=i).to_json()
        for i in range(int((MAX_NUM_PLAYERS - MIN_NUM_PLAYERS) / 2))
    ]
    invalid_few_opponents = valid_opponents[:MIN_NUM_PLAYERS-2]
    invalid_many_opponents = [
        Player(player_id=i).to_json()
        for i in range(MAX_NUM_PLAYERS)
    ]

    not_a_list = 'hi'
    with pytest.raises(ValueError):
        Feeding.from_json(not_a_list)

    wrong_number_of_inputs = ['a', 'b']
    with pytest.raises(ValueError):
        Feeding.from_json(wrong_number_of_inputs)

    wrong_input_order = [valid_player, valid_opponents, valid_watering_hole]
    with pytest.raises(ValueError):
        Feeding.from_json(wrong_input_order)

    wrong_watering_hole_type = [valid_player, '5', valid_opponents]
    with pytest.raises(ValueError):
        Feeding.from_json(wrong_watering_hole_type)

    wrong_opponents_type = [valid_player, valid_watering_hole, 'opponents']
    with pytest.raises(ValueError):
        Feeding.from_json(wrong_opponents_type)

    too_few_opponents = [
        valid_player, valid_watering_hole, invalid_few_opponents
    ]
    with pytest.raises(ValueError):
        Feeding.from_json(too_few_opponents)

    too_many_opponents = [
        valid_player, valid_watering_hole, invalid_many_opponents
    ]
    with pytest.raises(ValueError):
        Feeding.from_json(too_many_opponents)

    player_in_opponents = [
            Player(player_id=1).to_json(),
            valid_watering_hole,
            valid_opponents[:-1] + [Player(player_id=1).to_json()]
    ]
    with pytest.raises(ValueError):
        Feeding.from_json(player_in_opponents)

    duplicate_opponents = [
            valid_player,
            valid_watering_hole,
            valid_opponents[:-2] + ([Player(player_id=1).to_json()] * 2)
    ]
    with pytest.raises(ValueError):
        Feeding.from_json(duplicate_opponents)


def test_invalid_json_player():
    """tests creating a player with invalid JSON"""

    valid_id = 1
    valid_boards = []
    valid_bag = 10
    too_many_boards = ['board'] * Player.MAX_NUM_BOARDS

    invalid_player_type = 'hi'
    with pytest.raises(ValueError):
        Player.from_json(invalid_player_type)

    invalid_number_of_params = ['a', 'b']
    with pytest.raises(ValueError):
        Player.from_json(invalid_number_of_params)

    invalid_id_type = ['id', valid_boards, valid_bag]
    with pytest.raises(ValueError):
        Player.from_json(invalid_id_type)

    invalid_bag_type = [valid_id, valid_boards, 'bag']
    with pytest.raises(ValueError):
        Player.from_json(invalid_bag_type)

    invalid_id_range = [0, valid_boards, valid_bag]
    with pytest.raises(ValueError):
        Player.from_json(invalid_id_range)

    invalid_bag_range = [valid_id, valid_boards, -1]
    with pytest.raises(ValueError):
        Player.from_json(invalid_bag_range)

    invalid_number_of_boards = [valid_id, too_many_boards, valid_bag]
    with pytest.raises(ValueError):
        Player.from_json(invalid_number_of_boards)


def test_invalid_json_species():
    """tests creating a species with invalid JSON"""

    valid_food = ['food', 4]
    valid_body = ['body', 2]
    valid_population = ['population', 6]
    valid_traits = ['traits', ['fat-tissue']]
    valid_fat_tissue = ['fat-food', 5]

    invalid_species_type = 'species'
    with pytest.raises(ValueError):
        Species.from_json(invalid_species_type)

    invalid_num_params = [[], [], []]
    with pytest.raises(ValueError):
        Species.from_json(invalid_num_params)

    invalid_param_types = [valid_food, valid_body, valid_population, 5]
    with pytest.raises(ValueError):
        Species.from_json(invalid_param_types)

    invalid_fieldnames = [valid_food, valid_body, valid_population, ['hi', 5]]
    with pytest.raises(ValueError):
        Species.from_json(invalid_fieldnames)

    fat_tissue_field_without_trait = [
        valid_food,
        valid_body,
        valid_population,
        ['traits', []],
        valid_fat_tissue
    ]
    with pytest.raises(ValueError):
        Species.from_json(fat_tissue_field_without_trait)

    invalid_food = [['food', -1], valid_body, valid_population, valid_traits]
    with pytest.raises(ValueError):
        Species.from_json(invalid_food)

    invalid_body_low = [
        valid_food,
        ['body', Species.MIN_BODY_SIZE-1],
        valid_population,
        valid_traits
    ]
    with pytest.raises(ValueError):
        Species.from_json(invalid_body_low)

    invalid_body_high = [
        valid_food,
        ['body', Species.MAX_BODY_SIZE+1],
        valid_population,
        valid_traits
    ]
    with pytest.raises(ValueError):
        Species.from_json(invalid_body_high)

    invalid_population_low = [
        valid_food,
        valid_body,
        ['population', Species.MIN_POPULATION-1],
        valid_traits
    ]
    with pytest.raises(ValueError):
        Species.from_json(invalid_population_low)

    invalid_population_high = [
        valid_food,
        valid_body,
        ['population', Species.MAX_POPULATION+1],
        valid_traits
    ]
    with pytest.raises(ValueError):
        Species.from_json(invalid_population_high)

    duplicate_traits = ['traits', ['carnivore', 'carnivore']]
    invalid_duplicates = [
        valid_food,
        valid_body,
        valid_population,
        duplicate_traits
    ]
    with pytest.raises(ValueError):
        Species.from_json(invalid_duplicates)

    Species.from_json([
        valid_food,
        valid_body,
        valid_population,
        valid_traits,
    ])

def test_invalid_json_trait():
    """tests creating a trait with invalid JSON"""

    invalid_trait_type = None
    with pytest.raises(ValueError):
        Trait.from_json(invalid_trait_type)

    invalid_trait_name = 'invalid_trait_name'
    with pytest.raises(ValueError):
        Trait.from_json(invalid_trait_name)


def test_fat_tissue_single():
    """if one species has the Fat Tissue trait, it is selected"""

    selected_species = Species(
        food_supply=1,
        body_size=2,
        population=2,
        traits=[FatTissueTrait(fat_food=0)])

    my_species = [
        selected_species,
        Species(
            food_supply=1,
            body_size=2,
            population=2),
    ]

    me = Player(player_id=1, boards=my_species, food_bag=2)
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    watering_hole_tokens = 10
    opponents = [
        Player(
            player_id=2,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = FatTissueResult(selected_species, num_tokens=expected_tokens)

    assert get_feeding_result(feeding) == result


def test_fat_tissue_full_vegetarian():
    """a vegetarian species with a full Fat Tissue trait defaults to
    vegetarian behavior
    """

    selected_species = Species(
        food_supply=1,
        body_size=2,
        population=2,
        traits=[FatTissueTrait(fat_food=2)])

    my_species = [
        selected_species,
        Species(
            food_supply=1,
            body_size=2,
            population=3,
            traits=[CarnivoreTrait()]),
    ]
    me = Player(player_id=1, boards=my_species, food_bag=2)

    watering_hole_tokens = 2
    opponents = [
        Player(
            player_id=2,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = VegetarianResult(selected_species)

    assert get_feeding_result(feeding) == result


def test_fat_tissue_full_carnivore():
    """a species with a full Fat Tissue trait and a Carnivore trait
    defaults to Carnivore behavior and chooses the correct species to attack.
    in case of a multiple carnivores, chooses largest by lexicographic order.
    """

    attacking_species = Species(
        food_supply=1,
        body_size=2,
        population=4,
        traits=[FatTissueTrait(fat_food=2), CarnivoreTrait()])

    my_species = [
        attacking_species,
        Species(
            food_supply=1,
            body_size=2,
            population=3,
            traits=[CarnivoreTrait()]),
    ]
    me = Player(player_id=1, boards=my_species, food_bag=2)

    watering_hole_tokens = 10

    defending_species = Species(food_supply=1, body_size=2, population=2)
    defending_player = Player(
        player_id=2,
        boards=[defending_species],
        food_bag=2)
    opponents = [defending_player]

    situation = Situation(attacking_species, defending_species, None, None)
    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = CarnivoreResult(
        attacking_species, defending_player, defending_species)

    assert is_attackable(situation)
    assert get_feeding_result(feeding) == result


def test_hungry_carnivore_over_not_hungry_fat_tissue():
    """a hungry carnivore is chosen over a not-hungry species with the Fat
    Tissue trait
    """

    attacking_species = Species(
        food_supply=1,
        body_size=2,
        population=2,
        traits=[CarnivoreTrait()])

    my_species = [
        Species(
            food_supply=2,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=2)]),
        attacking_species,
    ]

    me = Player(player_id=1, boards=my_species, food_bag=2)

    watering_hole_tokens = 10

    defending_species = Species(
        food_supply=1,
        body_size=2,
        population=2)
    defending_player = Player(
        player_id=2,
        boards=[defending_species],
        food_bag=2)

    opponents = [defending_player]

    situation = Situation(attacking_species, defending_species, None, None)
    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = CarnivoreResult(
        attacking_species, defending_player, defending_species)

    assert is_attackable(situation)
    assert get_feeding_result(feeding) == result


def test_fat_tissue_nonzero_fat():
    """If fat tissue greater than 0 and fat tissue species chosen, tokens
    requested in the return is equal to the body size - fat tissue stored
    """

    selected_species = Species(
        food_supply=1,
        body_size=2,
        population=2,
        traits=[FatTissueTrait(fat_food=1)])

    my_species = [
        selected_species,
        Species(
            food_supply=1,
            body_size=2,
            population=3,
            traits=[CarnivoreTrait()]),
    ]
    me = Player(player_id=1, boards=my_species, food_bag=2)
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    watering_hole_tokens = 10
    opponents = [
        Player(
            player_id=3,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = FatTissueResult(selected_species, num_tokens=expected_tokens)

    assert get_feeding_result(feeding) == result


def test_fat_tissue_max_watering_hole():
    """The player asks for the number of tokens in the watering hole if it is
    less than the fat tissue can add
    """

    selected_species = Species(
        food_supply=1,
        body_size=6,
        population=2,
        traits=[FatTissueTrait(fat_food=2)])

    my_species = [
        selected_species,
        Species(
            food_supply=1,
            body_size=2,
            population=3,
            traits=[CarnivoreTrait()]),
    ]
    me = Player(player_id=1, boards=my_species, food_bag=2)

    watering_hole_tokens = 2
    expected_tokens = min((selected_species.body_size -
                           selected_species.traits[0].get_fat_food()),
                          watering_hole_tokens)

    opponents = [
        Player(
            player_id=3,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = FatTissueResult(selected_species, expected_tokens)

    assert get_feeding_result(feeding) == result


def test_fat_tissue_multiple():
    """If multiple species with fat tissue trait, default to largest fat
    tissue need
    """

    selected_species = Species(
        food_supply=1,
        body_size=2,
        population=2,
        traits=[FatTissueTrait(fat_food=0)])

    my_species = [
        Species(
            food_supply=1,
            body_size=5,
            population=2,
            traits=[FatTissueTrait(fat_food=4)]),
        selected_species
    ]

    me = Player(player_id=1, boards=my_species, food_bag=2)

    watering_hole_tokens = 10
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    opponents = [
        Player(
            player_id=2,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = FatTissueResult(selected_species, expected_tokens)

    assert get_feeding_result(feeding) == result


def test_fat_tissue_need_tie():
    """If multiple species and same fat tissue need, defaults to largest by
    lexicographic ordering
    """

    selected_species = Species(
        food_supply=1,
        body_size=3,
        population=2,
        traits=[FatTissueTrait(fat_food=1)])

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=1)]),
        selected_species,
    ]

    me = Player(player_id=1, boards=my_species, food_bag=2)

    watering_hole_tokens = 10
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    opponents = [
        Player(
            player_id=2,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = FatTissueResult(selected_species, expected_tokens)

    assert get_feeding_result(feeding) == result


def test_fat_tissue_ordering_tie():
    """If multiple species, same fat tissue need and lexicographic ordering
    tie, default to player board order
    """

    selected_species = Species(
        food_supply=1,
        body_size=2,
        population=2,
        traits=[FatTissueTrait(fat_food=1)])

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=1)]),
        selected_species,
    ]

    me = Player(player_id=1, boards=my_species, food_bag=2)

    watering_hole_tokens = 10
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    opponents = [
        Player(
            player_id=2,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = FatTissueResult(selected_species, expected_tokens)

    assert get_feeding_result(feeding) == result


def test_vegetarian_one():
    """If only one vegetarian species, it is selected"""

    selected_species = Species(
        food_supply=1,
        body_size=2,
        population=2)

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[CarnivoreTrait()]),
        selected_species,
    ]

    me = Player(player_id=1, boards=my_species, food_bag=2)
    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=3,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = VegetarianResult(selected_species)

    assert get_feeding_result(feeding) == result


def test_vegetarian_multiple():
    """If multiple vegetarian species, defaults to largest by lexicographic
    ordering
    """

    selected_species = Species(
        food_supply=1,
        body_size=3,
        population=2)

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2),
        selected_species,
    ]

    me = Player(player_id=1, boards=my_species, food_bag=2)
    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=3,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = VegetarianResult(selected_species)

    assert get_feeding_result(feeding) == result


def test_carnivore_largest():
    """Carnivore attacks the largest species that can be attacked"""

    attacking_species = Species(
        food_supply=1,
        body_size=2,
        population=4,
        traits=[CarnivoreTrait()])

    my_species = [
        attacking_species,
        Species(
            food_supply=1,
            body_size=2,
            population=3,
            traits=[CarnivoreTrait()]),
    ]
    me = Player(player_id=1, boards=my_species, food_bag=2)

    defending_species = Species(
        food_supply=1,
        body_size=3,
        population=2)
    defending_player = Player(
        player_id=2,
        boards=[
            Species(
                food_supply=1,
                body_size=2,
                population=2),
            defending_species,
        ],
        food_bag=2)

    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=3,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
        defending_player,
    ]

    situation = Situation(attacking_species, defending_species, None, None)
    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = CarnivoreResult(
        attacking_species, defending_player, defending_species)

    assert is_attackable(situation)
    assert get_feeding_result(feeding) == result


def test_carnivore_largest_tie():
    """If multiple species are the same size, defaults to opponent order"""

    attacking_species = Species(
        food_supply=1,
        body_size=2,
        population=5,
        traits=[CarnivoreTrait()])

    my_species = [
        attacking_species,
        Species(
            food_supply=1,
            body_size=2,
            population=3,
            traits=[CarnivoreTrait()]),
    ]
    me = Player(player_id=1, boards=my_species, food_bag=2)

    watering_hole_tokens = 10

    defending_species = Species(
        food_supply=1,
        body_size=2,
        population=2)

    defending_player = Player(
        player_id=2,
        boards=[defending_species],
        food_bag=3)

    opponents = [
        defending_player,
        Player(
            player_id=3,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=3),
    ]

    situation = Situation(attacking_species, defending_species, None, None)
    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = CarnivoreResult(
        attacking_species, defending_player, defending_species)

    assert is_attackable(situation)
    assert get_feeding_result(feeding) == result


def test_carnivore_opponent_order_tie():
    """If multiple species are the same size on the same opponent, defaults
    to the opponent's board order
    """

    attacking_species = Species(
        food_supply=1,
        body_size=2,
        population=5,
        traits=[CarnivoreTrait()])

    my_species = [
        attacking_species,
        Species(
            food_supply=1,
            body_size=2,
            population=3,
            traits=[CarnivoreTrait()]),
    ]
    me = Player(player_id=1, boards=my_species, food_bag=2)

    watering_hole_tokens = 10

    defending_species = Species(
        food_supply=1,
        body_size=2,
        population=2)

    defending_player = Player(
        player_id=2,
        boards=[
            defending_species,
            Species(
                food_supply=1,
                body_size=2,
                population=2),
        ],
        food_bag=3)

    opponents = [
        defending_player,
        Player(
            player_id=3,
            boards=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=3),
    ]

    situation = Situation(attacking_species, defending_species, None, None)
    feeding = Feeding(me, watering_hole_tokens, opponents)
    result = CarnivoreResult(
        attacking_species, defending_player, defending_species)

    assert is_attackable(situation)
    assert get_feeding_result(feeding) == result
