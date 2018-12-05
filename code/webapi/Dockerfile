FROM python:3.7-alpine

RUN apk --update add gcc libffi-dev musl-dev openssl-dev linux-headers

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && pip install -r requirements.txt

# add app
COPY ./src /usr/src/app

COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]