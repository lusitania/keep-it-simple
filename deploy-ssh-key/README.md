# Motivation
This is the most simple scenario. Suppose you maintain access to user accounts on a set of Linux servers and you need to grant access for a particular SSH key. In this case let the login name and password be identical.

The obvious choice would be to use `ssh-copy-id`. However the script supplies no (easy) way to authenticate a user by password. The trick is threefold:

 1. Provide an executable file that prints the password to stdout
 1. Set the environment appropriately
 1. Trick `ssh` to actually use the new environment by detaching it from the current terminal and placing it into a new session
