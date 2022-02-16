#!/bin/bash

DOCKERNETWORK=mcde
DOCKERVOLUME=~/volume_mcde
IMAGE_NAME=mcde-base
DEFAULTPASS=123

cont_name="$1"
proxy_host="$2"
proxy_port="$3"

if ! docker image inspect $IMAGE_NAME >/dev/null 2>/dev/null; then
  docker build -t $IMAGE_NAME .
fi

docker run -d --privileged --name "$cont_name" \
-e USER=user -e PASSWORD="$DEFAULTPASS" -e MCDE_PROXY_HOST="$proxy_host" -e MCDE_PROXY_PORT="$proxy_port" \
--expose 80 --expose 5900 --network "$DOCKERNETWORK" \
-v /dev/shm:/dev/shm -v $DOCKERVOLUME:/home/user/Desktop/volume \
$IMAGE_NAME
