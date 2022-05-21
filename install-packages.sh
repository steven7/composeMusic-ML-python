#!/bin/bash

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# Update the package listing, so we know what package exist:
apt-get update

# Install security updates:
apt-get -y upgrade

# Install a new package, without unnecessary recommended packages:
# Dependency for converting midi to actual music file.
apt-get -y install --no-install-recommends fluidsynth 


#Install HDF5py This won't install with pip on Apple Sillicon the normal way
# apt-get -y install hdf5
# brew install hdf5
# export HDF5_DIR=/opt/homebrew/Cellar/hdf5/1.12.0_4
# pip install --no-binary=h5py h5py

# /opt/homebrew/bin/brew install openblas
# export OPENBLAS=$(/opt/homebrew/bin/brew --prefix openblas)
# export CFLAGS="-falign-functions=8 ${CFLAGS}"
# git clone https://github.com/scipy/scipy.git
# cd scipy
# /opt/homebrew/bin/pip install .

# Delete cached files we don't need anymore (note that if you're
# using official Docker images for Debian or Ubuntu, this happens
# automatically, you don't need to do it yourself):
apt-get clean
# Delete index files we don't need anymore:
rm -rf /var/lib/apt/lists/*