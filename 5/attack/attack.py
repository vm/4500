from collections import namedtuple
from enum import Enum


class TraitKind(Enum):
    """represents a kind of trait card"""

    ambush = 'AMBUSH'
    burrowing = 'BURROWING'
    carnivore = 'CARNIVORE'
    climbing = 'CLIMBING'
    cooperation = 'COOPERATION'
    fat_tissue = 'FAT_TISSUE'
    fertile = 'FERTILE'
    foraging = 'FORAGING'
    hard_shell = 'HARD_SHELL'
    herding = 'HERDING'
    horns = 'HORNS'
    long_neck = 'LONG_NECK'
    pack_hunting = 'PACK_HUNTING'
    scavenger = 'SCAVENGER'
    symbiosis = 'SYMBIOSIS'
    warning_call = 'WARNING_CALL'


TraitCard = namedtuple('TraitCard', ['kind', 'num_tokens'])


class Species:
    """represents a species

    :attr traits: traits of the species
    :type traits: list of TraitCard

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

    def __init__(self):
        self.traits = []
        self.body_size = DEFAULT_BODY_SIZE
        self.population = DEFAULT_POPULATION
        self.food_supply = DEFAULT_FOOD_SUPPLY


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

    def is_carnivore(species):
        """determines whether a species is a carnivore

        :param species: species to check
        :type species: Species

        :returns: whether species is a carnivore
        :rtype: bool
        """

        return any(t.kind is TraitType.carnivore for t in species.traits)

    if not is_carnivore(attacker):
        raise ValueError('attacker must be a carnivore')

    raise NotImplementedError()
