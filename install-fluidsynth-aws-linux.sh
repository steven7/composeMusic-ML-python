#!/bin/bash

# Install FluidSynth from source files.

# Install C and C++ compiler
yum install gcc -y
yum install gcc-c++ -y

# Install other required packages
yum install make -y
yum install glib2-devel -y
 
# Install other dev tools
yum install libsndfile-devel -y
# # yum install libsndfile -y
# yum install libsndfile-utils -y
# yum install build-essential -y

# yum install fftw3 -y
# yum install libsamplerate -y
# yum install alsa-lib-devel -y
# yum install alsa-tools -y 
# # sudo yum install alsa-utils -y 
# # sudo yum install ladspa -y
# # sudo 
# yum install ladspa-devel -y
# yum install SDL2-devel -y
# sudo yum install readline-devel -y
# sudo yum install pulseaudio-libs-devel -y
# sudo yum install systemd-devel -y

# We need to install these on the aws linux for the tar comand line tool to work apparently.
yum install tar -y 
yum install gzip -y


# Install CMake. We need version 3.1.0 or higher
# sudo 
yum install cmake3 -y

# Update path for future fluidsynth install location.
# This will alow the system to find fluidsynth. It makes the fluidsynth --version command work.
export LD_LIBRARY_PATH=/usr/local/lib64:$LD_LIBRARY_PATH
  
export PATH=/usr/local/lib64:$PATH

 
#
# Install Fluidsynth
#

# Download source files in tar format.
curl -LJO https://github.com/FluidSynth/fluidsynth/archive/refs/tags/v2.2.7.tar.gz
# Unpack tar files
tar -xvzf fluidsynth-2.2.7.tar.gz
# clean up tar archive
rm fluidsynth-2.2.7.tar.gz
# Create and enter build directory
mkdir fluidsynth-2.2.7/build
cd fluidsynth-2.2.7/build
  
# CMake command to build. Use CMake3.
cmake3 ..
# Use make to install.
make install
 
# Path needed to find ldconfig
export PATH=$PATH:/sbin
# Linker thing
ldconfig -v
 
# fixes error: fluidsynth: error while loading shared libraries: libfluidsynth.so.3: cannot open shared object file: No such file or directory
# when running in python
# symlink the fluidsytnth we have on the left to the one the python lib looks for on the right.
# ln -s libfluidsynth.so.3.1.0 libfluidsynth.so.3
ln -s libfluidsynth.so libfluidsynth.so.3

echo ""
echo "______________ fluidsynth -h ______________" 
fluidsynth -h 
echo ""
echo "______________ fluidsynth --version ______________" 
fluidsynth --version 
 
# echo ""
# pwd
# echo ""

# Go back to root directory
cd ../..
# Then be used like in doc: https://gist.github.com/wilstenholme/424417bbbca83c0fe7189a0ffb6d4981
# MIDI to wav
# fluidsynth -F "$var".wav Soundfont.sf2 "$var".mid
# or in python
 
# echo ""
# echo ""
# echo "fluidsynth -F"
# fluidsynth -F tmp/changing_chords.wav /usr/local/share/soundfonts/default.sf2 run/0018_chorales/samples/changing_chords.midi
 
# echo ""
# echo "__ test __"