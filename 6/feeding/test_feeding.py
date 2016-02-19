"""
FOR ALL TEST HUNGRY/NOT-HUNGRY OF EACH
ADD TESTS THAT PLAYER DOESN'T VIOLATE BEHAVIORAL CONTRACTS


A Feeding is [Player, Natural+, LOP]. The natural number in the middle
specifies how many tokens of food are left at the watering hole.

A Player is
    [["id",Natural+],
     ["species",LOS],
     ["bag",Natural]]

A LOP is [Player, ..., Player]; the list might be empty.

A LOS is [Species+, ..., Species+]; the list might be empty.

A Natural+ is a JSON number interpretable as a natural number larger than, or
equal to, 1.

A Natural is a JSON number interpretable as a natural number.

A Species+ is one of:
a regular Species

a Species with a "fat-food" field:
    [["food",Nat],
     ["body",Nat],
     ["population",Nat],
     ["traits",LOT]
     ["fat-food" ,Nat]]
"""

def json_player(player_id, species, bag):
    """gets a JSON player representation from the given parameters

    :param player_id: player id
    :type player_id: Natural+

    :param species: list of JSON species
    :type species: LOS

    :param bag: food bag count
    :type bag: Natural

    :returns: JSON player representation
    :rtype: Player
    """

    return [["id", player_id],
            ["species", species],
            ["bag", bag]]


def json_species(food, body, population, traits, fat_food=None):
    """gets a JSON species from the given parameters

    :param food: food supply
    :type food: Nat

    :param body: body size
    :type body: Nat

    :param population: population
    :type population: Nat

    :param traits: traits
    :type traits: LOT

    :param fat_food: fat food if returned species is a Species+
    :type fat_food: Nat or None

    :returns: JSON representation of a species
    :type: Species or Species+
    """

    species = [["food", food],
               ["body", body],
               ["population", population],
               ["traits", traits]]

    if fat_food is not None:
        species.append(["fat-food", fat_food])

    return species

# TODO test if fat tissue greater than 0 and fat tissue species chosen, natural
# in the return is equal to the body size - fat tissue stored

# TODO watering hole has less than max fat tissue cap

def test_fat_tissue_one():
    """If only one species with fat tissue trait, it is selected"""

    my_species = [
        json_species(1, 2, 2, ['fat-tissue'], 0),
        json_species(1, 2, 2, []),
    ]

    me = json_player(1, my_species, 2)
    watering_hole_tokens = 10
    opponents = [
        json_player(2, [json_species(1, 2, 2, [])], 2),
        json_player(3, [json_species(1, 2, 2, [])], 2),
    ]

    feeding = [me, watering_hole_tokens, opponents]


def test_fat_tissue_multiple():
    """If multiple species with fat tissue trait, default to least fat tissue
    need"""
    pass


def test_fat_tissue_need_tie():
    """If multiple species and same fat tissue need, defaults to
    lexicographic ordering"""
    pass


def test_fat_tissue_ordering_tie():
    """If multiple species, same fat tissue need and lexicographic ordering
    tie, default to player board order"""
    pass


def test_vegetarian_one():
    """If only one vegetarian species, it is selected"""

    my_species = [
        json_species(1, 2, 2, []), #RETURNED
        json_species(1, 2, 2, ['carnivore']),
    ]

    me = json_player(1, my_species, 2)
    watering_hole_tokens = 10
    opponents = [
        json_player(3, [json_species(1, 2, 2, [])], 2),
    ]

    feeding = [me, watering_hole_tokens, opponents]


def test_vegetarian_multiple():
    """If multiple vegetarian species, defaults to lexicographic ordering"""

    my_species = [
        json_species(1, 2, 2, []),
        json_species(1, 3, 2, []),  # RETURNED
    ]

    me = json_player(1, my_species, 2)
    watering_hole_tokens = 10
    opponents = [
        json_player(3, [json_species(1, 2, 2, [])], 2),
    ]

    feeding = [me, watering_hole_tokens, opponents]


# TODO make sure to validate is attackable
def test_carnivore_largest():
    """Carnivore attacks the largest species that can be attacked"""

    my_species = [
        json_species(1, 2, 2, ['carnivore'])
    ]

    me = json_player(1, my_species, 2)
    watering_hole_tokens = 10
    opponents = [
        json_player(3, [
            json_species(1, 2, 2, []),
            json_species(1, 3, 2, [])  # THIS ONE
        ], 2)
    ]

    feeding = [me, watering_hole_tokens, opponents]


def test_carnivore_largest_tie():
    """If multiple species are the same size, defaults to opponent order"""

    my_species = [
        json_species(1, 2, 2, ['carnivore'])
    ]

    me = json_player(1, my_species, 2)
    watering_hole_tokens = 10
    opponents = [
        json_player(3, [json_species(1, 2, 2, [])], 3),   # THIS ONE
        json_player(4, [json_species(1, 2, 2, []]), 3)
    ]

    feeding = [me, watering_hole_tokens, opponents]


def test_carnivore_opponent_order_tie():
    """If multiple species are the same size on the same opponent, defaults
    to the opponent's board order"""

    my_species = [
        json_species(1, 2, 2, ['carnivore'])
    ]

    me = json_player(1, my_species, 2)
    watering_hole_tokens = 10
    opponents = [
        json_player(3, [
            json_species(1, 2, 2, []),    # THIS ONE
            json_species(1, 2, 2, [])
        ], 3),
        json_player(4, [json_species(1, 2, 2, []]), 3)
    ]

    feeding = [me, watering_hole_tokens, opponents]


def test_no_feeding_none_hungry():
    """If nothing can comsume food, returns no feeding"""

    my_species = [
        json_species(2, 2, 2, ['carnivore'])
    ]

    me = json_player(1, my_species, 2)
    watering_hole_tokens = 10
    opponents = [
        json_player(3, [
            json_species(1, 2, 2, []),    # THIS ONE
            json_species(1, 2, 2, [])
        ], 3),
        json_player(4, [json_species(1, 2, 2, []]), 3)
    ]

    feeding = [me, watering_hole_tokens, opponents]


def test_no_feeding_carnivore_cannot_attack():
    """If the the player only has one species which is a carnivore and none of
    the opponents' species are attackable, returns no feeding"""

    my_species = [
        json_species(1, 2, 2, ['carnivore'])
    ]

    me = json_player(1, my_species, 2)
    watering_hole_tokens = 10
    opponents = [
        json_player(3, [json_species(1, 2, 2, ['hard-shell'])], 3),
        json_player(4, [json_species(1, 2, 2, ['hard-shell']]), 3)
    ]

    feeding = [me, watering_hole_tokens, opponents]


def test_no_feeding_carnivore_cannot_attack_horns():
    """If the the player only has one species which is a carnivore and
    only attackable species has horns and player's species has 1 population
    size, returns no feeding"""

    my_species = [
        json_species(1, 2, 1, ['carnivore'])
    ]

    me = json_player(1, my_species, 2)
    watering_hole_tokens = 10
    opponents = [
        json_player(3, [json_species(1, 2, 2, ['horns'])], 3)
    ]

    feeding = [me, watering_hole_tokens, opponents]
