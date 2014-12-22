#!/bin/bash

# Fail hard on either errors or unset variables
set -e -u

# Syntax help if no parameters were given
if (( $# < 1 )); then
    echo "Syntax: echo <password> | $0 ssh-copy-id -i <id-file> user@remote"

# Read the password from the pipe (stdin) and call the ssh script
elif test -z "$MySshPass"; then
    read -s MySshPass

    export $MySshPass
    export SSH_ASKPASS="$0"
    [ -n $DISPLAY ] || export DISPLAY=dummy:0

    # Call the ssh script in a new session
    setsid "$@"

    # Never let a password linger in the environment
    unset MySshPass
    unset SSH_ASKPASS

# Provide response for ssh via SSH_ASKPASS
else
    echo "$MySshPass"
fi