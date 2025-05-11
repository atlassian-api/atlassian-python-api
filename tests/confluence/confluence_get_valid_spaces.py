#!/usr/bin/env python3

import os

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Credentials from environment variables
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

# Check if environment variables are loaded
if not all([CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN]):
    print("Error: Missing environment variables. Please create a .env file with the required variables.")
    exit(1)

print("Fetching available spaces...")
response = requests.get(
    f"{CONFLUENCE_URL}/wiki/api/v2/spaces?limit=10",
    auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
    headers={"Accept": "application/json"}
)

if response.status_code == 200:
    spaces = response.json().get("results", [])
    if spaces:
        print("\nAvailable spaces:")
        print("-------------------------")
        for i, space in enumerate(spaces, 1):
            print(f"{i}. Key: {space.get('key')}, Name: {space.get('name')}")
    else:
        print("No spaces found or you don't have access to any spaces.")
else:
    print(f"Error fetching spaces: {response.status_code}")
    print(response.text)

print("\nUpdate your .env file or tests with a valid space key.") 