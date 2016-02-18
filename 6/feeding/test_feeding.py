"""
FOR ALL TEST HUNGRY/NOT-HUNGRY OF EACH
ADD TESTS THAT PLAYER DOESN'T VIOLATE BEHAVIORAL CONTRACTS

Fat tissue tests
    - one species with fat tissue --> goes first
    - more than one with fat tissue --> largest need for fat tissue food
    - more than one with fat tissue, same need --> ordering
    - more than one with fat tissue, same need, ordering tie --> board order

Vegetarian
    - one vegetarian species --> goes first
    - multiple vegetarian species --> largest one (?) goes
    - mutliple veggie with same size --> ?

Carnivore
    - largest goes --> attacks largest species that can be attacked
    - largest goes, tie in largest to attack --> first in opponents
    - largest goes, tie in largest to attack, tie inside player
        --> first in opponent's board order

Other
    - player will not attack it's own species?
"""
