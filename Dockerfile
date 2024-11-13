# Use the official Python image from Docker Hub (choose version 3.8 or above)
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Define the command to run your application
CMD ["python", "main.py"]
