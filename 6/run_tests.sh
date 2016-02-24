#!/bin/sh
virtualenv -p python3 lvs-vignesh-venv
. lvs-vignesh-venv/bin/activate
pip install pytest
py.test test_player_proxy.py
# deactivate
# rm -r ./lvs-vignesh-venv
