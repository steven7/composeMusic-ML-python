# syntax=docker/dockerfile:1
 
FROM python:3.8-slim-buster

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

# Tensorflow with custom wheel for docker on M1 mac
RUN pip install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.htm

EXPOSE 8010

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8010"]

# waitress-serve --port=8010 --call hello:create_app

CMD [ "waitress-serve", "--port=8010", "--call", "app:create_app"]
# waitress-serve --port=8010 --call hello:create_app