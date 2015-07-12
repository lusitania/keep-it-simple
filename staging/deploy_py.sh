#/bin/bash

# PEP 20 explicit is better than implicit
set -e -u

# Allow argument list *.gz. Take only first argument and do python deploy magic. Ignore remainder.
NAME="${1/.tar.gz}"
ENVDIR="${ENVDIR:-$NAME/.env}"

echo "[${0##*/}] Deploying $NAME"

source ${0%/*}/mkenv.sh

test -e "$NAME" && echo "[${0##*/}] Removing superseded copy" && rm -r "$NAME"

echo "[${0##*/}] Extracting tarball"
tar xzf "$1"

echo "[${0##*/}] Registering webapp"
set +u
source "$ENVDIR/bin/activate"
set -u

cd "$NAME"
# Don't less. Quitting less terminates the whole chain. Use tail -f if you must
"$PYBIN" setup.py develop |& tee setup.log
cd -

echo "[${0##*/}] Cleaning up"
read -p "Delete tarball? [y/n]: " -s -n 1 askdelete
if [[ "$askdelete" =~ "y" ]]; then rm -v "$1"; fi

echo -e "\n-- Next Steps: Update symlink: rm staging && ln -s '$NAME' staging"
