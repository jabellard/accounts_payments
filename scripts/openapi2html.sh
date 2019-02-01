#!/bin/bash

# Script to generate a stand-alone html file from an openapi spec

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
OPENAPI_TEMPLATE_ROOT=${PROJECT_ROOT}/apps/documentation/templates/openapi/

openapi2html(){
  echo "Creating standalone html..."
  redoc-cli bundle  ${OPENAPI_ROOT}openapi.yaml &&
  mv redoc-static.html ${OPENAPI_ROOT}openapi.html &&
  cp -f ${OPENAPI_ROOT}openapi.html ${OPENAPI_TEMPLATE_ROOT}
  echo "Done."
}

openapi2html
