# Use the official Python 3 image based on Alpine Linux
FROM mcr.microsoft.com/devcontainers/python:3.12-bullseye

RUN apt update && apt install -y git-lfs

# Create and activate a virtual environment
# Do not need to do this in a docker file, because I can consider the container as an isolated environment
# RUN python3 -m venv venv &&. venv/bin/activate

# PYTHON LIBS
COPY requirements.txt .
RUN pip install -r requirements.txt && pip install --upgrade pip
