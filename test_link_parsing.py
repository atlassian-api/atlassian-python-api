#!/usr/bin/env python3
"""
Test script for Link header parsing functionality
"""

def _parse_link_header(link_header: str):
    """
    Parse Link header to extract next page URL.
    
    Link header format: <url>; rel="next", <url>; rel="prev"
    
    :param link_header: The Link header value
    :return: Next page URL if found, None otherwise
    """
    if not link_header:
        return None
        
    # Split by comma to get individual links
    links = link_header.split(',')
    
    for link in links:
        link = link.strip()
        # Look for rel="next"
        if 'rel="next"' in link or "rel='next'" in link:
            # Extract URL from <url>
            url_start = link.find('<')
            url_end = link.find('>')
            if url_start != -1 and url_end != -1:
                return link[url_start + 1:url_end]
    
    return None

# Test cases
test_cases = [
    # Standard format with quotes
    ('<https://api.example.com/page2>; rel="next", <https://api.example.com/page1>; rel="prev"', 'https://api.example.com/page2'),
    # Format with single quotes
    ("<https://api.example.com/page2>; rel='next', <https://api.example.com/page1>; rel='prev'", 'https://api.example.com/page2'),
    # Only next link
    ('<https://api.example.com/page2>; rel="next"', 'https://api.example.com/page2'),
    # No next link
    ('<https://api.example.com/page1>; rel="prev"', None),
    # Empty header
    ('', None),
    # None header
    (None, None),
]

print("Testing Link header parsing...")
for i, (header, expected) in enumerate(test_cases):
    result = _parse_link_header(header)
    status = "✓" if result == expected else "✗"
    print(f"{status} Test {i+1}: {result} == {expected}")
    if result != expected:
        print(f"  Header: {header}")
        print(f"  Expected: {expected}")
        print(f"  Got: {result}")

print("Link header parsing tests completed!")