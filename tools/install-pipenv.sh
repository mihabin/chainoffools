#!/usr/bin/env bash

# requires pyenv to be installed and sourceable
# first argument should be the PYTHON_VERSION to isntall pipenv to

if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi

pyenv shell $1

pip install --upgrade pipenv

exit 0