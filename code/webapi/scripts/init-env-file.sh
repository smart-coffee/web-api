#!/bin/bash

init_prod_env_file() {
    local_mode='prod'
    echo "MODE=$local_mode" > .env

    echo >> .env
    echo "CERT_FILE=cert.pem" >> .env
    echo "KEY_FILE=privkey.pem" >> .env

    echo >> .env
    echo "# Customize as needed" >> .env
    echo "DB_USER=" >> .env
    echo "DB_PW=" >> .env
    echo "DB_HOST=" >> .env
    echo "DB_NAME=" >> .env
    echo "DB_PORT=" >> .env

    echo >> .env
    echo "APP_HOST=" >> .env
    echo "APP_PORT=" >> .env
    echo "SECRET_KEY=" >> .env
    echo "APP_URL_PREFIX=" >> .env

    echo >> .env
    echo "# This path should conform with the path that is provided by uwsgi.ini" >> .env
    echo "SWAGGER_BASE_URL=/api" >> .env
}

init_dev_env_file() {
    local_mode='dev'
    echo "MODE=$local_mode" > "$location/.env"

    echo >> "$location/.env"
    echo "# Should be empty in $local_mode environment" >> "$location/.env"
    echo "CERT_FILE=" >> "$location/.env"

    echo >> "$location/.env"
    echo "# Should be empty in $local_mode environment" >> "$location/.env"
    echo "KEY_FILE=" >> "$location/.env"

    echo >> "$location/.env"
    echo "# Customize as needed" >> "$location/.env"
    echo "DB_USER=admin" >> "$location/.env"
    echo "DB_PW=admin" >> "$location/.env"
    echo "DB_HOST=localhost" >> "$location/.env"
    echo "DB_NAME=cm_db" >> "$location/.env"
    echo "DB_PORT=3308" >> "$location/.env"

    echo >> "$location/.env"
    echo "APP_HOST=localhost" >> "$location/.env"
    echo "APP_PORT=5000" >> "$location/.env"
    echo "SECRET_KEY=XLrIjHvKsQskA7m" >> "$location/.env"
    echo "APP_URL_PREFIX=" >> "$location/.env"

    echo >> "$location/.env"
    echo "# Should be empty in $local_mode environment" >> "$location/.env"
    echo "SWAGGER_BASE_URL=" >> "$location/.env"

}

init_test_env_file() {
    local_mode='test'
    echo "MODE=$local_mode" > appd/test/.env

    echo >> appd/test/.env
    echo "# Should be empty in $local_mode environment" >> appd/test/.env
    echo "CERT_FILE=" >> appd/test/.env

    echo >> appd/test/.env
    echo "# Should be empty in $local_mode environment" >> appd/test/.env
    echo "KEY_FILE=" >> appd/test/.env

    echo >> appd/test/.env
    echo "# Should be empty in $local_mode environment" >> appd/test/.env
    echo "DB_USER=" >> appd/test/.env
    echo "DB_PW=" >> appd/test/.env
    echo "DB_HOST=" >> appd/test/.env
    echo "DB_NAME=" >> appd/test/.env
    echo "DB_PORT=" >> appd/test/.env

    echo >> appd/test/.env
    echo "APP_HOST=" >> appd/test/.env
    echo "APP_PORT=" >> appd/test/.env
    echo "SECRET_KEY=" >> appd/test/.env
    echo "APP_URL_PREFIX=" >> appd/test/.env

    echo >> appd/test/.env
    echo "# Should be empty in $local_mode environment" >> appd/test/.env
    echo "SWAGGER_BASE_URL=" >> appd/test/.env

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
    #init_test_env_file
elif [[ "$mode" = "test" ]]; then
    init_test_env_file "$location"
else
    echo "Unknown mode: $mode"
    exit 1
fi