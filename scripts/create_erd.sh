#!/bin/bash

# Script to create Entity Relationship Diagram (ERD) for the selected models

# Named Arguments---------------------------------------------------
# -p : Root directory of the django project, defaults to './'
# -o : Output format for the generated file, defaults to 'png'

PROJECT_ROOT=''
OUTPUT_FORMAT=''

while getopts ":p:o:" opt; do
  case $opt in
    p) PROJECT_ROOT="$OPTARG"
    ;;
    o) OUTPUT_FORMAT="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ -z "$PROJECT_ROOT" ]
then
      PROJECT_ROOT=./
fi

if [ -z "$OUTPUT_FORMAT" ]
then
      OUTPUT_FORMAT=png
fi

 INCLUDE_MODELS_PATH=${PROJECT_ROOT}/scripts/INCLUDE_MODELS
 INCLUDE_MODELS="$(cat ${INCLUDE_MODELS_PATH})"

create_erd(){
  echo "Generating ERD..."
  python ${PROJECT_ROOT}manage.py graph_models  -o ${PROJECT_ROOT}/docs/db/erd.${OUTPUT_FORMAT} && #-I ${INCLUDE_MODELS}
  echo "Generated ERD is located at '${PROJECT_ROOT}/docs/db/erd.${OUTPUT_FORMAT}'"
 }

create_erd
