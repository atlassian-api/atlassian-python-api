#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example showing how to use both Confluence API v1 and v2 with the library
"""

from atlassian import Confluence, ConfluenceV2, create_confluence

# Example 1: Using the Confluence class with explicit API version
# For backwards compatibility, api_version=1 is the default
confluence_v1 = Confluence(
    url='https://your-domain.atlassian.net',
    username='your-email@example.com',
    password='your-api-token',
    api_version=1
)

# Example 2: Using the Confluence class with API v2
confluence_v1_with_v2 = Confluence(
    url='https://your-domain.atlassian.net',
    username='your-email@example.com',
    password='your-api-token',
    api_version=2
)

# Example 3: Using the dedicated ConfluenceV2 class (recommended for v2 API)
confluence_v2 = ConfluenceV2(
    url='https://your-domain.atlassian.net',
    username='your-email@example.com',
    password='your-api-token'
)

# Example 4: Using the factory method
confluence_v1_factory = create_confluence(
    url='https://your-domain.atlassian.net',
    username='your-email@example.com',
    password='your-api-token',
    api_version=1
)

confluence_v2_factory = create_confluence(
    url='https://your-domain.atlassian.net',
    username='your-email@example.com',
    password='your-api-token',
    api_version=2
)

# Verify the types and versions
print(f"confluence_v1 type: {type(confluence_v1)}, API version: {confluence_v1.api_version}")
print(f"confluence_v1_with_v2 type: {type(confluence_v1_with_v2)}, API version: {confluence_v1_with_v2.api_version}")
print(f"confluence_v2 type: {type(confluence_v2)}, API version: {confluence_v2.api_version}")
print(f"confluence_v1_factory type: {type(confluence_v1_factory)}, API version: {confluence_v1_factory.api_version}")
print(f"confluence_v2_factory type: {type(confluence_v2_factory)}, API version: {confluence_v2_factory.api_version}")

# Note: Currently most v2-specific methods are not implemented yet
# They will be added in Phase 2 and Phase 3 of the implementation 