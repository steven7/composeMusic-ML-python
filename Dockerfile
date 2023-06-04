# syntax=docker/dockerfile:1

# This is for AWS Lambda. It will be the default and production Dockerfile.
FROM  amazon/aws-lambda-python:3.8
# FROM --platform=linux/amd64 amazon/aws-lambda-python:3.8
# FROM --platform=linux/amd64 amazon/aws-lambda-python:3.8

# Set working directory.
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy contents of this directory to container's working directory.
# For this container only on sam.
# COPY compose ${LAMBDA_TASK_ROOT} 
# For this container only to upload to ecr.
# For when using docker compose?
COPY . ${LAMBDA_TASK_ROOT}

# FluidSynth wants the default sounfont to be in /usr/local/share/soundfonts/default.sf2 on Linux. The local folder is taken out of the path on mac.
# We will put the default in that location to make it happy. It is kind of a hack but it works.
RUN mkdir /home/sbx_user1051
RUN mkdir /home/sbx_user1051/.fluidsynth
RUN mkdir /usr/local/share/soundfonts

# FluidSynth wants the default sounfont to be in /usr/local/share/soundfonts/default.sf2 on Linux. The local folder is taken out of the path on mac.
# We will put the default in that location to make it happy. It is kind of a hack but it works.
# Move the default soundfont to the direct that fluidsynth expects it to be found in.
# For this container only on sam.
# COPY compose/soundfonts/default.sf2 ${LAMBDA_TASK_ROOT}/.fluidsynth/default_sound_font.sf2
# COPY compose/soundfonts/default.sf2  ~/.fluidsynth/default_sound_font.sf2
# For this container only to upload to ecr.
# COPY soundfonts/default.sf2 ${LAMBDA_TASK_ROOT}/.fluidsynth/default_sound_font.sf2
COPY soundfonts/default.sf2  /home/sbx_user1051/.fluidsynth/default_sound_font.sf2
COPY soundfonts/default.sf2  /usr/local/share/soundfonts/default.sf2

# Environment variables for fluidsynth installation.
ENV LD_LIBRARY_PATH="/usr/local/lib64:${LD_LIBRARY_PATH}"
ENV PATH="/usr/local/lib64:${PATH}"

# Dependency for converting midi to actual music file.
# RUN apt update && apt install fluidsynth 
RUN source ./install-fluidsynth-aws-linux.sh

# Update pip
# RUN  python3.8 -m pip install --upgrade pip
# Install the function's dependencies using file requirements.txt
# from your project folder. 
# For this container only and for docker compose.
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# # Tensorflow with custom wheel for docker on M1 mac
# RUN pip3 install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.htm

# Protobud library ~3.18 is missing the builder.pyt file for some reason. This makes up for that.
RUN curl https://raw.githubusercontent.com/protocolbuffers/protobuf/main/python/google/protobuf/internal/builder.py > /var/task/google/protobuf/internal/builder.py

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ]


# old one
# FROM python:3.8-slim-buster

# # development channel. Either dev or prod. docker-compose will pass in dev channel.
# # wil default to prod when deplying to aws
# # default to prod. docker-compose won't be on aws
# ARG channel=prod 

# # the arg will be the value of the channel_var environment variable.
# ENV channel_env_var=$channel

# WORKDIR /app

# # Copy contents of this directory to container's working directory.
# COPY . .

# # Dependency for converting midi to actual music file.
# # RUN apt update && apt install fluidsynth
# RUN ./install-packages.sh
 
# # FluidSynth wants the default sounfont to be in /usr/share/soundfonts/default.sf2. 
# # We will put the default in that location to make it happy. It is kind of a hack but it works.
# COPY soundfonts/default.sf2 /usr/share/soundfonts/default.sf2

# # Python dependencies
# RUN pip3 install -r requirements.txt 

# # Tensorflow with custom wheel for docker on M1 mac
# RUN pip install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.htm

# EXPOSE 8010

# CMD [ "waitress-serve", "--port=8010", "--call", "app:create_app"]
