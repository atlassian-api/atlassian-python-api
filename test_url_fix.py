#!/usr/bin/env python3

import logging
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up verbose logging
logging.basicConfig(level=logging.DEBUG)
# Enable HTTP request logging
logging.getLogger("urllib3").setLevel(logging.DEBUG)

# Credentials from environment variables
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

# Check if environment variables are loaded
if not all([CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN]):
    print("Error: Missing environment variables. Please create a .env file with the required variables.")
    exit(1)

print("\n" + "-"*80)
print("TESTING PAGINATION URL STRUCTURE")
print("-"*80)

# Make a direct API call to get the first page and inspect the next URL
print("\nMaking direct API call to get first page and inspect the next URL")
direct_url = f"{CONFLUENCE_URL}/wiki/api/v2/spaces?limit=1"
print(f"Direct API call to: {direct_url}")

try:
    response = requests.get(
        url=direct_url,
        auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
        headers={"Accept": "application/json"}
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
                    full_next_url = f"{base_url}{next_url}"
                    print(f"\nTesting full next URL directly: {full_next_url}")
                    next_response = requests.get(
                        url=full_next_url,
                        auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
                        headers={"Accept": "application/json"}
                    )
                    print(f"Status code: {next_response.status_code}")
                    if 200 <= next_response.status_code < 300:
                        next_data = next_response.json()
                        print(f"Response contains {len(next_data.get('results', []))} results")
                    else:
                        print(f"Error response: {next_response.text}")
                
                # Test the problem URL that's being constructed
                problem_url = f"{CONFLUENCE_URL}/wiki{next_url}"
                print(f"\nTesting the problem URL: {problem_url}")
                problem_response = requests.get(
                    url=problem_url,
                    auth=(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN),
                    headers={"Accept": "application/json"}
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

print("\n" + "-"*80)
print("COMPLETE") 