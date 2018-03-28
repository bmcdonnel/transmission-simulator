#!/bin/bash

if [ ! -d 'venv' ]; then
  echo 'bootstrapping virtual environment'
  source bootstrap.sh
fi

source venv/bin/activate

python -m main "$@"

