# Test Scripts for Confluence V2 API

## Overview

These test scripts are used to test the Confluence V2 API implementation. They require credentials to connect to a Confluence instance.

## Setting Up Credentials

To run the test scripts, you need to set up your Confluence credentials. 

### Step 1: Create a .env file

Create a `.env` file in the root directory of the project with the following format:

```
CONFLUENCE_URL=https://your-instance.atlassian.net
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token
CONFLUENCE_SPACE_KEY=SPACE
```

Replace the values with your own credentials:
- `CONFLUENCE_URL`: The URL of your Confluence instance
- `CONFLUENCE_USERNAME`: Your Confluence username (usually an email)
- `CONFLUENCE_API_TOKEN`: Your Confluence API token (can be generated in your Atlassian account settings)
- `CONFLUENCE_SPACE_KEY`: The key of a space in your Confluence instance that you have access to

### Step 2: Install required packages

Make sure you have all required packages installed:

```
pip install -r requirements-dev.txt
```

### Step 3: Run the scripts

Now you can run the test scripts:

```
python test_search.py
python test_pages.py
```

## Security Note

The `.env` file is listed in `.gitignore` to prevent accidentally committing your credentials to the repository. Never commit your credentials directly in code files.

If you need to find available spaces to use for testing, you can run:

```
python get_valid_spaces.py
```

This will output a list of spaces that you have access to, which can be used for the `CONFLUENCE_SPACE_KEY` environment variable. 