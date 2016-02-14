The purpose of this project was to implement is_attackable and write a
specification for a player in Evolution.

attack/attack.py - implements the is_attackable function
attack/situation.py - implements Situation, Role, and Species objects
attack/test_attack.py - tests for is_attackable
attack/trait.py - implements an object for each known Trait
player-interface.txt - specifies an implementation for a Player
xattack - script to determine if a defender is attackable in a JSON situation

to use xattack, run:
./xattack < some-json-input > some-json-output

to run tests in test_attack, run:
./run_tests.sh

Read the code in the following order:
- attack/attack.py
- attack/situation.py
- attack/trait.py
- attack/test_attack.py
- xattack
- player-interface.txt
