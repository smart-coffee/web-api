# Backend Application for our IoT Coffeemachine

[![Build Status](https://travis-ci.com/smart-coffee/web-api.svg?branch=master)](https://travis-ci.com/smart-coffee/web-api)

* Python >= 3.6 required
* API-Documentation: [https://webapi-docs.tobias-blaufuss.de](https://webapi-docs.tobias-blaufuss.de)

## Initialization of the project (Development)

Initialize the project: `sh scripts/init.sh`. This will:

* ... initialize the virtual environment
* ... initialize `.env` files
* ... initialize `docker` containers (database)

## Start the app

* `sh scripts/app-start.sh`
* Go to [http://localhost:5000](http://localhost:5000)
* Try the login resource with the following credentials => admin:password
* You should receive a JWT Token, which you can use for other available resources that require a JWT Token.
* Use the token for the `/users/current` and you will receive all information about the current user account.

## Reset database
`sh scripts/init-database.sh`

## Docker

Start docker environment with `docker-compose up`. This will start the following containers:

* MySQL, Database Server (Host:3308, Network:3306)
* Adminer, Database Administration Tool (Host:8081, Network:8080)

Visit [http://localhost:8081](http://localhost:8081) and access the database with the credentials listed in `docker-compose.yml`. There should be **1 user in the `user` table** if you initialized the project correctly.

Example connection:

* server: mysql-dev
* user: admin
* password: admin
* database: cm_db

## PRODUCTION (Without docker)

* Start production server: `./uwsgi-start`
* Stop production server: `./uwsgi-stop`
* Ports should be changed in `uwsgi.ini` **AND** `src/.env`
