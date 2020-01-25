#!/usr/bin/env bash

apt-get update -qq &> /dev/null || exit 1

apt-get install -qq \
    git \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
&> /dev/null || exit 1

rm -rf /var/lib/apt/lists/* || exit 1

git config --global url.https://github.com/.insteadOf git@github.com:
git config --global url.https://.insteadOf git://

git clone https://github.com/pyenv/pyenv.git /root/.pyenv

exit 0