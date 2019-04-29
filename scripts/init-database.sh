#!/bin/sh

SERVICE=mysql-dev

# Start docker containers in background
docker-compose up -d $SERVICE

# Wait for them to start
sleep 10

# Initialize DB
source venv/bin/activate
cd src
python reset_database.py
cd ..
deactivate

# Stop containers running in background
docker-compose stop $SERVICE
