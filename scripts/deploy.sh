#!/bin/bash

# deploy.sh - Deployment script for the application

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting deployment..."

# Pull the latest code from the repository
echo "Pulling latest code from the repository..."
git pull origin main

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python migrate_db.py

# Restart the application (assuming a systemd service)
echo "Restarting the application service..."
sudo systemctl restart myapp.service

echo "Deployment completed successfully!"
