#!/bin/bash

version=${1:-`cat VERSION`}

docker build . -t projectriff/python2-function-invoker:$version
