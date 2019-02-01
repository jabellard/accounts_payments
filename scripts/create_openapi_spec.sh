#!/bin/bash

# Script generate openapi spec from yaml fragments

# Named Arguments---------------------------------------------------
# -p : Root directory of the django project, defaults to './'

PROJECT_ROOT=''

while getopts ":p:" opt; do
  case $opt in
    p) PROJECT_ROOT="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ -z "$PROJECT_ROOT" ]
then
      PROJECT_ROOT=./
fi

OPENAPI_ROOT=${PROJECT_ROOT}/docs/openapi/

create_openapi_spec(){
  echo "Creating spec..."
  json-refs resolve -f  -y ${OPENAPI_ROOT}index.yaml > ${OPENAPI_ROOT}openapi.yaml &&
  echo "Done."
}

create_openapi_spec
