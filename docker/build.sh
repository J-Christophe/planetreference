#!/bin/sh
docker build --no-cache=true --build-arg SSH_PRIVATE_KEY="`more ~/.ssh/id_rsa`" -t dev/planetreference .
