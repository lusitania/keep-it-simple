# Motivation
How do you perform mass-operations on an arbitrary large set of machines? "You open your [OpenStack dashboard](www.openstack.org/software/openstack-dashboard/) and ... what was that? You don't have a dashboard? Pity."

It is actually quite simple to do this with Linux' standard tools. All you need is `ssh`, a `for`-loop and a place/file to keep your server records.

## Instructions
You don't even need to create a BASH file for this. I've been using this approach on a copy-and-paste basis for over two years.

Example assumptions:
 - Server IPs are held in two non-disjoint files `servers_{backend,frontend}.txt`
 - `servers_*` may contain comments (line starts with `#`)
 - One IP entry per line
 - Public key method is used for authentication, certificate is accepted on all remote accounts

Preparations:
 1. Load `ssh-agent`
 1. Select the servers, ie. *backend* and *frontend*, and join into a list
 1. Consolidate list: remove duplicates and comments

```
ssh-agent bash
ssh-add ~/.ssh/myserverkey

mylist="$(<servers_backend.txt)\n"
mylist+="$(<servers_frontend.txt)\n"
consolidated="$(echo -e "$mylist"|grep -vE "^\W*$|^\W*#"|sort|uniq -u)"
```

Iterate of server selection and submit command:
```
read mycmd
for s in $consolidated; do \
    echo -n -e "\n==> Server: $s\t";\
    ssh -o ConnectTimeout=5 -o BatchMode=yes -o stricthostkeychecking=no $s "$mycmd";\
done
```

## Discussion
**Why not set mycmd directly?** Escaping. The more elaborate commands also require elaborate escaping if you want to assign the string value to a variable. When using `read` you can simply copy-and-paste the commands you've used for testing. No further escaping required.
