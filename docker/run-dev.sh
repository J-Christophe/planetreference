#!/bin/sh
set search
set ps

search=`docker images | grep dev/planetreference | wc -l`
if [ $search = 0 ];
then
	# only the heaader - no image found
	echo "Please build the image by running 'make docker-container-dev'"
	exit 1
fi

ps=`docker ps -a | grep develop-planetreference | wc -l`
if [ $ps = 0 ];
then
	echo "no container available, start one"
	docker run --name=develop-planetreference \
		-v /dev:/dev \
		-v `echo ~`:/home/${USER} \
		-v `pwd`/data:/srv/planetreference/data \
		-p 8082:8082 \
		-it dev/planetreference /bin/bash
	exit $?
fi

ps=`docker ps | grep develop-planetreference | wc -l`
if [ $ps = 0 ];
then
	echo "container available but not started, start and go inside"
	docker start develop-planetreference
	docker exec -it develop-planetreference /bin/bash
else
	echo "container started, go inside"
	docker exec -it develop-planetreference /bin/bash
fi
