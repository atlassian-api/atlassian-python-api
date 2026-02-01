#!/usr/bin/env python3
# coding=utf-8
"""
Example: Confluence Cloud Error Handling and Troubleshooting

This example demonstrates comprehensive error handling patterns for the Confluence Cloud v2 API,
including common error scenarios, debugging techniques, and recovery strategies.

Key features demonstrated:
- Common API error types and handling
- Authentication and authorization errors
- Rate limiting and throttling
- Content validation errors
- Network and connectivity issues
- Debugging and logging strategies
- Retry mechanisms and recovery patterns

Prerequisites:
- Confluence Cloud instance
- API token (not username/password)
- Python 3.9+

Usage:
    python confluence_error_handling.py

Configuration:
    Update the CONFLUENCE_URL and API_TOKEN variables below with your credentials.
"""

import os
import sys
import time
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import json

# Add the parent directory to the path to import atlassian
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from atlassian.confluence import ConfluenceCloud

# Configuration - Update these with your Confluence Cloud details
CONFLUENCE_URL = "https://your-domain.atlassian.net"
API_TOKEN = "your-api-token"
TEST_SPACE_KEY = "DEMO"  # Update with your test space key


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ConfluenceErrorHandler:
    """
    Comprehensive error handler for Confluence Cloud API operations.

    This class provides utilities for handling various types of errors
    that can occur when working with the Confluence Cloud API.
    """

    def __init__(self, confluence_client: ConfluenceCloud):
        """
        Initialize the error handler.

        Args:
            confluence_client: ConfluenceCloud client instance
        """
        self.confluence = confluence_client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def safe_api_call(
        self, operation: Callable, *args, max_retries: int = 3, backoff_factor: float = 1.0, **kwargs
    ) -> Optional[Any]:
        """
        Execute an API call with error handling and retry logic.

        Args:
            operation: The API operation to execute
            args: Positional arguments for the operation
            max_retries: Maximum number of retry attempts
            backoff_factor: Exponential backoff factor
            kwargs: Keyword arguments for the operation

        Returns:
            Operation result or None if all retries failed
        """
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                result = operation(*args, **kwargs)
                if attempt > 0:
                    self.logger.info(f"Operation succeeded on attempt {attempt + 1}")
                return result

            except Exception as e:
                last_exception = e
                error_type = self._classify_error(e)

                self.logger.warning(f"Attempt {attempt + 1}/{max_retries + 1} failed: {error_type} - {str(e)}")

                # Don't retry certain error types
                if error_type in ["authentication", "authorization", "validation"]:
                    self.logger.error(f"Non-retryable error: {error_type}")
                    break

                # Don't retry on last attempt
                if attempt == max_retries:
                    break

                # Calculate backoff delay
                delay = backoff_factor * (2**attempt)
                self.logger.info(f"Waiting {delay:.1f} seconds before retry...")
                time.sleep(delay)

        self.logger.error(f"All retry attempts failed. Last error: {last_exception}")
        return None

    def _classify_error(self, error: Exception) -> str:
        """
        Classify an error into a category for appropriate handling.

        Args:
            error: The exception to classify

        Returns:
            Error category string
        """
        error_str = str(error).lower()

        if "unauthorized" in error_str or "401" in error_str:
            return "authentication"
        elif "forbidden" in error_str or "403" in error_str:
            return "authorization"
        elif "not found" in error_str or "404" in error_str:
            return "not_found"
        elif "rate limit" in error_str or "429" in error_str:
            return "rate_limit"
        elif "bad request" in error_str or "400" in error_str:
            return "validation"
        elif "server error" in error_str or "500" in error_str:
            return "server_error"
        elif "timeout" in error_str or "connection" in error_str:
            return "network"
        else:
            return "unknown"

    def validate_adf_content(self, content: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate ADF content structure.

        Args:
            content: ADF content dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Basic ADF structure validation
            if not isinstance(content, dict):
                return False, "Content must be a dictionary"

            if content.get("version") != 1:
                return False, "ADF version must be 1"

            if content.get("type") != "doc":
                return False, "Root type must be 'doc'"

            if "content" not in content:
                return False, "Missing 'content' array"

            if not isinstance(content["content"], list):
                return False, "'content' must be an array"

            # Validate content nodes
            for i, node in enumerate(content["content"]):
                if not isinstance(node, dict):
                    return False, f"Content node {i} must be a dictionary"

                if "type" not in node:
                    return False, f"Content node {i} missing 'type'"

            return True, None

        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def diagnose_api_issue(self, error: Exception) -> Dict[str, Any]:
        """
        Provide diagnostic information for an API error.

        Args:
            error: The exception to diagnose

        Returns:
            Dictionary with diagnostic information
        """
        diagnosis = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "category": self._classify_error(error),
            "timestamp": datetime.now().isoformat(),
            "suggestions": [],
        }

        category = diagnosis["category"]

        if category == "authentication":
            diagnosis["suggestions"] = [
                "Check if your API token is valid and not expired",
                "Verify the token has the correct permissions",
                "Ensure you're using the correct authentication method",
                "Check if your Confluence instance URL is correct",
            ]
        elif category == "authorization":
            diagnosis["suggestions"] = [
                "Verify you have permission to access the requested resource",
                "Check if the space or page exists and is accessible",
                "Ensure your user account has the required permissions",
                "Contact your Confluence administrator if needed",
            ]
        elif category == "not_found":
            diagnosis["suggestions"] = [
                "Verify the resource ID or key is correct",
                "Check if the resource has been deleted or moved",
                "Ensure you're using the correct API endpoint",
                "Try searching for the resource first",
            ]
        elif category == "rate_limit":
            diagnosis["suggestions"] = [
                "Implement exponential backoff and retry logic",
                "Reduce the frequency of API calls",
                "Consider using cursor pagination for large datasets",
                "Check your API usage against Confluence limits",
            ]
        elif category == "validation":
            diagnosis["suggestions"] = [
                "Validate your request data structure",
                "Check required fields are present",
                "Verify data types match API expectations",
                "Review the API documentation for correct format",
            ]
        elif category == "server_error":
            diagnosis["suggestions"] = [
                "Retry the request after a short delay",
                "Check Confluence status page for known issues",
                "Contact Atlassian support if the issue persists",
                "Implement proper error handling and logging",
            ]
        elif category == "network":
            diagnosis["suggestions"] = [
                "Check your internet connection",
                "Verify firewall settings allow API access",
                "Try increasing request timeout values",
                "Consider implementing connection pooling",
            ]

        return diagnosis


def demonstrate_authentication_errors():
    """
    Demonstrate handling authentication-related errors.
    """
    print("=== Authentication Error Handling ===\n")

    # Test with invalid credentials
    print("1. Testing invalid API token...")
    invalid_confluence = ConfluenceCloud(url=CONFLUENCE_URL, token="invalid-token-12345")
    invalid_confluence.enable_v2_api()

    error_handler = ConfluenceErrorHandler(invalid_confluence)

    # Try to get spaces with invalid token
    result = error_handler.safe_api_call(invalid_confluence._v2_client.get_spaces, limit=5)

    if result is None:
        print("   ✅ Invalid token error handled correctly")
    else:
        print("   ❌ Unexpected: Invalid token was accepted")

    # Test with invalid URL
    print("\n2. Testing invalid Confluence URL...")
    invalid_url_confluence = ConfluenceCloud(url="https://non-existent-domain.atlassian.net", token=API_TOKEN)
    invalid_url_confluence.enable_v2_api()

    error_handler_url = ConfluenceErrorHandler(invalid_url_confluence)

    result = error_handler_url.safe_api_call(
        invalid_url_confluence._v2_client.get_spaces, limit=5, max_retries=1  # Reduce retries for demo
    )

    if result is None:
        print("   ✅ Invalid URL error handled correctly")
    else:
        print("   ❌ Unexpected: Invalid URL was accepted")

    print("\n✅ Authentication error handling demonstrated!")


def demonstrate_validation_errors():
    """
    Demonstrate handling content validation errors.
    """
    print("=== Content Validation Error Handling ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()
    error_handler = ConfluenceErrorHandler(confluence)

    # Test ADF validation
    print("1. Testing ADF content validation...")

    # Valid ADF content
    valid_adf = {
        "version": 1,
        "type": "doc",
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Valid content"}]}],
    }

    is_valid, error_msg = error_handler.validate_adf_content(valid_adf)
    print(f"   Valid ADF: {is_valid} {f'- {error_msg}' if error_msg else ''}")

    # Invalid ADF content examples
    invalid_examples = [
        {"name": "Missing version", "content": {"type": "doc", "content": []}},
        {"name": "Wrong version", "content": {"version": 2, "type": "doc", "content": []}},
        {"name": "Missing content array", "content": {"version": 1, "type": "doc"}},
        {"name": "Invalid content node", "content": {"version": 1, "type": "doc", "content": ["invalid"]}},
    ]

    for example in invalid_examples:
        is_valid, error_msg = error_handler.validate_adf_content(example["content"])
        print(f"   {example['name']}: {is_valid} - {error_msg}")

    # Test API validation with invalid content
    print("\n2. Testing API validation with invalid content...")

    try:
        # Get a space to test with
        spaces_response = confluence._v2_client.get_spaces(limit=1)
        spaces = spaces_response.get("results", [])

        if spaces:
            space_id = spaces[0]["id"]

            # Try to create page with invalid ADF
            invalid_adf = {"invalid": "structure"}

            result = error_handler.safe_api_call(
                confluence._v2_client.create_page,
                space_id=space_id,
                title="Invalid Content Test",
                content=invalid_adf,
                content_format="adf",
                max_retries=0,  # Don't retry validation errors
            )

            if result is None:
                print("   ✅ Invalid ADF content rejected by API")
            else:
                print("   ❌ Unexpected: Invalid ADF was accepted")
        else:
            print("   No spaces available for testing")

    except Exception as e:
        print(f"   Error during validation test: {e}")

    print("\n✅ Validation error handling demonstrated!")


def demonstrate_rate_limiting():
    """
    Demonstrate handling rate limiting errors.
    """
    print("=== Rate Limiting Error Handling ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()
    error_handler = ConfluenceErrorHandler(confluence)

    print("1. Understanding rate limits...")
    rate_limits = {
        "Confluence Cloud": "Varies by plan (typically 1000 requests/hour)",
        "Burst limit": "Short-term higher limits for brief spikes",
        "Per-user limits": "Limits may apply per user account",
        "API endpoint limits": "Some endpoints may have specific limits",
    }

    for limit_type, description in rate_limits.items():
        print(f"   {limit_type}: {description}")

    print("\n2. Rate limit handling strategies...")
    strategies = [
        "Implement exponential backoff",
        "Monitor rate limit headers in responses",
        "Use cursor pagination to reduce API calls",
        "Cache frequently accessed data",
        "Batch operations when possible",
        "Implement request queuing",
    ]

    for strategy in strategies:
        print(f"   • {strategy}")

    print("\n3. Testing rate limit handling...")

    # Make several rapid API calls to demonstrate handling
    print("   Making rapid API calls to test handling...")

    for i in range(5):
        result = error_handler.safe_api_call(confluence._v2_client.get_spaces, limit=1, max_retries=1)

        if result:
            print(f"   Call {i+1}: Success ({len(result.get('results', []))} results)")
        else:
            print(f"   Call {i+1}: Failed (possibly rate limited)")

        # Small delay between calls
        time.sleep(0.1)

    print("\n4. Rate limit best practices:")
    best_practices = [
        "Monitor your API usage regularly",
        "Implement proper retry logic with backoff",
        "Use webhooks instead of polling when possible",
        "Cache data to reduce API calls",
        "Consider upgrading your Confluence plan for higher limits",
    ]

    for practice in best_practices:
        print(f"   • {practice}")

    print("\n✅ Rate limiting handling demonstrated!")


def demonstrate_debugging_techniques():
    """
    Demonstrate debugging techniques for API issues.
    """
    print("=== Debugging Techniques ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()
    error_handler = ConfluenceErrorHandler(confluence)

    print("1. Enabling detailed logging...")

    # Configure detailed logging
    logging.getLogger("atlassian").setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)

    print("   Logging configured for detailed output")

    print("\n2. API call inspection...")

    try:
        # Make an API call and inspect the process
        print("   Making API call with detailed logging...")

        response = confluence._v2_client.get_spaces(limit=2)

        print(f"   Response type: {type(response)}")
        print(f"   Response keys: {list(response.keys()) if isinstance(response, dict) else 'N/A'}")

        if isinstance(response, dict) and "results" in response:
            print(f"   Results count: {len(response['results'])}")

            # Show structure of first result
            if response["results"]:
                first_result = response["results"][0]
                print(f"   First result keys: {list(first_result.keys())}")

    except Exception as e:
        print(f"   Error during API call: {e}")

        # Diagnose the error
        diagnosis = error_handler.diagnose_api_issue(e)
        print(f"   Error diagnosis: {json.dumps(diagnosis, indent=2)}")

    print("\n3. Common debugging steps:")
    debugging_steps = [
        "Enable detailed logging for HTTP requests",
        "Inspect request and response headers",
        "Validate request payload structure",
        "Check API endpoint URLs and parameters",
        "Test with minimal examples first",
        "Use API testing tools (Postman, curl) for comparison",
        "Check Confluence instance status and version",
        "Review API documentation for changes",
    ]

    for step in debugging_steps:
        print(f"   • {step}")

    print("\n4. Useful debugging tools:")
    tools = {
        "requests-toolbelt": "HTTP request/response logging",
        "httpx": "Modern HTTP client with better debugging",
        "mitmproxy": "HTTP proxy for request inspection",
        "Postman": "API testing and documentation",
        "curl": "Command-line HTTP testing",
        "Browser DevTools": "Network tab for web-based debugging",
    }

    for tool, description in tools.items():
        print(f"   {tool}: {description}")

    print("\n✅ Debugging techniques demonstrated!")


def demonstrate_recovery_patterns():
    """
    Demonstrate recovery patterns for failed operations.
    """
    print("=== Recovery Patterns ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()
    error_handler = ConfluenceErrorHandler(confluence)

    print("1. Graceful degradation example...")

    def get_page_with_fallback(page_id: str) -> Optional[Dict[str, Any]]:
        """
        Get page with fallback to basic information if detailed fetch fails.
        """
        # Try to get full page details
        result = error_handler.safe_api_call(
            confluence._v2_client.get_page_by_id,
            page_id,
            expand=["body.atlas_doc_format", "version", "space"],
            max_retries=1,
        )

        if result:
            print(f"   ✅ Full page details retrieved for {page_id}")
            return result

        # Fallback: try basic page info
        print(f"   ⚠️ Falling back to basic page info for {page_id}")
        result = error_handler.safe_api_call(confluence._v2_client.get_page_by_id, page_id, max_retries=1)

        if result:
            print(f"   ✅ Basic page info retrieved for {page_id}")
            return result

        print(f"   ❌ Could not retrieve any info for {page_id}")
        return None

    # Test with a real page if available
    try:
        spaces_response = confluence._v2_client.get_spaces(limit=1)
        spaces = spaces_response.get("results", [])

        if spaces:
            space_id = spaces[0]["id"]
            pages_response = confluence._v2_client.get_pages(space_id=space_id, limit=1)
            pages = pages_response.get("results", [])

            if pages:
                test_page_id = pages[0]["id"]
                result = get_page_with_fallback(test_page_id)
                print(f"   Fallback test result: {'Success' if result else 'Failed'}")
            else:
                print("   No pages available for fallback testing")
        else:
            print("   No spaces available for fallback testing")

    except Exception as e:
        print(f"   Error during fallback test: {e}")

    print("\n2. Circuit breaker pattern...")

    class SimpleCircuitBreaker:
        """Simple circuit breaker implementation."""

        def __init__(self, failure_threshold: int = 3, timeout: int = 60):
            self.failure_threshold = failure_threshold
            self.timeout = timeout
            self.failure_count = 0
            self.last_failure_time = None
            self.state = "closed"  # closed, open, half-open

        def call(self, func, *args, **kwargs):
            """Execute function with circuit breaker protection."""
            if self.state == "open":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "half-open"
                    print("   Circuit breaker: half-open (testing)")
                else:
                    raise Exception("Circuit breaker is open")

            try:
                result = func(*args, **kwargs)
                if self.state == "half-open":
                    self.state = "closed"
                    self.failure_count = 0
                    print("   Circuit breaker: closed (recovered)")
                return result

            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
                    print("   Circuit breaker: open (too many failures)")

                raise e

    print("   Circuit breaker pattern helps prevent cascading failures")
    print("   States: closed (normal) → open (failing) → half-open (testing)")

    print("\n3. Recovery strategies:")
    strategies = [
        "Implement exponential backoff for retries",
        "Use circuit breakers to prevent cascading failures",
        "Provide graceful degradation with fallback options",
        "Cache data to serve during outages",
        "Queue operations for later retry",
        "Implement health checks and monitoring",
        "Use bulkhead pattern to isolate failures",
        "Provide user-friendly error messages",
    ]

    for strategy in strategies:
        print(f"   • {strategy}")

    print("\n✅ Recovery patterns demonstrated!")


def provide_troubleshooting_guide():
    """
    Provide a comprehensive troubleshooting guide.
    """
    print("=== Troubleshooting Guide ===\n")

    troubleshooting_steps = [
        {
            "issue": "Authentication Failures",
            "symptoms": ["401 Unauthorized", "Invalid token", "Access denied"],
            "solutions": [
                "Verify API token is correct and not expired",
                "Check token permissions and scopes",
                "Ensure correct Confluence instance URL",
                "Test with a fresh token",
                "Verify account has necessary permissions",
            ],
        },
        {
            "issue": "Content Creation Errors",
            "symptoms": ["400 Bad Request", "Invalid ADF", "Validation errors"],
            "solutions": [
                "Validate ADF structure before submission",
                "Check required fields are present",
                "Verify space ID exists and is accessible",
                "Test with minimal content first",
                "Review ADF documentation and examples",
            ],
        },
        {
            "issue": "Rate Limiting",
            "symptoms": ["429 Too Many Requests", "Rate limit exceeded"],
            "solutions": [
                "Implement exponential backoff",
                "Reduce request frequency",
                "Use cursor pagination",
                "Cache frequently accessed data",
                "Consider upgrading Confluence plan",
            ],
        },
        {
            "issue": "Network Issues",
            "symptoms": ["Connection timeout", "DNS resolution", "SSL errors"],
            "solutions": [
                "Check internet connectivity",
                "Verify firewall settings",
                "Test with different network",
                "Increase timeout values",
                "Check proxy settings",
            ],
        },
        {
            "issue": "Performance Problems",
            "symptoms": ["Slow responses", "Timeouts", "High memory usage"],
            "solutions": [
                "Use cursor pagination for large datasets",
                "Implement connection pooling",
                "Cache frequently accessed data",
                "Optimize query parameters",
                "Monitor API usage patterns",
            ],
        },
    ]

    for item in troubleshooting_steps:
        print(f"{item['issue']}:")
        print("  Symptoms:")
        for symptom in item["symptoms"]:
            print(f"    • {symptom}")
        print("  Solutions:")
        for solution in item["solutions"]:
            print(f"    • {solution}")
        print()

    print("General Debugging Checklist:")
    checklist = [
        "☐ Enable detailed logging",
        "☐ Test with minimal examples",
        "☐ Verify credentials and permissions",
        "☐ Check API endpoint URLs",
        "☐ Validate request payload",
        "☐ Monitor rate limits",
        "☐ Test network connectivity",
        "☐ Review error messages carefully",
        "☐ Check Confluence status page",
        "☐ Consult API documentation",
    ]

    for item in checklist:
        print(f"  {item}")

    print("\nUseful Resources:")
    resources = [
        "Confluence Cloud REST API v2 Documentation",
        "Atlassian Developer Community",
        "Confluence Status Page",
        "API Rate Limiting Guidelines",
        "ADF (Atlassian Document Format) Specification",
        "Atlassian Support Portal",
    ]

    for resource in resources:
        print(f"  • {resource}")


def main():
    """Main function demonstrating error handling and troubleshooting."""
    if CONFLUENCE_URL == "https://your-domain.atlassian.net" or API_TOKEN == "your-api-token":
        print("Please update the CONFLUENCE_URL and API_TOKEN variables with your credentials.")
        print("You can also set them as environment variables:")
        print("  export CONFLUENCE_URL='https://your-domain.atlassian.net'")
        print("  export CONFLUENCE_TOKEN='your-api-token'")
        return

    print("Confluence Cloud Error Handling and Troubleshooting")
    print("=" * 55)
    print()

    # Run all demonstrations
    demonstrate_authentication_errors()
    print("\n" + "-" * 55 + "\n")

    demonstrate_validation_errors()
    print("\n" + "-" * 55 + "\n")

    demonstrate_rate_limiting()
    print("\n" + "-" * 55 + "\n")

    demonstrate_debugging_techniques()
    print("\n" + "-" * 55 + "\n")

    demonstrate_recovery_patterns()
    print("\n" + "-" * 55 + "\n")

    provide_troubleshooting_guide()

    print("\n" + "=" * 55)
    print("Error handling demonstration completed!")
    print("\nKey takeaways:")
    print("1. Always implement proper error handling and retry logic")
    print("2. Validate content before submitting to the API")
    print("3. Monitor rate limits and implement backoff strategies")
    print("4. Use detailed logging for debugging issues")
    print("5. Implement graceful degradation and recovery patterns")
    print("6. Keep the troubleshooting guide handy for quick reference")


if __name__ == "__main__":
    # Allow configuration via environment variables
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL", CONFLUENCE_URL)
    API_TOKEN = os.getenv("CONFLUENCE_TOKEN", API_TOKEN)
    TEST_SPACE_KEY = os.getenv("TEST_SPACE_KEY", TEST_SPACE_KEY)

    main()
