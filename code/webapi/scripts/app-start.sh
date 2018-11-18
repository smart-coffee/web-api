#!/bin/sh

docker-compose up -d
source venv/bin/activate
cd src
python app.py