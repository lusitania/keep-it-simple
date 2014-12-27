#!/bin/bash
# Provide zmq libraries
sudo apt-get install libzmq3-dev

# Provide Python zmq wrapper
virtualenv3 .env
. .env/bin/activate
pip3 -r zmq-one-off-handshake.pip
