#!/bin/bash

# Infinite loop to call the Python script every 10 minutes
while true; do
    # Call the Python script
    python3 get_comments_from_urls.py

    # Wait for 10 minutes (600 seconds)
    sleep 600
done
