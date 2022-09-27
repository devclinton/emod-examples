REGISTRY=idm-docker-staging.packages.idmod.org/idmtools
TAG_NAME=idmtools-rockylinux-emodpy-malaria
TAG_VERSION=2.3.6


build:  ## Build the image
	docker build . -t ${REGISTRY}/${TAG_NAME}:${TAG_VERSION}

publish: build  ## Publish image
	docker push ${REGISTRY}/${TAG_NAME}:${TAG_VERSION}

push: publish  ## Alias for publish
