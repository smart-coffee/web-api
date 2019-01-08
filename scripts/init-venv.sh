#!/bin/sh

python3.6 -m venv venv
if [[ "$?" = "127" ]]; then
    echo "Trying python3.7"
    python3.7 -m venv venv
fi
if [[ "$?" = "127" ]]; then
    echo "python3.6 or python3.7 is not installed."
    exit 1
fi

source venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
