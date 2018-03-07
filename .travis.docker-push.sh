#!/bin/bash		
		
set -o errexit
set -o nounset
set -o pipefail

version=`cat VERSION`

./build.sh latest
docker tag "projectriff/python2-function-invoker:latest" "projectriff/python2-function-invoker:${version}"
docker tag "projectriff/python2-function-invoker:latest" "projectriff/python2-function-invoker:${version}-ci-${TRAVIS_COMMIT}"

docker login -u "${DOCKER_USERNAME}" -p "${DOCKER_PASSWORD}"
docker push "projectriff/python2-function-invoker"
