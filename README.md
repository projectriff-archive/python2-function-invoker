# Python2 Function Invoker [![Build Status](https://travis-ci.org/projectriff/python2-function-invoker.svg?branch=master)](https://travis-ci.org/projectriff/python2-function-invoker)

## About


⚠️ **This function invoker is deprecated. Please use the [Python 3 function invoker](https://github.com/projectriff/python3-function-invoker) instead.**


The Python 2 function invoker, as the name implies, supports functions written in Python 2.  The invoker supports function arguments of type `str` or `dict`, determined by the message's `Content-Type` header.
For messages containing `Content-Type:application/json`, the bytes payload is converted to a dict. Reflection is used to convert the return value. Currently only UTF-8 encoding is supported.

Supported Python Version: 2.7.x

## Install as a riff invoker

```bash
riff invokers apply -f python2-invoker.yaml
```

## Running Tests

This script will install a virtual environment for python 2.7 and run the tests.

```bash
./run_tests.sh
```

## Update grpc modules

```bash
./setup.py grpc
```

## Build the docker image

```bash
./build.sh
```

## Running test functions in riff

```bash
./build.sh
riff create python tests/functions -n upper -p grpc --handler handle
riff publish -i upper -r -d "hello, world"
```

## riff Commands

- [riff init python2](#riff-init-python2)
- [riff create python2](#riff-create-python2)

<!-- riff-init -->

### riff init python2

Initialize a python2 function

#### Synopsis

Generate the function based on the function source code specified as the filename, handler
name, artifact and version specified for the function image repository and tag.

For example, type:

    riff init python2 -i words -n uppercase --handler=process

to generate the resource definitions using sensible defaults.


```
riff init python2 [flags]
```

#### Options

```
      --handler string   the name of the function handler (default "{{ .FunctionName }}")
  -h, --help             help for python2
```

#### Options inherited from parent commands

```
  -a, --artifact string          path to the function artifact, source code or jar file
      --config string            config file (default is $HOME/.riff.yaml)
      --dry-run                  print generated function artifacts content to stdout only
  -f, --filepath string          path or directory used for the function resources (defaults to the current directory)
      --force                    overwrite existing functions artifacts
  -i, --input string             the name of the input topic (defaults to function name)
      --invoker-version string   the version of the invoker to use when building containers
  -n, --name string              the name of the function (defaults to the name of the current directory)
  -o, --output string            the name of the output topic (optional)
  -u, --useraccount string       the Docker user account to be used for the image repository (default "current OS user")
  -v, --version string           the version of the function image (default "0.0.1")
```

#### SEE ALSO

* [riff init](https://github.com/projectriff/riff/blob/master/riff-cli/docs/riff_init.md)	 - Initialize a function


<!-- /riff-init -->

<!-- riff-create -->

### riff create python2

Create a python2 function

#### Synopsis

Create the function based on the function source code specified as the filename, handler
name, artifact and version specified for the function image repository and tag.

For example, type:

    riff create python2 -i words -n uppercase --handler=process

to create the resource definitions, and apply the resources, using sensible defaults.


```
riff create python2 [flags]
```

#### Options

```
      --handler string     the name of the function handler (default "{{ .FunctionName }}")
  -h, --help               help for python2
      --namespace string   the namespace used for the deployed resources (defaults to kubectl's default)
      --push               push the image to Docker registry
```

#### Options inherited from parent commands

```
  -a, --artifact string          path to the function artifact, source code or jar file
      --config string            config file (default is $HOME/.riff.yaml)
      --dry-run                  print generated function artifacts content to stdout only
  -f, --filepath string          path or directory used for the function resources (defaults to the current directory)
      --force                    overwrite existing functions artifacts
  -i, --input string             the name of the input topic (defaults to function name)
      --invoker-version string   the version of the invoker to use when building containers
  -n, --name string              the name of the function (defaults to the name of the current directory)
  -o, --output string            the name of the output topic (optional)
  -u, --useraccount string       the Docker user account to be used for the image repository (default "current OS user")
  -v, --version string           the version of the function image (default "0.0.1")
```

#### SEE ALSO

* [riff create](https://github.com/projectriff/riff/blob/master/riff-cli/docs/riff_create.md)	 - Create a function (equivalent to init, build, apply)


<!-- /riff-create -->
