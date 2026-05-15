#!/bin/bash

# Tyhjennetään vanhat logit (valinnainen, älä käytä jos haluat tallentaa lokit)
: > logs/error.log

echo "Starting main process..."
python3 processes/main.py 

echo "Timeout reached. Exiting script."