#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Confluence credentials from environment variables
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN")

# Check if environment variables are loaded
if not all([CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN]):
    print("Error: Missing environment variables. Please create a .env file with the required variables.")
    sys.exit(1)

print("\n" + "-" * 80)
print("TESTING PAGINATION URL STRUCTURE")
print("-" * 80)

# Make a direct API call to get the first page and inspect the next URL
print("\nMaking direct API call to get first page and inspect the next URL")
DIRECT_URL = f"{CONFLUENCE_URL}/wiki/api/v2/spaces?limit=1"
print(f"Direct API call to: {DIRECT_URL}")

try:
    response = requests.get(
        url=DIRECT_URL, auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN), headers={"Accept": "application/json"}
    )
    status = response.status_code
    print(f"Status code: {status}")

    if 200 <= status < 300:
        try:
            data = response.json()
            print(f"Response contains {len(data.get('results', []))} results")

            # Extract and examine the next URL
            next_url = data.get("_links", {}).get("next")
            if next_url:
                print(f"\nNEXT URL: '{next_url}'")
                print(f"URL type: {type(next_url)}")
                print(f"First character: '{next_url[0]}'")
                if next_url.startswith("/"):
                    print("URL starts with /")
                else:
                    print("URL does NOT start with /")

                # Show the base URL we'd use
                base_url = data.get("_links", {}).get("base")
                if base_url:
                    print(f"BASE URL: '{base_url}'")
                    print(f"Full next URL would be: {base_url}{next_url}")

                # Test the full next URL directly
                if base_url:
                    FULL_NEXT_URL = f"{base_url}{next_url}"
                    print(f"\nTesting full next URL directly: {FULL_NEXT_URL}")
                    next_response = requests.get(
                        url=FULL_NEXT_URL,
                        auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
                        headers={"Accept": "application/json"},
                    )
                    print(f"Status code: {next_response.status_code}")
                    if 200 <= next_response.status_code < 300:
                        next_data = next_response.json()
                        print(f"Response contains {len(next_data.get('results', []))} results")
                    else:
                        print(f"Error response: {next_response.text}")

                # Test the problem URL that's being constructed
                PROBLEM_URL = f"{CONFLUENCE_URL}/wiki{next_url}"
                print(f"\nTesting the problem URL: {PROBLEM_URL}")
                problem_response = requests.get(
                    url=PROBLEM_URL,
                    auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
                    headers={"Accept": "application/json"},
                )
                print(f"Status code: {problem_response.status_code}")
                if problem_response.status_code != 200:
                    print(f"Error response: {problem_response.text[:100]}...")
            else:
                print("No next URL in response")

            # Debug the _links structure
            print("\nFull _links structure:")
            print(json.dumps(data.get("_links", {}), indent=2))

        except Exception as e:
            print(f"Error parsing JSON: {e}")
    else:
        print(f"Error response: {response.text}")
except Exception as e:
    print(f"Request error: {e}")

print("\n" + "-" * 80)
print("COMPLETE")
