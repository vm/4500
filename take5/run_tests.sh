virtualenv lvs-vignesh-venv
source lvs-vignesh-venv/bin/activate # something here w/ python3
pip install pytest
py.test test_dealer.py
deactivate
rm -r ./lvs-vignesh-venv
