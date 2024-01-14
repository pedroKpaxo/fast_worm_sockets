# Use the official Python image with your desired version
FROM python:3.10

# Set the maintainer label
LABEL maintainer="pedro@monumentosoftware.com.br"

# Set the environment variable to unbuffered mode to see output logs in real-time
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to leverage Docker cache
COPY ./requirements /app/requirements

# Upgrade pip and install the Python dependencies
RUN pip install --upgrade pip && pip install -r /app/requirements/production.txt

# Copy the application source code to the container
COPY . /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Health check to ensure the server is running (adjust the check command as per your application)
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000", "||", "exit 1"]

# Expose the port your app runs on

