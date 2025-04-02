#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found."
    echo "Please create a .env file with your credentials based on .env.example"
    exit 1
fi

# Load environment variables
set -a
source .env
set +a

# Run integration tests
python -m unittest tests/test_jira_v3_integration.py -v

# Return the exit code of the tests
exit $? 