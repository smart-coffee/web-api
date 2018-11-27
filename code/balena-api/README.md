# Simple Balena API
Small API that uses balena-sdk to get information about registered devices.

## Docker usage
* Start development container: `docker-compose up webapi-dev`
* Start production container: `docker-compose up webapi-prod`

## Local installation and usage
* Installation: `sh scripts/init`
* Configure your environment variables: `src/.env`
* Start app in **development** mode: `sh scripts/start-app`
* Start app in **production** mode: `sh scripts/start-app prod`