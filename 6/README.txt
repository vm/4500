The purpose of this project was to implement get_feeding_result, and write a
memo describing the dealer's usage of is_attackable within Evolution game.

feed.pdf - memo describing dealer's usage of is_attackable

feeding/attack.py - is_attackable function
feeding/feeding.py - Feeding class, implementation for game player,
                     and get_feeding_result function
feeding/player.py - BasePlayer class
feeding/result.py - namedtuples for each feeding result type
feeding/situation.py - Situation and Role classes
feeding/species.py - Species class
feeding/trait.py - base Trait class and subclasses for each specific trait
feeding/utils.py - utility functions for use throughout the project

feeding/test/test_attack.py - tests for is_attackable
feeding/test/test_feeding.py - tests for get_feeding_result
feeding/test/json/*.json - input and output files for testing xfeed

compile - script to "compile" xfeed
xfeed - script to determine the next species to feed given in a JSON feeding
run_tests.sh - runs all unit tests

to use xfeed, run:
./xfeed < some-json-input > some-json-output
