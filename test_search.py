#!/usr/bin/env python3

import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Credentials from environment variables
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")

# Check if environment variables are loaded
if not all([CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN, SPACE_KEY]):
    print("Error: Missing environment variables. Please create a .env file with the required variables.")
    exit(1)

# Test with just a query
print("Test 1: Search with simple query")
query = "test"
response = requests.get(
    f"{CONFLUENCE_URL}/wiki/api/v2/search",
    auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
    headers={"Accept": "application/json"},
    params={
        "query": query, 
        "limit": 5,
        "content-type": "page"
    }
)
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    results = data.get("results", [])
    print(f"Found {len(results)} results")
    if results:
        print("First result title:", results[0].get("title"))
else:
    print("Error:", response.text)

# Test with query and CQL
print("\nTest 2: Search with query and CQL")
response = requests.get(
    f"{CONFLUENCE_URL}/wiki/api/v2/search",
    auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
    headers={"Accept": "application/json"},
    params={
        "query": query,
        "cql": f'space="{SPACE_KEY}" AND type=page',
        "limit": 5,
        "content-type": "page"
    }
)
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    results = data.get("results", [])
    print(f"Found {len(results)} results")
    if results:
        print("First result title:", results[0].get("title"))
else:
    print("Error:", response.text)

# Test with different approach - get pages in a space
print("\nTest 3: Get pages in a space")
response = requests.get(
    f"{CONFLUENCE_URL}/wiki/api/v2/pages",
    auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
    headers={"Accept": "application/json"},
    params={
        "space-id": SPACE_KEY,
        "limit": 5
    }
)
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    results = data.get("results", [])
    print(f"Found {len(results)} results")
    if results:
        print("First result title:", results[0].get("title"))
else:
    print("Error:", response.text) 