"""
A JSONTrait is one of:
    - "carnivore"
    - "ambush"
    - "burrowing"
    - "climbing"
    - "cooperation"
    - "fat-tissue"
    - "fertile"
    - "foraging"
    - "hard-shell"
    - "herding"
    - "horns"
    - "long-neck"
    - "pack-hunting"
    - "scavenger"
    - "symbiosis"
    - "warning-call"
"""


class Trait:
    """base class for a trait card

    subclass and provide json_name class attribute

    :attr ttype: type of the trait
    :type ttype: TraitType

    :attr tokens: number of tokens
    :type tokens: int
    """

    CARNIVORE_MIN_TOKENS = -8
    CARNIVORE_MAX_TOKENS = 8

    VEGETARIAN_MIN_TOKENS = -3
    VEGETARIAN_MAX_TOKENS = 3

    is_carnivore = False

    def __init__(self, tokens=0):
        """creates a trait type

        :param ttype: type of the trait
        :type ttype: TraitType

        :param tokens: number of tokens
        :type tokens: int

        :param is_carnivore: whether the trait is a carnivore
        :type is_carnivore: bool
        """

        if self.is_carnivore:
            min_tokens = self.CARNIVORE_MIN_TOKENS
            max_tokens = self.CARNIVORE_MAX_TOKENS
        else:
            min_tokens = self.VEGETARIAN_MIN_TOKENS
            max_tokens = self.VEGETARIAN_MAX_TOKENS

        if not min_tokens <= tokens <= max_tokens:
            msg = ('Tokens for vegetarian must be in interval [{},{}]'
                   .format(min_tokens, max_tokens))
            raise ValueError(msg)

        self.tokens = tokens

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.tokens == other.tokens)

    def __lt__(self, other):
        return self.json_name < other.json_name

    @classmethod
    def from_json(cls, json_trait):
        """creates a Trait from a JSON representation

        :param json_trait: JSON trait
        :type json_trait: JSONTrait

        :returns: trait
        :rtype: Trait
        """

        trait_name_to_class = {tc.json_name: tc for tc in ALL_TRAITS}

        try:
            TraitClass = trait_name_to_class[json_trait]
        except KeyError:
            raise ValueError("Unknown JSON trait name")

        return TraitClass()

    def to_json(self):
        """creates a JSON representation of the trait

        :returns: JSON trait
        :rtype: JSONTrait
        """

        return self.json_name

    @staticmethod
    def modify(species, role):
        """modifies the species

        to be overwritten by the inheriting class
        default behavior is to not modify the species

        :param species: species to modify
        :type species: Species

        :param role: role of the species in the situation
        :type role: Role

        :returns: modified species
        :rtype: Species
        """

        return species

    @staticmethod
    def prevents_attack(situation, role):
        """determines whether the trait prevents an attack

        to be overwritten by the inheriting class
        default behavior is to return true

        :param situation: situation to evaluate
        :type situation: Situation

        :param role: role in the situation
        :type role: SituationRole

        :returns: whether the situation results in an attack
        :rtype: bool
        """

        return False


class AmbushTrait(Trait):
    """implements an Ambush trait

    Ambush overcomes a Warning Call during an attack
    """

    json_name = 'ambush'


class BurrowingTrait(Trait):
    """implements a Burrowing trait

    Burrowing deflects an attack when its species has a food supply equal to
    its population size
    """

    json_name = 'burrowing'

    @staticmethod
    def prevents_attack(situation, role):
        defender = situation.defender
        return (role is Role.defender and
                defender.food_supply == defender.population)


class CarnivoreTrait(Trait):
    """implements an Carnivore trait

    Carnivore must attack to eat during the feeding stage.
    """

    json_name = 'carnivore'
    is_carnivore = True


class ClimbingTrait(Trait):
    """implements a Climbing trait

    Climbing prevents an attack unless the Carnivore also has the Climbing
    attribute.
    """

    json_name = 'climbing'

    @staticmethod
    def prevents_attack(situation, role):
        defender, attacker, *_ = situation
        return (role is Role.defender and
                defender.has_trait(ClimbingTrait) and
                not attacker.has_trait(ClimbingTrait))


class CooperationTrait(Trait):
    """implements a Cooperation trait

    Cooperation automatically feeds the species to its right one token of food
    every time it eats (taken from the common food supply at the watering
    hole).
    """

    json_name = 'cooperation'


class FatTissueTrait(Trait):
    """implements a Fat Tissue trait

    Fat Tissue allows a species to store as many food tokens as its body-size
    count.
    """

    json_name = 'fat-tissue'

    DEFAULT_FAT_FOOD = 0

    def __init__(self, fat_food=DEFAULT_FAT_FOOD):
        super().__init__()
        self._fat_food = fat_food

    def __eq__(self, other):
        return super().__eq__(other) and self._fat_food == other._fat_food

    def get_fat_food(self):
        return self._fat_food

    def add_fat_food(self, tokens):
        self._fat_food += tokens

    def reset_fat_food(self):
        self._fat_food = DEFAULT_FAT_FOOD


class FertileTrait(Trait):
    """implements a Fertile trait

    Fertile automatically adds one animal to the population when the food cards
    are revealed.
    """

    json_name = 'fertile'


class ForagingTrait(Trait):
    """implements a Foraging trait

    Foraging enables this species to eat two tokens of food for every feeding.
    """

    json_name = 'foraging'


class HardShellTrait(Trait):
    """implements a Hard Shell trait

    Hard Shell prevents an attack unless the attacker is at least 4 units
    larger than this species in body size.
    """

    json_name = 'hard-shell'

    @staticmethod
    def prevents_attack(situation, role):
        defender, attacker, *_ = situation
        return (role is Role.defender and
                attacker.body_size - 4 < defender.body_size)


class HerdingTrait(Trait):
    """implements a Herding trait

    Herding stops attacks from Carnivore species whose populations are smaller
    or equal in size to this species’ population.
    """

    json_name = 'herding'

    @staticmethod
    def prevents_attack(situation, role):
        defender, attacker, *_ = situation
        return (role is Role.defender and
                attacker.population <= defender.population)


class HornsTrait(Trait):
    """implements a Horns trait

    Horns kills one animal of an attacking Carnivore species before the attack
    is completed.
    """

    json_name = 'horns'


class LongNeckTrait(Trait):
    """implements a Long Neck trait

    Long Neck automatically adds one food token for the entire species when
    the food cards are revealed.
    """

    json_name = 'long-neck'


class PackHuntingTrait(Trait):
    """implements a Pack Hunting trait

    Pack Hunting adds this species’ population size to its body size for
    attacks on other species.
    """

    json_name = 'pack-hunting'

    @staticmethod
    def modify(species, role):
        if role is Role.attacker:
            species.body_size += species.population
        return species


class ScavengerTrait(Trait):
    """implements a Scavenger trait

    Scavenger automatically eats one food token every time a Carnivore eats
    another species.
    """

    json_name = 'scavenger'


class SymbiosisTrait(Trait):
    """implements a Symbiosis trait

    Symbiosis prevents an attack if this species has a neighbor to the right
    whose body size is larger than this one’s.
    """

    json_name = 'symbiosis'

    @staticmethod
    def prevents_attack(situation, role):
        defender, attacker, _, right_neighbor = situation

        return (role is Role.defender and
                right_neighbor is not None and
                right_neighbor.body_size > defender.body_size)


class WarningCallTrait(Trait):
    """implements a Warning Call trait

    Warning Call prevents an attack from a Carnivore on both neighboring
    species unless the attacker has the Ambush property.
    """

    json_name = 'warning-call'

    @staticmethod
    def prevents_attack(situation, role):
        _, attacker, left_neighbor, right_neighbor = situation

        left_prevents = (role is Role.left_neighbor and
                         left_neighbor is not None and
                         left_neighbor.has_trait(WarningCallTrait))

        right_prevents = (role is Role.right_neighbor and
                          right_neighbor is not None and
                          right_neighbor.has_trait(WarningCallTrait))

        return ((left_prevents or right_prevents) and
                not situation.attacker.has_trait(AmbushTrait))


ALL_TRAITS = [
    AmbushTrait,
    BurrowingTrait,
    CarnivoreTrait,
    ClimbingTrait,
    CooperationTrait,
    FatTissueTrait,
    FertileTrait,
    ForagingTrait,
    HardShellTrait,
    HerdingTrait,
    HornsTrait,
    LongNeckTrait,
    PackHuntingTrait,
    ScavengerTrait,
    SymbiosisTrait,
    WarningCallTrait,
]
