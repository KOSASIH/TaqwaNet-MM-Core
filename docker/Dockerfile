# Dockerfile - Docker configuration for the application

# Use the official Python image as a base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port (adjust as necessary)
EXPOSE 5000

# Command to run the application
CMD ["python", "src/app.py"]  # Adjust the command based on your application entry point
