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

# Get pages with no space filtering
print("Test 1: Getting pages with no filtering")
response = requests.get(
    f"{CONFLUENCE_URL}/wiki/api/v2/pages",
    auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
    headers={"Accept": "application/json"},
    params={
        "limit": 5
    }
)
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    results = data.get("results", [])
    print(f"Found {len(results)} pages")
    if results:
        for i, page in enumerate(results, 1):
            print(f"{i}. ID: {page.get('id')}, Title: {page.get('title')}")
            space = page.get("space", {})
            print(f"   Space Key: {space.get('key')}, Space Name: {space.get('name')}")
    else:
        print("No pages found.")
else:
    print("Error:", response.text)

# Get specific space info
print("\nTest 2: Get space info for TS")
response = requests.get(
    f"{CONFLUENCE_URL}/wiki/api/v2/spaces",
    auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
    headers={"Accept": "application/json"},
    params={
        "keys": SPACE_KEY,
        "limit": 1
    }
)
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    results = data.get("results", [])
    print(f"Found {len(results)} spaces")
    if results:
        space = results[0]
        print(f"Space ID: {space.get('id')}")
        print(f"Space Key: {space.get('key')}")
        print(f"Space Name: {space.get('name')}")
        
        # Now try getting pages with this space ID
        space_id = space.get('id')
        if space_id:
            print(f"\nGetting pages for space ID: {space_id}")
            page_response = requests.get(
                f"{CONFLUENCE_URL}/wiki/api/v2/pages",
                auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
                headers={"Accept": "application/json"},
                params={
                    "space-id": space_id,
                    "limit": 5
                }
            )
            print(f"Status code: {page_response.status_code}")
            if page_response.status_code == 200:
                page_data = page_response.json()
                page_results = page_data.get("results", [])
                print(f"Found {len(page_results)} pages in space {SPACE_KEY}")
                if page_results:
                    for i, page in enumerate(page_results, 1):
                        print(f"{i}. ID: {page.get('id')}, Title: {page.get('title')}")
                else:
                    print("No pages found in this space.")
            else:
                print("Error getting pages:", page_response.text)
    else:
        print(f"No space found with key {SPACE_KEY}")
else:
    print("Error getting space:", response.text) 