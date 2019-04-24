#!/bin/sh

DB_USER=${DB_USER:-$MYSQL_USER}
DB_PW=${DB_PW:-$MYSQL_PASSWORD}
DB_NAME=${DB_NAME:-$MYSQL_DATABASE}
DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-"3306"}
APP_PROCESSES=${APP_PROCESSES:-"4"}
APP_THREADS=${APP_THREADS:-"2"}

echo "Working directory: $WORK_DIR"
echo "Source directory: $SRC_DIR"
echo "App starts on host:'$APP_HOST' on port:'$APP_PORT'"
echo "For ports outside the container, checkout the 'docker-compose.yml' file."

if [[ ! -f "cert.pem" ]]; then
	echo "Linking cert.pem"
	ln -s /ssl/cert.pem $SRC_DIR/$CERT_FILE
fi
if [[ ! -f "privkey.pem" ]]; then
	echo "Linking privkey.pem"
	ln -s /ssl/privkey.pem $SRC_DIR/$KEY_FILE
fi

# Create uwsgi configuration
cat <<EOF >$WORK_DIR/uwsgi.ini
[uwsgi]
https = $APP_HOST:$APP_PORT,src/$CERT_FILE,src/$KEY_FILE
chdir = src
socket = %n.sock
manage-script-name = true
mount =	/api=app.py
callable = $APP_CALLABLE

threads = $APP_THREADS
processes = $APP_PROCESSES
master = true
safe-pidfile = %n.pid
EOF

# Create .env file
cat <<EOF >$SRC_DIR/.env
MODE=$MODE

CERT_FILE=$CERT_FILE
KEY_FILE=$KEY_FILE

# Customize as needed
DB_USER=$DB_USER
DB_PW=$DB_PW
DB_HOST=$DB_HOST
DB_NAME=$DB_NAME
DB_PORT=$DB_PORT

APP_HOST=$APP_HOST
APP_PORT=$APP_PORT
SECRET_KEY=$SECRET_KEY
APP_URL_PREFIX=$APP_URL_PREFIX

# This path should conform with the path that is provided by uwsgi.ini"
SWAGGER_BASE_URL=$SWAGGER_BASE_URL
EOF

# Start app
if [[ "$FLASK_ENV" = "production" ]]; then
	echo "Production mode."
	sh uwsgi-start
elif [[ "$FLASK_ENV" = "development" ]]; then
	echo "Development mode."
	cd "$SRC_DIR"
	python app.py
else
	echo "Unknown FLASK_ENV: $FLASK_ENV"
	exit 1
fi
