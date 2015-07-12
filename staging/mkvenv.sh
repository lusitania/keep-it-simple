#!/bin/bash

# PEP 20 explicit is better than implicit
set -e -u

# If unset/empty PYBIN will be assigned the latest `python3' installed
echo "[${0##*/}] Using Python ${PYBIN:=$(which python3.{0..99}|sort -nr|head -n 1)}"

# venv is broken in Ubuntu 14.04, use virtualenv instead
echo "[${0##*/}] Using ${MKENVBIN:=$(which virtualenv-${PYBIN##*python})}"

if [ -z ${ENVDIR:-} ]; then
    BASEDIR="$(readlink -m "${0%/*}/../")"
    ENVDIR="$BASEDIR/run/python"
else
    [ -z $BASEDIR ] && BASEDIR="$(readlink -m "${ENVDIR}")"
fi

echo "[${0##*/}] Creating environment in $ENVDIR"
[ -d $ENVDIR ] || mkdir --parents $ENVDIR

# --relocatable gives you no extra here since every env is independent
# --always-copy because of https://github.com/pypa/virtualenv/pull/663
$MKENVBIN -q -p "$PYBIN" --clear --always-copy "$ENVDIR"

# fix activate's PS1 to display BASEDIR instead of ENVDIR
echo "[${0##*/}] Patching bin/activate"
sed -ri "s|PS1=.+basename ...VIRTUAL_ENV.+$|PS1=\"(${BASEDIR##*/}) \$PS1\"|" "$ENVDIR/bin/activate"
if ! ln -s $ENVDIR/bin/activate ${0%/*}/activate 2>/dev/null; then
    cp -f $ENVDIR/bin/activate ${0%/*}/
fi
