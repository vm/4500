import pytest

from feeding.attack import is_attackable
from feeding.trait import *
from feeding.situation import Situation
from feeding.species import Species


def test_not_carnivore():
    """tests that an error is raised when the attacker is not a carnivore"""

    defender = Species()
    attacker = Species()

    with pytest.raises(ValueError):
        situation = Situation(defender, attacker, None, None)
        is_attackable(situation)


def test_ambush():
    """tests the Ambust trait"""

    defender = Species(traits=[WarningCallTrait()])
    attacker = Species(traits=[CarnivoreTrait(), AmbushTrait()])
    assert is_attackable(Situation(defender, attacker, None, None))

    defender = Species()
    attacker = Species(traits=[CarnivoreTrait(), AmbushTrait()])
    left_neighbor = Species(traits=[WarningCallTrait()])
    assert is_attackable(Situation(defender, attacker, left_neighbor, None))

    defender = Species()
    attacker = Species(traits=[CarnivoreTrait(), AmbushTrait()])
    right_neighbor = Species(traits=[WarningCallTrait()])
    assert is_attackable(Situation(defender, attacker, None, right_neighbor))


def test_burrowing():
    """tests the Burrowing trait"""

    defender = Species(food_supply=4, population=4, traits=[BurrowingTrait()])
    attacker = Species(traits=[CarnivoreTrait()])
    assert not is_attackable(Situation(defender, attacker, None, None))

    defender = Species(food_supply=0, population=4, traits=[BurrowingTrait()])
    attacker = Species(traits=[CarnivoreTrait()])
    assert is_attackable(Situation(defender, attacker, None, None))


def test_climbing():
    """tests the Climbing trait"""

    defender = Species(traits=[ClimbingTrait()])
    attacker = Species(traits=[CarnivoreTrait()])
    assert not is_attackable(Situation(defender, attacker, None, None))

    defender = Species(traits=[ClimbingTrait()])
    attacker = Species(traits=[CarnivoreTrait(), ClimbingTrait()])
    assert is_attackable(Situation(defender, attacker, None, None))


def test_hard_shell():
    """tests the Hard Shell trait"""

    defender = Species(body_size=1, traits=[HardShellTrait()])
    attacker = Species(body_size=4, traits=[CarnivoreTrait()])
    assert not is_attackable(Situation(defender, attacker, None, None))

    defender = Species(body_size=1, traits=[HardShellTrait()])
    attacker = Species(body_size=5, traits=[CarnivoreTrait()])
    assert is_attackable(Situation(defender, attacker, None, None))


def test_herding():
    """tests the Herding trait"""

    defender = Species(population=4, traits=[HerdingTrait()])
    attacker = Species(population=3, traits=[CarnivoreTrait()])
    assert not is_attackable(Situation(defender, attacker, None, None))

    defender = Species(population=4, traits=[HerdingTrait()])
    attacker = Species(population=4, traits=[CarnivoreTrait()])
    assert not is_attackable(Situation(defender, attacker, None, None))

    defender = Species(population=4, traits=[HerdingTrait()])
    attacker = Species(population=5, traits=[CarnivoreTrait()])
    assert is_attackable(Situation(defender, attacker, None, None))


def test_pack_hunting():
    """tests the Pack Hunting trait"""

    defender = Species(body_size=1, traits=[HardShellTrait()])
    attacker = Species(
        body_size=4,
        population=1,
        traits=[CarnivoreTrait(), PackHuntingTrait()])
    assert is_attackable(Situation(defender, attacker, None, None))

    defender = Species(body_size=1, traits=[HardShellTrait()])
    attacker = Species(
        body_size=3,
        population=1,
        traits=[CarnivoreTrait(), PackHuntingTrait()])
    assert not is_attackable(Situation(defender, attacker, None, None))


def test_symbiosis():
    """tests the Symbiosis trait"""

    defender = Species(body_size=2, traits=[SymbiosisTrait()])
    attacker = Species(traits=[CarnivoreTrait()])
    right_neighbor = Species(body_size=4)
    assert not is_attackable(
        Situation(defender, attacker, None, right_neighbor))

    defender = Species(body_size=6, traits=[SymbiosisTrait()])
    attacker = Species(traits=[CarnivoreTrait()])
    right_neighbor = Species(body_size=4)
    assert is_attackable(Situation(defender, attacker, None, right_neighbor))

    defender = Species(body_size=2, traits=[SymbiosisTrait()])
    attacker = Species(traits=[CarnivoreTrait()])
    left_neighbor = Species(body_size=4)
    assert is_attackable(Situation(defender, attacker, left_neighbor, None))

    defender = Species(body_size=6, traits=[SymbiosisTrait()])
    attacker = Species(traits=[CarnivoreTrait()])
    left_neighbor = Species(body_size=4)
    assert is_attackable(Situation(defender, attacker, left_neighbor, None))


def test_warning_call():
    """tests the Warning Call trait"""

    defender = Species(traits=[WarningCallTrait()])
    attacker = Species(traits=[CarnivoreTrait()])
    assert is_attackable(Situation(defender, attacker, None, None))

    defender = Species()
    attacker = Species(traits=[CarnivoreTrait()])
    left_neighbor = Species(traits=[WarningCallTrait()])
    assert not is_attackable(
        Situation(defender, attacker, left_neighbor, None))

    defender = Species()
    attacker = Species(traits=[CarnivoreTrait()])
    right_neighbor = Species(traits=[WarningCallTrait()])
    assert not is_attackable(
        Situation(defender, attacker, None, right_neighbor))
