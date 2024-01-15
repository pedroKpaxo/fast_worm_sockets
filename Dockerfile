# BASE DJANGO_DOCKERFILE
# Last mod == 22-12-2023
FROM python:3.10

LABEL maintainer="pedro@monumentosoftware.com.br"

# Set the environment variable to unbuffered mode to see output logs in real-time
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy the requirements file to leverage Docker cache
COPY ./requirements /app/requirements

RUN pip install --upgrade pip && pip install -r /app/requirements/production.txt

# Copy the application source code to the container
COPY . /app

# IMPORTANT
# This is the port that FastAPI will be listening on inside the container
EXPOSE 8000

# Healthcheck to monitor the application
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000", "||", "exit 1"]

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
