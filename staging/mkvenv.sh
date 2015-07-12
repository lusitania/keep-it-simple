#!/bin/bash

# PEP 20 explicit is better than implicit
set -e -u

# If unset/empty PYBIN will be assigned the latest `python3' installed
echo "[${0##*/}] Using Python ${PYBIN:=$(which python3.{0..99}|sort -nr|head -n 1)}"

# venv is broken in Ubuntu 14.04, use virtualenv instead
echo "[${0##*/}] Using ${MKENVBIN:=$(which virtualenv-${PYBIN##*python})}"

echo "[${0##*/}] Creating environment in ${ENVDIR:=$(readlink -f ${0%/*}/../usr/)}"
[ -d $ENVDIR ] || mkdir --parents $ENVDIR

# --relocatable gives you no extra here since every env is independent
# --always-copy because of https://github.com/pypa/virtualenv/pull/663
$MKENVBIN -p "$PYBIN" --clear --always-copy "$ENVDIR"
