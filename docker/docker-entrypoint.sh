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

if [[ -f /ssl/cert.pem && ! -f "$SRC_DIR/$CERT_FILE" ]]; then
	echo "Linking $CERT_FILE"
	ln -s /ssl/cert.pem $SRC_DIR/$CERT_FILE
fi
if [[ -f /ssl/privkey.pem && ! -f "$SRC_DIR/$KEY_FILE" ]] ; then
	echo "Linking $KEY_FILE"
	ln -s /ssl/privkey.pem $SRC_DIR/$KEY_FILE
fi

# Create uwsgi configuration
envsubst < ${TEMPLATE_DIR}/uwsgi.ini.template | cat > $WORK_DIR/uwsgi.ini

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
