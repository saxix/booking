---
title: Docker
---


To locally build your docker image just run:


    	DOCKER_BUILDKIT=1 docker build \
			--target dist \	
			-t booking:local \
			-f docker/Dockerfile .
