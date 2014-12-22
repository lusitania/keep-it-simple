#/bin/bash

# PEP 20 explicit is better than implicit
set -e -u
PYBIN="python3.3"
ENVDIR="$NAME/.env"

# Allow argument list *.gz. Take only first argument and do python deploy magic. Ignore remainder.
NAME="${1/.tar.gz}"
echo "-- Deploying $NAME"

test -e "$NAME" && echo "--- Removing superseded copy" && rm -r "$NAME"

echo "--- Extracting tarball"
tar xzf "$1"

echo "--- Creating environment $ENVDIR"
# --relocatable gives you no extra here since every env is independent
virtualenv -p "$PYBIN" --clear "$ENVDIR"

echo "--- Registering webapp"
set +u
source "$ENVDIR/bin/activate"
set -u

cd "$NAME"
# Don't less. Quitting less terminates the whole chain. Use tail -f if you must
"$PYBIN" setup.py develop |& tee setup.log
cd -

echo "--- Cleaning up"
read -p "Delete tarball? [y/n]: " -s -n 1 askdelete
if [[ "$askdelete" =~ "y" ]]; then rm -v "$1"; fi

echo -e "\n-- Next Steps: Update symlink: rm staging && ln -s '$NAME' staging"
