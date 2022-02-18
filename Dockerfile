# syntax=docker/dockerfile:1

FROM python:3.8.11-slim-buster

# development channel. Either dev or prod. docker-compose will pass in dev channel.
# wil default to prod when deplying to aws
# default to prod. docker-compose won't be on aws
ARG channel=prod 

# the arg will be the value of the channel_var environment variable.
ENV channel_env_var=$channel

WORKDIR /app

# Copy contents of this directory to container's working directory.
COPY . .

# Dependency for converting midi to actual music file.
# RUN apt update && apt install fluidsynth
RUN ./install-packages.sh
 
# FluidSynth wants the default sounfont to be in /usr/share/soundfonts/default.sf2. 
# We will put the default in that location to make it happy. It is kind of a hack but it works.
COPY soundfonts/default.sf2 /usr/share/soundfonts/default.sf2

# Python dependencies
RUN pip3 install -r requirements.txt 

EXPOSE 5000

# CMD [ "python3", "-m" , "flask", "run", "--host=localhost", "--port=5000"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]