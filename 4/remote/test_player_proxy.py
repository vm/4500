import player_proxy as proxy

"""
read
- create TCP socket and write
- valid
    - {}, [], 1, true
    - start-round, take-turn, choose
- long waits
- out of order action

is_valid_json
- valid
- invalid

get_reply
- valid
    - check equal to appro method
- invalid
    - bad msg fmt, shutdown
    - timing violation false, shutdown

start_round
- check player gets hand

take_turn
- check that right card returned

choose
- check it is 0

send
- make TCP socket and check that the input is the same as output on other side
"""

def test_is_valid_json():
    assert proxy.is_valid_json('[]')
    assert proxy.is_valid_json('{}')
    assert proxy.is_valid_json('true')
    assert proxy.is_valid_json('"\"\""')
    assert proxy.is_valid_json('"{\"ok: [{}, {}]}"')

    assert not proxy.is_valid_json('[')
    assert not proxy.is_valid_json('{')

    lcard = [[0, 0], [1, 1], [2, 2]]
    assert proxy.is_valid_json('["start-round", {}]'.format(lcard))

    deck = [lcard, lcard, lcard]
    assert proxy.is_valid_json('["take-turn", {}]'.format(deck))
    assert proxy.is_valid_json('["choose", {}]'.format(deck))

    assert not proxy.is_valid_json('["start-rou')
    assert not proxy.is_valid_json('["start-round: [')
