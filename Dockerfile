# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Selenium WebDriver dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . /app

# Set environment variables
ENV PYTHONUNBUFFERED=1

