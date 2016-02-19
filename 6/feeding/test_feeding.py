from feeding.feeding import Feeding
from feeding.player import Player
from feeding.species import Species
from feeding.traits import CarnivoreTrait, FatTissueTrait, HornsTrait


"""
FOR ALL TEST HUNGRY/NOT-HUNGRY OF EACH
ADD TESTS THAT PLAYER DOESN'T VIOLATE BEHAVIORAL CONTRACTS
"""


def test_fat_tissue_one():
    """If only one species with fat tissue trait, it is selected"""

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=0)]),  # THIS ONE
        Species(
            food_supply=1,
            body_size=2,
            population=2),
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

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


def test_fat_tissue_nonzero_fat():
    """If fat tissue greater than 0 and fat tissue species chosen, tokens
    requested in the return is equal to the body size - fat tissue stored"""

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=1)]),  # THIS ONE
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

    # TODO ASSERT EQUAL ONE


def test_fat_tissue_max_watering_hole():
    """The player asks for the number of tokens in the watering hole if it is
    less than the fat tissue can add"""

    my_species = [
        Species(
            food_supply=1,
            body_size=6,
            population=2,
            traits=[FatTissueTrait(fat_food=2)]),  # THIS ONE
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 2

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

    # TODO ASSERT EQUAL 2


def test_fat_tissue_multiple():
    """If multiple species with fat tissue trait, default to largest fat
    tissue need"""

    my_species = [
        Species(
            food_supply=1,
            body_size=5,
            population=2,
            traits=[FatTissueTrait(fat_food=4)]),
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=0)]),  #THIS ONE
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

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


def test_fat_tissue_need_tie():
    """If multiple species and same fat tissue need, defaults to largest by
    lexicographic ordering"""

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=1)]),
        Species(
            food_supply=1,
            body_size=3,
            population=2,
            traits=[FatTissueTrait(fat_food=1)]),  #THIS ONE
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

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


def test_fat_tissue_ordering_tie():
    """If multiple species, same fat tissue need and lexicographic ordering
    tie, default to player board order"""

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,  # THIS ONE
            traits=[FatTissueTrait(fat_food=1)]),
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=1)]),
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

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


def test_vegetarian_one():
    """If only one vegetarian species, it is selected"""

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2), # RETURNED
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[CarnivoreTrait()]),
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


def test_vegetarian_multiple():
    """If multiple vegetarian species, defaults to largest by lexicographic
    ordering"""

    my_species = [
        Species(
            food_supply=1,
            body_size=3,
            population=2), # RETURNED BOY
        Species(
            food_supply=1,
            body_size=2,
            population=2),
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


# TODO make sure to validate is attackable
def test_carnivore_largest():
    """Carnivore attacks the largest species that can be attacked"""

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[CarnivoreTrait()]),
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=2,
            species=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
                Species(
                    food_supply=1,  # This one
                    body_size=3,
                    population=2),
            ],
            food_bag=2),
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


def test_carnivore_largest_tie():
    """If multiple species are the same size, defaults to opponent order"""

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[CarnivoreTrait()]),
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=2,
            species=[
                Species(
                    food_supply=1,  # THIS ONE
                    body_size=2,
                    population=2),
            ],
            food_bag=3),
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

    feeding = Feeding(me, watering_hole_tokens, opponents)



def test_carnivore_opponent_order_tie():
    """If multiple species are the same size on the same opponent, defaults
    to the opponent's board order"""

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[CarnivoreTrait()]),
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=2,
            species=[
                Species(
                    food_supply=1,  # THIS ONE
                    body_size=2,
                    population=2),
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2),
            ],
            food_bag=3),
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

    feeding = Feeding(me, watering_hole_tokens, opponents)


def test_no_feeding_none_hungry():
    """If nothing can comsume food, returns no feeding"""

    feeding = [me, watering_hole_tokens, opponents]

    my_species = [
        Species(
            food_supply=2,
            body_size=2,
            population=2,
            traits=[CarnivoreTrait()]),
        Species(
            food_supply=2,
            body_size=2,
            population=2),
        Species(
            food_supply=2,
            body_size=2,
            population=2,
            traits=[FatTissueTrait(fat_food=2)]),
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
            food_bag=3),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)


def test_no_feeding_carnivore_cannot_attack():
    """If the the player only has one species which is a carnivore and none of
    the opponents' species are attackable, returns no feeding"""

    my_species = [
        Species(
            food_supply=1,
            body_size=2,
            population=2,
            traits=[CarnivoreTrait()]),
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=2,
            species=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2,
                    traits=[HardShell()]),
            ],
            food_bag=3),
        Player(
            player_id=3,
            species=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2,
                    traits=[HardShell()]),
            ],
            food_bag=3),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)


def test_no_feeding_carnivore_cannot_attack_horns():
    """If the the player only has one species which is a carnivore and
    only attackable species has horns and player's species has 1 population
    size, returns no feeding"""

    my_species = [
        Species(
            food_supply=0,
            body_size=2,
            population=1,
            traits=[CarnivoreTrait()]),
    ]

    me = Player(player_id=1, species=my_species, food_bag=2)

    watering_hole_tokens = 10

    opponents = [
        Player(
            player_id=2,
            species=[
                Species(
                    food_supply=1,
                    body_size=2,
                    population=2,
                    traits=[HornsTrait()]),
            ],
            food_bag=2),
    ]

    feeding = Feeding(me, watering_hole_tokens, opponents)
