#!/bin/sh

# Start docker containers in background
docker-compose up -d

# Wait for them to start
sleep 5

# Initialize DB
source venv/bin/activate
cd src
python reset_database.py
cd ..
deactivate

# Stop containers running in background
docker-compose stop
