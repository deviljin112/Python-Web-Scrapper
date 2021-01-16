#!/bin/bash

## Installs all dependencies for the app to work
sudo apt install software-properties-common -y
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install python3-venv -y
sudo apt install sqlite3 -y
sudo apt install git -y

## Enters the repo folder
cd ../deploy_code/

## Creates and activates python Venv
python3 -m venv venv
source venv/bin/activate

## Installs all dependencies for Flask and App to run
python3 -m pip install -r requirements.txt
python3 setup.py build
python3 setup.py install

# Exports the current path to Python to run tests on
export PYTHONPATH=$PWD/project/

# Creates Database
python3 create_db.py

## Exports the correct Flask Environment
export FLASK_APP=project

## User prompt to run the app
echo "======================================"
echo "Flask Application ready for deployment"
echo "Use 'flask run' to run the app."
echo "It is recommended to run 'tmux'"
echo "See README for production deployment"
echo "======================================"
