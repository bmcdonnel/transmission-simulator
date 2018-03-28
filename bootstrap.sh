#!/bin/bash

# create a virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# these packages will be installed to the venv, and will not affect the system at large
pip install pylint
pip install nose
pip install mock
pip install matplotlib
