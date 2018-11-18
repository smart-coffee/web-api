#!/bin/sh

# Initialize virtual environment
sh ./scripts/init-venv.sh

# Initialize .env file
sh ./scripts/init-env-file.sh dev src

# Initialize database
sh ./scripts/init-database.sh