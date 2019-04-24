FROM python:3.7-alpine

# Install general dependencies
RUN apk --update add gcc libffi-dev musl-dev openssl-dev linux-headers gettext

# Setup general environment
ENV WORK_DIR /usr/src/app
ENV SRC_DIR ${WORK_DIR}/src
ENV APP_CALLABLE FLASK_APP
ENV TEMPLATE_DIR /usr/templates

# Configure working directory
WORKDIR ${WORK_DIR}

# Install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && pip install -r requirements.txt

# Add complete app
COPY src ${SRC_DIR}

# Add template files
COPY docker/templates ${TEMPLATE_DIR}

# Add start script for uwsgi server
COPY uwsgi-start ${WORK_DIR}/uwsgi-start

# Configure entry point
COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]
