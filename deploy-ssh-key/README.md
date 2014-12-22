# Motivation
This is the most simple scenario. Suppose you maintain access to user accounts on a set of Linux servers and you need to grant access for a particular SSH key. In this case let the login name and password be identical.

The obvious choice would be to use `ssh-copy-id`. However the script supplies no (easy) way to authenticate a user by password. The trick is threefold:

 1. Provide an executable file that prints the password to stdout
 1. Set the environment appropriately
 1. Trick `ssh` to actually use the new environment by detaching it from the current terminal and placing it into a new session

## Instructions
Deploying the key to multiple servers is now dead simple:

```
servers="ip1 ip2 ..."
idfile=~/.ssh/id_rsa.pub
read somevar

for host in $servers; do \
    MySshPass="$somevar" ./deploy-ssh-key.sh ssh-copy-id -i "$idfile" user@$host \
done
```
Notice that I don't echo the password into the pipe. This way the password doesn't appear in BASH's history. The extra assignment is necessary due to the internal unset of MySshPass within our shell script.

This approach also opens the path for per-server passwords. `awk` may be your tool of choice.