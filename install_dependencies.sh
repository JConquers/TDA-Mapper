#!/bin/bash

# Check if virtualenv is installed, if not install it
if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found, installing it..."
    pip install virtualenv
fi

# Create virtual environment
virtualenv env

# Activate virtual environment
source env/bin/activate

# Install packages
pip install -r dependencies.txt

echo "All dependencies installed."
