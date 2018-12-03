#!/bin/sh

echo "App starts on host:'$APP_HOST' on port:'$APP_PORT'"
echo "Mode: $MODE"
echo "For ports outside the container, checkout the 'docker-compose.yml' file."
python app.py