#!/bin/bash
# The inotify package is maintained in a mercurial repo on Bitbucket
# The frozen pip requirements therefore require the hg command
sudo apt-get install mercurial

# Provide Python inotify wrapper
virtualenv3 .env
. .env/bin/activate
pip3 -r watch-directory.pip

# If you don't want to install mercurial you may clone a fork from github
pip3 install -e git://github.com/gurubert/python-inotify.git#egg=python-inotify
