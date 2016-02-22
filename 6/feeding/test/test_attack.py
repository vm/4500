import pytest

from feeding.attack import is_attackable
from feeding.trait import *
from feeding.situation import Situation
from feeding.species import Species


def test_not_carnivore():
    """tests that an error is raised when the attacker is not a carnivore"""

    attacker = Species()
    defender = Species()

    with pytest.raises(ValueError):
        situation = Situation(attacker, defender, None, None)
        is_attackable(situation)


def test_ambush():
    """tests the Ambust trait"""

    attacker = Species(traits=[CarnivoreTrait(), AmbushTrait()])
    defender = Species(traits=[WarningCallTrait()])
    assert is_attackable(Situation(attacker, defender, None, None))

    attacker = Species(traits=[CarnivoreTrait(), AmbushTrait()])
    defender = Species()
    left_neighbor = Species(traits=[WarningCallTrait()])
    assert is_attackable(Situation(attacker, defender, left_neighbor, None))

    attacker = Species(traits=[CarnivoreTrait(), AmbushTrait()])
    defender = Species()
    right_neighbor = Species(traits=[WarningCallTrait()])
    assert is_attackable(Situation(attacker, defender, None, right_neighbor))


def test_burrowing():
    """tests the Burrowing trait"""

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species(food_supply=4, population=4, traits=[BurrowingTrait()])
    assert not is_attackable(Situation(attacker, defender, None, None))

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species(food_supply=0, population=4, traits=[BurrowingTrait()])
    assert is_attackable(Situation(attacker, defender, None, None))


def test_climbing():
    """tests the Climbing trait"""

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species(traits=[ClimbingTrait()])
    assert not is_attackable(Situation(attacker, defender, None, None))

    attacker = Species(traits=[CarnivoreTrait(), ClimbingTrait()])
    defender = Species(traits=[ClimbingTrait()])
    assert is_attackable(Situation(attacker, defender, None, None))


def test_hard_shell():
    """tests the Hard Shell trait"""

    attacker = Species(body_size=4, traits=[CarnivoreTrait()])
    defender = Species(body_size=1, traits=[HardShellTrait()])
    assert not is_attackable(Situation(attacker, defender, None, None))

    attacker = Species(body_size=5, traits=[CarnivoreTrait()])
    defender = Species(body_size=1, traits=[HardShellTrait()])
    assert is_attackable(Situation(attacker, defender, None, None))


def test_herding():
    """tests the Herding trait"""

    attacker = Species(population=3, traits=[CarnivoreTrait()])
    defender = Species(population=4, traits=[HerdingTrait()])
    assert not is_attackable(Situation(attacker, defender, None, None))

    attacker = Species(population=4, traits=[CarnivoreTrait()])
    defender = Species(population=4, traits=[HerdingTrait()])
    assert not is_attackable(Situation(attacker, defender, None, None))

    attacker = Species(population=5, traits=[CarnivoreTrait()])
    defender = Species(population=4, traits=[HerdingTrait()])
    assert is_attackable(Situation(attacker, defender, None, None))


def test_pack_hunting():
    """tests the Pack Hunting trait"""

    attacker = Species(
        body_size=4,
        population=1,
        traits=[CarnivoreTrait(), PackHuntingTrait()])
    defender = Species(body_size=1, traits=[HardShellTrait()])
    assert is_attackable(Situation(attacker, defender, None, None))

    attacker = Species(
        body_size=3,
        population=1,
        traits=[CarnivoreTrait(), PackHuntingTrait()])
    defender = Species(body_size=1, traits=[HardShellTrait()])
    assert not is_attackable(Situation(attacker, defender, None, None))


def test_symbiosis():
    """tests the Symbiosis trait"""

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species(body_size=2, traits=[SymbiosisTrait()])
    right_neighbor = Species(body_size=4)
    assert not is_attackable(
        Situation(attacker, defender, None, right_neighbor))

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species(body_size=6, traits=[SymbiosisTrait()])
    right_neighbor = Species(body_size=4)
    assert is_attackable(Situation(attacker, defender, None, right_neighbor))

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species(body_size=2, traits=[SymbiosisTrait()])
    left_neighbor = Species(body_size=4)
    assert is_attackable(Situation(attacker, defender, left_neighbor, None))

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species(body_size=6, traits=[SymbiosisTrait()])
    left_neighbor = Species(body_size=4)
    assert is_attackable(Situation(attacker, defender, left_neighbor, None))


def test_warning_call():
    """tests the Warning Call trait"""

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species(traits=[WarningCallTrait()])
    assert is_attackable(Situation(attacker, defender, None, None))

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species()
    left_neighbor = Species(traits=[WarningCallTrait()])
    assert not is_attackable(
        Situation(attacker, defender, left_neighbor, None))

    attacker = Species(traits=[CarnivoreTrait()])
    defender = Species()
    right_neighbor = Species(traits=[WarningCallTrait()])
    assert not is_attackable(
        Situation(attacker, defender, None, right_neighbor))
