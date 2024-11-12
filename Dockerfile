# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt update \
  && apt install ffmpeg -y \
  && apt-get clean \
  && pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "app.py"]
