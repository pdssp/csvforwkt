#!/bin/sh
# csvForWKT - csvForWKT is a python script that creates a WKT-crs for some bodies from the solar system. The content that is filled in the WKT-crs comes from the report of IAU Working Group on Cartographic.
# Copyright (C) 2022 - CNES (Jean-Christophe Malapert for Pôle Surfaces Planétaires)
#
# This file is part of csvForWKT.
#
# csvForWKT is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v3  as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# csvForWKT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License v3  for more details.
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with csvForWKT.  If not, see <https://www.gnu.org/licenses/>.
set search
set ps

search=`docker images | grep dev/csvforwkt | wc -l`
if [ $search = 0 ];
then
	# only the heaader - no image found
	echo "Please build the image by running 'make docker-container-dev'"
	exit 1
fi

ps=`docker ps -a | grep develop-csvforwkt | wc -l`
if [ $ps = 0 ];
then
	echo "no container available, start one"
	docker run --name=develop-csvforwkt #\
		#-v /dev:/dev \
		#-v `echo ~`:/home/${USER} \
		#-v `pwd`/data:/srv/csvforwkt/data \
		#-p 8082:8082 \
		-it dev/csvforwkt /bin/bash
	exit $?
fi

ps=`docker ps | grep develop-csvforwkt | wc -l`
if [ $ps = 0 ];
then
	echo "container available but not started, start and go inside"
	docker start develop-csvforwkt
	docker exec -it develop-csvforwkt /bin/bash
else
	echo "container started, go inside"
	docker exec -it develop-csvforwkt /bin/bash
fi
