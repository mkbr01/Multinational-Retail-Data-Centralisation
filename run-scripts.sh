#!/bin/bash

# Define the path to your virtual environment
VENV_PATH="/myvenv"

# Execute database_utils.py
"${VENV_PATH}/bin/python" database_utils.py

# Execute data_extraction.py
"${VENV_PATH}/bin/python" data_extraction.py

# Execute data_cleaning.py
"${VENV_PATH}/bin/python" data_cleaning.py
