from collections import namedtuple
from enum import Enum


Situation = namedtuple(
    'Situation', ['attacker', 'defender', 'left_neighbor', 'right_neighbor'])


class Role(Enum):
    attacker = 'attacker',
    defender = 'defender',
    left_neighbor = 'left_neighbor',
    right_neighbor = 'right_neighbor'


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

    MIN_NUM_TRAITS = 0
    MAX_NUM_TRAITS = 3

    DEFAULT_BODY_SIZE = 0
    MIN_BODY_SIZE = 0
    MAX_BODY_SIZE = 7

    DEFAULT_POPULATION = 1
    MIN_POPULATION = 0
    MAX_POPULATION = 7

    DEFAULT_FOOD_SUPPLY = 0

    def __init__(self, food_supply=None, body_size=None,
                 population=None, traits=None):
        """creates a Species

        :param food_supply: food supply
        :type food_supply: int

        :param body_size: body size
        :type body_size: int

        :param population: population
        :type population: int

        :param traits: traits
        :type traits: list of TraitCard
        """

        if food_supply is None:
            self.food_supply = self.DEFAULT_FOOD_SUPPLY
        else:
            self.food_supply = food_supply

        if body_size is None:
            self.body_size = self.DEFAULT_BODY_SIZE
        else:
            self._check_not_within_bounds(
                body_size, self.MIN_BODY_SIZE, self.MAX_BODY_SIZE, 'body_size')
            self.body_size = body_size

        if population is None:
            self.population = self.DEFAULT_POPULATION
        else:
            self._check_not_within_bounds(
                population, self.MIN_POPULATION, self.MAX_POPULATION,
                'population')
            self.population = population

        if traits is None:
            self.traits = []
        else:
            self._check_not_within_bounds(
                len(traits), self.MIN_NUM_TRAITS, self.MAX_NUM_TRAITS,
                'number of traits')
            self.traits = traits

    @staticmethod
    def _check_not_within_bounds(value, min_value, max_value, value_type):
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

    @property
    def is_carnivore(self):
        """whether the species is a carnivore

        :returns: whether the species is a carnivore
        :rtype: bool
        """

        return any(trait.is_carnivore for trait in self.traits)

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
