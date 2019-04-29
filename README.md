# Backend Application for our IoT Coffeemachine

[![Build Status](https://travis-ci.com/smart-coffee/web-api.svg?branch=master)](https://travis-ci.com/smart-coffee/web-api)
[![License](https://img.shields.io/github/license/smart-coffee/web-api.svg)](https://opensource.org/licenses/MIT)

* Python >= 3.6 required
* API-Documentation: [https://webapi-docs.tobias-blaufuss.de](https://webapi-docs.tobias-blaufuss.de)

## Development

### Initialization of the project

Initialize the project: `sh scripts/init.sh`. This will:

* ... initialize the virtual environment
* ... initialize `.env` files
* ... initialize `docker` containers (database)

### Start and test the app

* `sh scripts/app-start.sh`
* Go to [http://localhost:5000](http://localhost:5000)
* Try the login resource with the following credentials => admin:password
* You should receive a JWT Token, which you can use for other available resources that require a JWT Token.
* Use the token for the `/users/current` and you will receive all information about the current user account.

### Reset database

`sh scripts/init-database.sh`

## Production: Docker

You have to create the following files:

* ./docker/db/env/.env
* ./docker/db/conf/config-file.cnf
* ./docker/web-api/env/.env

Have a look at `docker-compose.prod.yml` and follow the hints in the line comments about the content of the created .env and cnf files.

Start the services with `docker-compose -f docker-compose.prod.yml --build -d`

## Production: Without docker

### Setup

* Initialize virtual environment: `sh scripts/init-venv.sh`
* Initialize environment files: `sh scripts/init-env.sh prod src`
* Configure src/.env according to your production environment
* Initialize uwsgi.ini: `sh scripts/init-uwsgi-local src/.env`

### Start

* Start production server: `./uwsgi-start`
* Stop production server: `./uwsgi-stop`

### Important

If you change ANYTHING in src/.env, you should run `./scripts/init-uwsgi-local src/.env` again!
