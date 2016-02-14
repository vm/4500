virtualenv -p python3 lvs-vignesh-venv
source lvs-vignesh-venv/bin/activate
pip install pytest
py.test attack/test_attack.py
deactivate
rm -r ./lvs-vignesh-venv
