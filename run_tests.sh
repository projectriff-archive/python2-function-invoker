#!/usr/bin/env bash

PYTHON=python

if !command -v $PYTHON &>/dev/null; then
    echo Python is not installed
fi

if ! command -v pip &>/dev/null; then
   echo "Installing pip"
   wget https://bootstrap.pypa.io/get-pip.py
   sudo $PYTHON get-pip.py
   sudo pip install -U pip
   rm get-pip.py
fi

if ! command -v virtualenv &>/dev/null; then
   echo "Installing virtualenv"
   sudo pip install -U virtualenv
fi

REQUIRED_PYTHON_VERSION=2.7
VENV_DIR=test_pyenv

virtualenv -q -p "python$REQUIRED_PYTHON_VERSION" $VENV_DIR
source $VENV_DIR/bin/activate
pip install -r invoker/requirements.txt

./setup.py test

deactivate

rm -rf $VENV_DIR

