#!/bin/bash

# Note 'python' aliased to 2.7 on MacOS Catalina for backwards compatibility bu NOT recommended
# The commands below have been adapted for python3/pip3 instead

# Create and enable a virtual environment
python3 -m venv env
source env/bin/activate

# Upgrade pip and install required packages
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Create a .env file from the .env.template
cp -n .env.template .env
