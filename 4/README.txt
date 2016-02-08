The purpose of this project was to host 6Nimmt! over TCP and to
introduce ourselves to Evolution

remote/player_proxy.py: implements a TCP socket proxy for a player
remote/test_player_proxy.py: tests for player proxy
test/*-in.json: nth test input
test/*-out.json: nth test output
evolution/evolution-framework.txt: data definitions and ambiguities for evolution

To start the proxy with the default settings: sh remote-client
To run tests: sh run_tests.sh
