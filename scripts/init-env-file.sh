#!/bin/bash

init_prod_env_file() {
    local_mode='prod'
    export MODE=$local_mode
    export CERT_FILE=${CERT_FILE:-"cert.pem"}
    export KEY_FILE=${KEY_FILE:-"privkey.pem"}
    export SWAGGER_BASE_URL=${SWAGGER_BASE_URL:-"/api"}

    envsubst < docker/templates/.env.template | cat > $location/.env
}

init_dev_env_file() {
    local_mode='dev'
    export MODE=$local_mode
    export DB_USER=admin
    export DB_PW=password
    export DB_HOST=localhost
    export DB_NAME=cm_db
    export DB_PORT=3308
    export APP_HOST=localhost
    export APP_PORT=5000
    export SECRET_KEY=XLrIjHvKsQskA7m

    envsubst < docker/templates/.env.template | cat > $location/.env
}

mode=$1
location=$2

# SCRIPT

if [[ -z "$mode" ]]; then
    echo "Provide one of these modes as first parameter: dev, prod, test"
    exit 1
fi

if [[ ! -d "$location" ]]; then
    echo "Provide a valid destination directory for generating the .env file as second parameter."
    exit 2
fi

echo "Selected mode: $mode"
echo "Destination directory: $location"

if [[ "$mode" = "prod" ]]; then
    init_prod_env_file "$location"
elif [[ "$mode" = "dev" ]]; then
    init_dev_env_file "$location"
else
    echo "Unknown mode: $mode"
    exit 1
fi