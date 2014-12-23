# Motivation
You often read about *staging* as a good practice (like from Martin Fowler). But in practice the recommendations you receive have little to do with staging, i.e. "staging areas" in [Python setuptools](https://pythonhosted.org/setuptools/setuptools.html).

Read my full article here: http://nerdcorner.info/tales/on-staging-with-python-and-setuptools

## Example Setup

 - Package repository: `/var/webcode/{name-of-project}-{version}`
 - Source distributions via `python3 setup.py sdist`
 - Two staging areas: *staging* and *production*
 - Two Vhosts with document roots to `/var/webcode/{staging,production}`

A deployment to either stage (ie. `staging`) would require the following steps:

 1. Build source distribution on development machine (or any other convenient platform)
 1. Upload the distribution into the package repository
 1. Build environment and install application into companion: `deploy_py.sh projectA-0.4.tar.gz`
 1. Create symbolic link to the stage's document root: `rm staging && ln -s projectA-0.4 staging`

That's it.
