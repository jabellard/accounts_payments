#!/bin/bash

# Script to destroy sqlitedb and migration files

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

delete_db_files(){
  echo "Deleting files..."
  rm ${PROJECT_ROOT}db.sqlite3
  find ${PROJECT_ROOT} -path "*/migrations/*.py" -not -name "__init__.py" -delete
  find ${PROJECT_ROOT} -path "*/migrations/*.pyc"  -delete
  echo "Done."
}

while true; do
    read -p "Are you sure you want to delete the database files[y/n]?" yn
    case $yn in
        [Yy]* ) delete_db_files; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
