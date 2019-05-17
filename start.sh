#!/usr/bin/env bash
set -eu

export FLASK_APP=start.py

if [[ "$#" -ne 1 ]]; then
  echo "Must have 1 argument"
  exit 1
fi

case "$1" in 
  dev)
    export FLASK_ENV=development
    ;;
  prod)
    unset FLASK_ENV
    ;;
  *)
    echo "Use either 'prod' or 'dev'"
    exit 1
esac


pipenv run flask run