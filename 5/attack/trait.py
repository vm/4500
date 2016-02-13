from attack.situation import Situation, Role


class Trait:
    """represents a trait card

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

    def __init__(self, tokens):
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

    pass


class BurrowingTrait(Trait):
    """implements a Burrowing trait

    Burrowing deflects an attack when its species has a food supply equal to
    its population size
    """

    @staticmethod
    def prevents_attack(situation, role):
        defender = situation.defender
        return (role is Role.defender and
                defender.food_supply == defender.population)


class CarnivoreTrait(Trait):
    """implements an Carnivore trait

    Carnivore must attack to eat during the feeding stage.
    """

    is_carnivore = True


class ClimbingTrait(Trait):
    """implements a Climbing trait

    Climbing prevents an attack unless the Carnivore also has the Climbing
    attribute.
    """

    @staticmethod
    def prevents_attack(situation, role):
        attacker, defender, *_ = situation
        return (role is Role.defender and
                defender.has_trait(ClimbingTrait) and
                not attacker.has_trait(ClimbingTrait))


class HardShellTrait(Trait):
    """implements a Hard Shell trait

    Hard Shell prevents an attack unless the attacker is at least 4 units
    larger than this species in body size.
    """

    @staticmethod
    def prevents_attack(situation, role):
        attacker, defender, *_ = situation
        return (role is Role.defender and
                attacker.body_size - 4 < defender.body_size)


class HerdingTrait(Trait):
    """implements a Herding trait

    Herding stops attacks from Carnivore species whose populations are smaller
    or equal in size to this species’ population.
    """

    @staticmethod
    def prevents_attack(situation, role):
        attacker, defender, *_ = situation
        return (role is Role.defender and
                attacker.population <= defender.population)


class PackHuntingTrait(Trait):
    """implements a Pack Hunting trait

    Pack Hunting adds this species’ population size to its body size for
    attacks on other species.
    """

    @staticmethod
    def modify(species, role):
        if role is Role.attacker:
            species.body_size += species.population
        return species


class SymbiosisTrait(Trait):
    """implements a Symbiosis trait

    Symbiosis prevents an attack if this species has a neighbor to the right
    whose body size is larger than this one’s.
    """

    @staticmethod
    def prevents_attack(situation, role):
        attacker, defender, _, right_neighbor = situation

        return (role is Role.defender and
                right_neighbor is not None and
                right_neighbor.body_size > defender.body_size)


class WarningCallTrait(Trait):
    """implements a Warning Call trait

    Warning Call prevents an attack from a Carnivore on both neighboring
    species unless the attacker has the Ambush property.
    """

    @staticmethod
    def prevents_attack(situation, role):
        attacker, _, left_neighbor, right_neighbor = situation

        left_neighbor_prevents = (role is Role.left_neighbor and
                                  left_neighbor is not None and
                                  left_neighbor.has_trait(WarningCallTrait))

        right_neighbor_prevents = (role is Role.right_neighbor and
                                   right_neighbor is not None and
                                   right_neighbor.has_trait(WarningCallTrait))

        return ((left_neighbor_prevents or right_neighbor_prevents) and
                not situation.attacker.has_trait(AmbushTrait))


trait_name_to_class = {
    'carnivore': CarnivoreTrait,
    'ambush': AmbushTrait,
    'burrowing': BurrowingTrait,
    'climbing': ClimbingTrait,
    'hard-shell': HardShellTrait,
    'herding': HerdingTrait,
    'pack-hunting': PackHuntingTrait,
    'symbiosis': SymbiosisTrait,
    'warning-call': WarningCallTrait,
}