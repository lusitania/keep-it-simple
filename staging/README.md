# Motivation
You often read about *staging* as a good practice. But in practice the recommendations you receive have little to do with staging, i.e. "staging areas" in [Python setuptools](https://pythonhosted.org/setuptools/setuptools.html).

In my opinion staging means to
 1. Decrease uncertainty and verify correctness
 1. Lever your application onto the target platform
 1. Provide an atomic and non-intrusive (one-step) deployment
 1. Ensure a role-back option

This entails a set of invariants:
 1. Every staged revision has its own environment
 1. Each environment is immutable
 1. Each revision operates independent of any other code present on the platform
 1. A verification is final

## Example Setup
 - Revision repository: `/var/webcode/{name-of-project}-{version}`
 - Two staging areas: *staging* and *production*
 - Two VHosts with document roots to `/var/webcode/{staging,production}`

Steps to take:
 1. Prepare environment in revision repository
 1. Create symlink like: `rm staging && ln -s {name-of-project}-{version} staging`

## Discussion
**Every environment is shared by exactly one application revision.** The reason for this is twofold:
 - `setuptools` creates files in its "staging area" `site-packages` that directly link the environment to the installed app. `setuptools` always overwrite `easy-install.pth` so that only the recently installed revision will prevail. `nameofproject.egg-link` is version-agnostic and will also always be overwritten with each setup run, effectively sabotaging the staging idea. Using `--relocatable` only disables changes to `easy-install.pth` but introduces new issues (i.e. load failures in frameworks that don't anticipate this behaviour). The issue with the egg-link can't be resolved.
 - With a *shared* environment uncertainty is introduced to already verified revisions with all subsequent setup runs: A setup may or may not install new packages that may or may not break apps previously verified. This directly contradicts the primary intention of staging (as established above).

**Non-intrusive deployment.** Honestly, putting your app to work is a side show. It's a process you do once in a while, which never changes and simply has to work. You are getting paid for a running app, not for the process of making it so. 
 - One command has to suffice
 - Anything that can go wrong must be non-critical. In the example above: Must happen before the symlink.

**Atomicity.** Critical steps must not fail. Any failure must have happened before (like package errors, failed unit test, ...). In the example above: The system changes behaviour only once the symlink was redirected.

**Role-back.** Things can still go wrong. Don't get yourself in the way by overwriting previously good states. Keep your old stuff for a while longer.
