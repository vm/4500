The purpose of this project was to implement is_attackable and write a
specification for a player in Evolution.

attack/attack.py - implements the is_attackable function
attack/situation.py - implements Situation, Role, and Species objects
attack/test_attack.py - tests for is_attackable
attack/trait.py - implements an object for each known Trait
player-interface.txt - specifies an implementation for a Player
xattack - script to determine if a defender is attackable in a JSON situation
run_tests.sh - runs the tests for the is_attackable functions
run_xattack_tests.sh - runs the tests for xattack
test - directory of tests for xattack

to use xattack, run:
./xattack < some-json-input > some-json-output

to run tests in test_attack.py, run:
./run_tests.sh

to run tests in /test, run:
./run_xattack_tests.sh

Read the code in the following order:
- attack/attack.py
- attack/situation.py
- attack/trait.py
- attack/test_attack.py
- xattack
- player-interface.txt
