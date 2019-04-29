#!/bin/sh

export DB_USER=${DB_USER:-$MYSQL_USER}
export DB_PW=${DB_PW:-$MYSQL_PASSWORD}
export DB_NAME=${DB_NAME:-$MYSQL_DATABASE}
export DB_HOST=${DB_HOST:-"localhost"}
export DB_PORT=${DB_PORT:-"3306"}
export APP_PROCESSES=${APP_PROCESSES:-"4"}
export APP_THREADS=${APP_THREADS:-"2"}

echo "Working directory: $WORK_DIR"
echo "Source directory: $SRC_DIR"
echo "App starts on host:'$APP_HOST' on port:'$APP_PORT'"
echo "For ports outside the container, checkout the 'docker-compose.yml' file."

if [[ -f /ssl/cert.pem && ! -f "$SRC_DIR/$CERT_FILE" ]]; then
	echo "Linking $CERT_FILE"
	ln -s /ssl/cert.pem $SRC_DIR/$CERT_FILE
fi
if [[ -f /ssl/privkey.pem && ! -f "$SRC_DIR/$KEY_FILE" ]] ; then
	echo "Linking $KEY_FILE"
	ln -s /ssl/privkey.pem $SRC_DIR/$KEY_FILE
fi

# Create uwsgi configuration
UWSGI_HTTPS_TEMPLATE=$TEMPLATE_DIR/uwsgi-docker.https.ini.template
UWSGI_HTTP_TEMPLATE=$TEMPLATE_DIR/uwsgi-docker.http.ini.template

export MOUNT_URL=${SWAGGER_BASE_URL:-"/"}
if [[ -z $MOUNT_URL ]]; then
    export MOUNT_URL="/"
fi

if [[ ! -z "$CERT_FILE" && ! -z "$KEY_FILE" ]]; then
    echo "uWSGI HTTPS enabled. Please check your certificates."
    envsubst < $UWSGI_HTTPS_TEMPLATE | cat > $WORK_DIR/uwsgi.ini
else
    echo "uWSGI HTTP enabled."
    envsubst < $UWSGI_HTTP_TEMPLATE | cat > $WORK_DIR/uwsgi.ini
fi

# Create .env file
envsubst < ${TEMPLATE_DIR}/.env.template | cat > $SRC_DIR/.env

# Start app
if [[ "$FLASK_ENV" = "production" ]]; then
	echo "Production mode."
	sh uwsgi-start
elif [[ "$FLASK_ENV" = "development" ]]; then
	echo "Development mode."
	cd "$SRC_DIR"
	python app.py
elif [[ "$FLASK_ENV" = "testing" ]]; then
	echo "Testing mode."
	echo "Run tests here!"
	cat src/.env
	cat uwsgi.ini
else
	echo "Unknown FLASK_ENV: $FLASK_ENV"
	exit 1
fi
