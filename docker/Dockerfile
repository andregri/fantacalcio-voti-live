# Base image
FROM python:3.9-slim-bullseye

ENV DEBIAN_FRONTEND noninteractive

# Basic stuff
RUN apt-get update && \
    apt-get install -y vim git

# Install the `fantacalcio-voti-live` prerequisites
# * The PostgreSQL dev files
RUN apt-get install -y libpq-dev
# * nodejs and protobufjs
RUN apt install -y nodejs
RUN apt install -y npm
RUN npm cache clean --force

# Get `fantacalcio-voti-live`
RUN git clone -v https://github.com/FabioLuporini/fantacalcio-voti-live.git

# Install `fantacalcio-voti-live`
RUN python3 -m venv /venv && \
    /venv/bin/pip install -r fantacalcio-voti-live/requirements.txt && \
    rm -rf ~/.cache/pip

# Install JS requirements
RUN cd fantacalcio-voti-live && \
    npm install protobufjs && \
    cd ..

# Install more dev utils
RUN /venv/bin/pip install ipython && \
    rm -rf ~/.cache/pip

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
