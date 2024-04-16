# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install any dependencies required by your Python script
RUN pip3 install domeneshop_bots

# Copy the Python script and config file into the container
COPY example.py .
COPY config.json .

# Run the Python script when the container starts
CMD ["python", "example.py"]
