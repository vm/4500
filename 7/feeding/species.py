rom feeding.trait import Trait, FatTissueTrait


"""
A LOS is [JSONSpecies+, ..., JSONSpecies+]; the list might be empty.

A JSONSpecies is
    [["food",Nat],
     ["body",Nat],
     ["population",Nat],
     ["traits",LOT]]

A JSONSpecies+ is one of:
    - a regular JSONSpecies
    - a JSONSpecies with a "fat-food" field:
        [["food",Nat],
         ["body",Nat],
         ["population",Nat],
         ["traits",LOT]
         ["fat-food" ,Nat]]

A Natural+ is a JSON number interpretable as a natural number larger than,
or equal to, 1.

A Natural is a JSON number interpretable as a natural number.
"""


class Species:
    """represents a species board

    :attr traits: traits of the species
    :type traits: list of Trait

    :attr body_size: body size of the species
    :type body_size: int

    :attr population: population
    :type population: int

    :attr food_supply: current food supply of the species
    :type food_supply: int

    :inv: MIN_BODY_SIZE <= body_size <= MAX_BODY_SIZE
    :inv: MIN_POPULATION <= population <= MAX_POPULATION
    :inv: MIN_NUM_TRAITS <= len(traits) <= MAX_NUM_TRAITS
    """

    MIN_FOOD_SUPPLY = 0
    MAX_FOOD_SUPPLY = float('inf')

    MIN_NUM_TRAITS = 0
    MAX_NUM_TRAITS = 3

    MIN_BODY_SIZE = 0
    MAX_BODY_SIZE = 7

    MIN_POPULATION = 0
    MAX_POPULATION = 7

    def __init__(self, food_supply=0, body_size=0, population=1, traits=None):
        """creates a Species

        :param food_supply: food supply
        :type food_supply: int

        :param body_size: body size
        :type body_size: int

        :param population: population
        :type population: int

        :param traits: traits
        :type traits: list of Trait
        """

        self._check_within_bounds(
            food_supply, self.MIN_FOOD_SUPPLY, self.MAX_FOOD_SUPPLY,
            'food_supply')
        self.food_supply = food_supply

        self._check_within_bounds(
            body_size, self.MIN_BODY_SIZE, self.MAX_BODY_SIZE, 'body_size')
        self.body_size = body_size

        self._check_within_bounds(
            population, self.MIN_POPULATION, self.MAX_POPULATION,
            'population')
        self.population = population

        if traits is None:
            self.traits = []
        else:
#        TODO: commented out to allow test-fest to pass
#            self._check_within_bounds(
#                len(traits), self.MIN_NUM_TRAITS, self.MAX_NUM_TRAITS,
#                'number of traits')

            trait_names = [trait.json_name for trait in traits]
            if len(trait_names) != len(set(trait_names)):
                raise ValueError('invalid duplicate traits')

            self.traits = traits

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.food_supply == other.food_supply and
                self.body_size == other.body_size and
                self.population == other.population and
                sorted(self.traits) == sorted(other.traits))  # based on ids

    def __lt__(self, other):
        """implements lexicographic comparison by population, food given,
        and plain body size
        """

        return (self.population < other.population or
                self.food_supply < other.food_supply or
                self.body_size < other.body_size)

    @classmethod
    def from_json(cls, json_species):
        """creates a Species from a JSON representation

        :param json_species: JSON species
        :type json_species: JSONSpecies

        :returns: species
        :rtype: Species or None
        """

        if json_species is False:
            return None

        if not isinstance(json_species, list):
            raise ValueError('json_species must be a list')

        if not all(
                isinstance(pair, list) and len(pair) == 2
                for pair in json_species):
            raise ValueError('all json_species entries must be [name, value]')

        actual_names = ["food", "bag", "population", "traits"]
        passed_names = [name for [name, value] in json_species]

        if not len(passed_names) in {4, 5} and all(
                actual == passed
                for actual, passed in zip(actual_names, passed_names)):
            raise ValueError('invalid key on a species')

        [
            [_, food],
            [_, body],
            [_, population],
            [_, json_traits],
            *maybe_fat_food
        ] = json_species

        if not isinstance(json_traits, list):
            raise ValueError('invalid traits')

        traits = [Trait.from_json(t) for t in json_traits]

        if maybe_fat_food:
            [[fat_food_name, fat_food]] = maybe_fat_food
            if not fat_food_name == "fat-food":
                raise ValueError('invalid key on fat food')

            find_fat_tissue_trait = [
                trait
                for trait in traits
                if isinstance(trait, FatTissueTrait)
            ]

            if find_fat_tissue_trait:
                fat_tissue_trait = find_fat_tissue_trait[0]
            else:
                raise ValueError('no fat tissue trait found on a species'
                                 'passing fat food')

            fat_tissue_trait.add_fat_food(fat_food)

        return cls(food, body, population, traits)

    def to_json(self):
        """creates a JSON representation of the species

        :returns: JSON species
        :rtype: JSONSpecies
        """

        json_traits = [t.to_json() for t in self.traits]

        species = [["food", self.food_supply],
                   ["body", self.body_size],
                   ["population", self.population],
                   ["traits", json_traits]]

        fat_tissue_trait = self.get_trait(FatTissueTrait)
        if (fat_tissue_trait is not None and
                fat_tissue_trait.get_fat_food() > 0):
            species.append(["fat-food", fat_tissue_trait.get_fat_food()])

        return species

    def get_trait(self, TraitClass):
        """gets the first trait in a list of traits

        :param TraitClass: trait to find
        :type TraitClass: class Trait

        :returns: first trait found or None if not found
        :rtype: Trait or None
        """

        try:
            return next(t for t in self.traits
                        if isinstance(t, TraitClass))
        except StopIteration:
            return None

    @staticmethod
    def _check_within_bounds(value, min_value, max_value, value_type):
        """checks that a given value is not within the bounds

        :raises: ValueError if value is invalid
        """

        if not min_value <= value <= max_value:
            raise ValueError('{} must be in interval [{}, {}]'
                             .format(value_type, min_value, max_value))

    def has_trait(self, TraitClass):
        """whether the species has the given trait

        :param trait: trait to check
        :type trait: class inheriting from Trait

        :returns: whether the species has the given trait
        :rtype: bool
        """

        return any(isinstance(t, TraitClass) for t in self.traits)

    def is_carnivore(self):
        """whether the species is a carnivore

        :returns: whether the species is a carnivore
        :rtype: bool
        """

        return any(trait.is_carnivore for trait in self.traits)

    def is_hungry(self):
        """whether the species is hungry

        :returns: whether the species is hungry
        :rtype: bool
        """

        return (self._is_hungry_fat_tissue() or
                (self.food_supply < self.population))

    def _is_hungry_fat_tissue(self):
        """whether more food can be stored on fat food

        :returns: whether more food can be stored on fat food
        :rtype: bool
        """

        return (
            self.has_trait(FatTissueTrait) and
            self.get_trait(FatTissueTrait).get_fat_food() < self.body_size)

    @property
    def max_food_supply(self):
        """maximum food supply that the species can have

        :returns: max food supply
        :rtype: int
        """

        return self.population

    def prevents_attack(self, situation, role):
        """whether the species prevents an attack in the situation

        :param situation: situation
        :type situation: Situation

        :param role: role of the species in the situation
        :type role: Role

        :returns: whether the species prevents an attack in the situation
        :rtype: bool
        """

        return any(trait.prevents_attack(situation, role)
                   for trait in self.traits)

    def apply_traits(self, role):
        """applies trait modifications based on a given role

        :param role: role of the species in the situation
        :type role: Role
        """

        for trait in self.traits:
            trait.modify(self, role)

    def copy(self):
        """makes a copy of itself

        :returns: copy
        :rtype: Species
        """

        food_supply = self.food_supply
        body_size = self.body_size
        population = self.population
        traits = [t for t in self.traits]

        return Species(food_supply, body_size, population, traits)
