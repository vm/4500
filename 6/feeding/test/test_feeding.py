from feeding.attack import is_attackable
from feeding.feeding import Feeding
from feeding.player import Player
from feeding.species import Species
from feeding.trait import CarnivoreTrait, FatTissueTrait, HornsTrait


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

    me = Player(player_id=1, species=my_species, food_bag=2)
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    watering_hole_tokens = 10
    opponents = [
        Player(
            player_id=2,
            species=[
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
    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 2
    opponents = [
        Player(
            player_id=2,
            species=[
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
        attacker,
        Species(
            food_supply=1,
            body_size=2,
            population=3,
            traits=[CarnivoreTrait()]),
    ]
    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10

    defending_species = Species(food_supply=1, body_size=2, population=2)
    defending_player = Player(player_id=2, species=[defender], food_bag=2)
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
            food_supply=1,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=2)]),
        attacking_species,
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10

    defending_species = Species(
        food_supply=1,
        body_size=2,
        population=2)
    defending_player = Player(
        player_id=2,
        species=[defending_species],
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
    me = Player(player_id=1, species=my_species, food_bag=2)
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    watering_hole_tokens = 10
    opponents = [
        Player(
            player_id=3,
            species=[
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
    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 2
    expected_tokens = min((selected_species.body_size -
                           selected_species.traits[0].get_fat_food()),
                          watering_hole_tokens)

    opponents = [
        Player(
            player_id=3,
            species=[
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

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    opponents = [
        Player(
            player_id=2,
            species=[
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

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    opponents = [
        Player(
            player_id=2,
            species=[
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

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10
    expected_tokens = (selected_species.body_size -
                       selected_species.traits[0].get_fat_food())

    opponents = [
        Player(
            player_id=2,
            species=[
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

    me = Player(player_id=1, species=my_species, food_bag=2)
    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=3,
            species=[
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

    me = Player(player_id=1, species=my_species, food_bag=2)
    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=3,
            species=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
    result VegetarianResult(selected_species)

    assert get_feeding_result(feeding) == result


def test_carnivore_largest():
    """Carnivore attacks the largest species that can be attacked"""

    attacking_species = Species(
        food_supply=1,
        body_size=2,
        population=2,
        traits=[CarnivoreTrait()])

    my_species = [
        attacking_species,
        Species(
            food_supply=1,
            body_size=2,
            population=3,
            traits=[CarnivoreTrait()]),
    ]
    me = Player(player_id=1, species=my_species, food_bag=2)

    defending_species = Species(
        food_supply=1,
        body_size=3,
        population=2)
    defending_player = Player(
        player_id=2,
        species=[
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
            species=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=2),
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
    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10

    defending_species = Species(
        food_supply=1,
        body_size=2,
        population=2)

    defending_player = Player(
        player_id=2,
        species=[defending_species],
        food_bag=3)

    opponents = [
        defending_player,
        Player(
            player_id=3,
            species=[
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
    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10

    defending_species = Species(
        food_supply=1,
        body_size=2,
        population=2)

    defending_player = Player(
        player_id=2,
        species=[
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
            species=[
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
