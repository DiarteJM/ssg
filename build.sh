#!/bin/bash
# Set execute permissions on the script
chmod +x build.sh

# Run the main.py script with the "/ssg/" basepath
# This is the base URL path where the site will be served from
PYTHONPATH=$(pwd) python3 src/main.py "/ssg/"

# Print success message
echo "Build completed! Files are in the public/ directory."