# envs to set before use this script
.ONESHELL:
DOCKER_IMAGE_NAME?=saxix/booking

CMD?=run
VERSION?=dev
STAGE?=dist

RUN_OPTIONS?=
BUILD_OPTIONS?=

.PHONY: help runlocal tests
.DEFAULT_GOAL := help


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


.build:
	DOCKER_BUILDKIT=1 cd .. && docker build \
			--target ${STAGE} \
			${BUILD_OPTIONS} \
			-t ${DOCKER_IMAGE} \
			-f docker/Dockerfile .
	docker images | grep "${DOCKER_IMAGE_NAME}"
	docker inspect ${DOCKER_IMAGE} | jq -r '.[0].Config.Labels'

build:
	DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:latest \
	$(MAKE) .build ## build image

.build-stage:
	DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:latest-${STAGE} \
	$(MAKE) .build

base_os:
	STAGE=base_os $(MAKE) .build-stage

builder:
	STAGE=builder $(MAKE) .build-stage

tests:
	STAGE=tests $(MAKE) .build-stage

production:
	STAGE=production $(MAKE) .build-stage

dist:
	STAGE=dist $(MAKE) .build-stage


step1: base_os
step2: builder
step3: tests
step4: production
step5: dist

build1: base_os
build2: builder
build3: tests
build4: production
build5: dist

.run:
	cd .. && docker run \
	 		--rm \
			-p 8001:8000 \
			-e DATABASE_URL="${DATABASE_URL}" \
			-e DEBUG="1" \
			-e SECRET_KEY=liujhljhlkjhlkjhlkj \
			-e SOCIAL_AUTH_REDIRECT_IS_HTTPS="False" \
			-e GOOGLE_CLIENT_ID="${GOOGLE_CLIENT_ID}" \
			-e GOOGLE_CLIENT_SECRET="${GOOGLE_CLIENT_SECRET}" \
			-e SUPERUSERS="${SUPERUSERS}" \
			${RUN_OPTIONS} \
			-t ${DOCKER_IMAGE} \
			${CMD}

run:
	DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:latest \
 	STAGE='dist' \
 	CMD='run' \
	$(MAKE) .run

.run-step:
	DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:latest-${STAGE} \
	RUN_OPTIONS="-it" \
 	CMD='/bin/bash' \
	$(MAKE) .run



run1:
	STAGE=base_os \
	$(MAKE) .run-step

run2:
	STAGE=builder \
	$(MAKE) .run-step

run3:
	STAGE=tests \
	$(MAKE) .run-step

run4:
	STAGE=production \
	$(MAKE) .run-step

run5:
	STAGE=dist \
	$(MAKE) .run-step

all: step1 step2 step3 step4 step5


.shell:
	RUN_OPTIONS=-it \
	CMD=/bin/bash \
	$(MAKE) .run

shell1:
	DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:latest-base_os \
	$(MAKE) .shell

shell2:
	DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:latest-builder \
	$(MAKE) .shell

shell3:
	DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:latest-tests \
	$(MAKE) .shell

shell4:
	DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:latest-production \
	$(MAKE) .shell

shell5:
	DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:latest \
	$(MAKE) .shell

push:
	docker push ${DOCKER_IMAGE_NAME}:latest
	docker push ${DOCKER_IMAGE_NAME}:main
	railway up
