#!/bin/bash

# Fail hard on either errors or unset variables
set -e -u

# Syntax help if no parameters were given
if (( $# < 1 )); then
    echo "Syntax: echo <password> | $0 ssh-copy-id -i <id-file> user@remote"
    exit 1
fi

# Provide response if $0 was called from ssh via SSH_ASKPASS
if [ -n "$MySshPass" ] && [ -n "$SSH_ASKPASS" ]; then
    echo "$MySshPass"
    exit 0
fi

# Read the password from the pipe (stdin) if it wasn't set externally
if [ -z "$MySshPass" ]; then
    read -s MySshPass
    export $MySshPass
fi


export SSH_ASKPASS="$0"
[ -n $DISPLAY ] || export DISPLAY=dummy:0

# Call the ssh script in a new session
setsid "$@"

# Never let a password linger in the environment
unset MySshPass
unset SSH_ASKPASS
