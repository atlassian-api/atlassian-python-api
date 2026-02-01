#!/usr/bin/env python3
# coding=utf-8
"""
Example: Confluence Cloud Dual API Configuration

This example demonstrates how to configure and use both v1 and v2 APIs in the same application,
including when to use each API, how to switch between them, and best practices for dual API usage.

Key features demonstrated:
- Configuring dual API support
- Switching between v1 and v2 APIs dynamically
- API feature comparison and selection
- Migration strategies and compatibility
- Performance considerations
- Best practices for dual API applications

Prerequisites:
- Confluence Cloud instance
- API token (not username/password)
- Python 3.9+

Usage:
    python confluence_dual_api_configuration.py

Configuration:
    Update the CONFLUENCE_URL and API_TOKEN variables below with your credentials.
"""

import os
import sys
import time
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json

# Add the parent directory to the path to import atlassian
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from atlassian.confluence import ConfluenceCloud

# Configuration - Update these with your Confluence Cloud details
CONFLUENCE_URL = "https://your-domain.atlassian.net"
API_TOKEN = "your-api-token"
TEST_SPACE_KEY = "DEMO"  # Update with your test space key


class DualAPIManager:
    """
    Manager class for handling dual API configuration and operations.

    This class provides utilities for working with both v1 and v2 APIs,
    including automatic API selection based on operation requirements.
    """

    def __init__(self, confluence_client: ConfluenceCloud):
        """
        Initialize the dual API manager.

        Args:
            confluence_client: ConfluenceCloud client instance
        """
        self.confluence = confluence_client
        self.api_capabilities = self._analyze_api_capabilities()

    def _analyze_api_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """
        Analyze capabilities of both v1 and v2 APIs.

        Returns:
            Dictionary mapping API versions to their capabilities
        """
        return {
            "v1": {
                "content_format": "storage",
                "pagination": "offset",
                "id_format": "numeric",
                "space_reference": "key",
                "strengths": [
                    "Mature and stable",
                    "Extensive feature coverage",
                    "Well-documented",
                    "Backward compatibility",
                ],
                "limitations": ["Storage format complexity", "Less efficient pagination", "Older response structures"],
                "best_for": [
                    "Legacy integrations",
                    "Complex content manipulation",
                    "Operations not yet in v2",
                    "Backward compatibility requirements",
                ],
            },
            "v2": {
                "content_format": "adf",
                "pagination": "cursor",
                "id_format": "uuid",
                "space_reference": "id",
                "strengths": [
                    "Modern ADF content format",
                    "Efficient cursor pagination",
                    "Better performance",
                    "Cleaner response structures",
                ],
                "limitations": [
                    "Limited feature coverage (growing)",
                    "Newer, less battle-tested",
                    "Breaking changes possible",
                ],
                "best_for": [
                    "New integrations",
                    "High-performance applications",
                    "Modern content creation",
                    "Large dataset processing",
                ],
            },
        }

    def get_api_recommendation(self, operation: str) -> str:
        """
        Get API version recommendation for a specific operation.

        Args:
            operation: The operation to perform

        Returns:
            Recommended API version ('v1' or 'v2')
        """
        v2_operations = {
            "create_page_with_adf",
            "cursor_pagination",
            "bulk_page_processing",
            "modern_content_creation",
            "high_performance_reads",
        }

        v1_operations = {
            "complex_content_manipulation",
            "legacy_macro_handling",
            "advanced_space_management",
            "user_management",
            "detailed_permissions",
        }

        if operation in v2_operations:
            return "v2"
        elif operation in v1_operations:
            return "v1"
        else:
            # Default recommendation based on general capabilities
            return "v2" if self.confluence._v2_client else "v1"

    def execute_with_best_api(self, operation: str, **kwargs) -> Any:
        """
        Execute an operation using the most appropriate API version.

        Args:
            operation: The operation to perform
            kwargs: Operation parameters

        Returns:
            Operation result
        """
        recommended_api = self.get_api_recommendation(operation)

        print(f"   Executing '{operation}' with {recommended_api} API")

        if recommended_api == "v2" and self.confluence._v2_client:
            return self._execute_v2_operation(operation, **kwargs)
        else:
            return self._execute_v1_operation(operation, **kwargs)

    def _execute_v1_operation(self, operation: str, **kwargs) -> Any:
        """Execute operation using v1 API."""
        # Ensure v1 API is active
        self.confluence.disable_v2_api()

        if operation == "get_spaces":
            return self.confluence.get_spaces(**kwargs)
        elif operation == "get_pages":
            space_key = kwargs.get("space_key", TEST_SPACE_KEY)
            return self.confluence.get_all_pages_from_space(space=space_key, **kwargs)
        elif operation == "create_page":
            return self.confluence.create_page(**kwargs)
        else:
            raise ValueError(f"Unknown v1 operation: {operation}")

    def _execute_v2_operation(self, operation: str, **kwargs) -> Any:
        """Execute operation using v2 API."""
        # Ensure v2 API is active
        self.confluence.enable_v2_api()

        if operation == "get_spaces":
            return self.confluence._v2_client.get_spaces(**kwargs)
        elif operation == "get_pages":
            return self.confluence._v2_client.get_pages(**kwargs)
        elif operation == "create_page_with_adf":
            return self.confluence._v2_client.create_page(**kwargs)
        else:
            raise ValueError(f"Unknown v2 operation: {operation}")

    def compare_api_performance(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Compare performance between v1 and v2 APIs for an operation.

        Args:
            operation: The operation to compare
            kwargs: Operation parameters

        Returns:
            Performance comparison results
        """
        results = {
            "operation": operation,
            "v1": {"time": None, "result_count": None, "error": None},
            "v2": {"time": None, "result_count": None, "error": None},
        }

        # Test v1 API
        try:
            start_time = time.time()
            v1_result = self._execute_v1_operation(operation, **kwargs)
            v1_time = time.time() - start_time

            results["v1"]["time"] = v1_time
            if isinstance(v1_result, list):
                results["v1"]["result_count"] = len(v1_result)
            elif isinstance(v1_result, dict) and "results" in v1_result:
                results["v1"]["result_count"] = len(v1_result["results"])
        except Exception as e:
            results["v1"]["error"] = str(e)

        # Test v2 API
        try:
            start_time = time.time()
            v2_result = self._execute_v2_operation(operation, **kwargs)
            v2_time = time.time() - start_time

            results["v2"]["time"] = v2_time
            if isinstance(v2_result, dict) and "results" in v2_result:
                results["v2"]["result_count"] = len(v2_result["results"])
        except Exception as e:
            results["v2"]["error"] = str(e)

        return results


def demonstrate_dual_api_setup():
    """
    Demonstrate setting up dual API configuration.
    """
    print("=== Dual API Setup ===\n")

    # Initialize Confluence client
    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)

    print("1. Initial client configuration...")
    api_status = confluence.get_api_status()
    print(f"   Default API: {api_status.get('current_default')}")
    print(f"   v2 Available: {api_status.get('v2_available')}")
    print(f"   Force v2: {api_status.get('force_v2_api')}")
    print(f"   Prefer v2: {api_status.get('prefer_v2_api')}")

    print("\n2. Enabling v2 API support...")
    confluence.enable_v2_api()

    api_status = confluence.get_api_status()
    print(f"   Current API: {api_status.get('current_default')}")
    print(f"   v2 Client initialized: {confluence._v2_client is not None}")

    print("\n3. API switching demonstration...")

    # Switch to v1
    print("   Switching to v1 API...")
    confluence.disable_v2_api()
    api_status = confluence.get_api_status()
    print(f"   Current API: {api_status.get('current_default')}")

    # Switch back to v2
    print("   Switching to v2 API...")
    confluence.enable_v2_api()
    api_status = confluence.get_api_status()
    print(f"   Current API: {api_status.get('current_default')}")

    print("\n4. Dual API manager initialization...")
    dual_manager = DualAPIManager(confluence)

    print("   API capabilities analysis:")
    for version, capabilities in dual_manager.api_capabilities.items():
        print(f"   {version.upper()} API:")
        print(f"     Content format: {capabilities['content_format']}")
        print(f"     Pagination: {capabilities['pagination']}")
        print(f"     ID format: {capabilities['id_format']}")
        print(f"     Best for: {', '.join(capabilities['best_for'][:2])}")

    print("\n✅ Dual API setup completed!")

    return confluence, dual_manager


def demonstrate_api_selection():
    """
    Demonstrate automatic API selection based on operation type.
    """
    print("=== Automatic API Selection ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()
    dual_manager = DualAPIManager(confluence)

    print("1. API recommendations for different operations...")

    operations = [
        "create_page_with_adf",
        "cursor_pagination",
        "complex_content_manipulation",
        "legacy_macro_handling",
        "bulk_page_processing",
        "user_management",
    ]

    for operation in operations:
        recommendation = dual_manager.get_api_recommendation(operation)
        print(f"   {operation}: {recommendation} API")

    print("\n2. Executing operations with automatic API selection...")

    try:
        # Test get_spaces operation
        print("   Testing get_spaces operation...")
        result = dual_manager.execute_with_best_api("get_spaces", limit=3)

        if result and "results" in result:
            print(f"   Retrieved {len(result['results'])} spaces")
        elif isinstance(result, dict) and "results" in result:
            print(f"   Retrieved {len(result['results'])} spaces")
        else:
            print(f"   Result type: {type(result)}")

    except Exception as e:
        print(f"   Error: {e}")

    print("\n3. Operation-specific API usage patterns...")

    patterns = {
        "Content Creation": {
            "v1": "Use for complex Storage Format content",
            "v2": "Use for modern ADF content creation",
        },
        "Data Retrieval": {
            "v1": "Use for detailed metadata and legacy fields",
            "v2": "Use for high-performance bulk operations",
        },
        "Pagination": {"v1": "Use offset-based for small datasets", "v2": "Use cursor-based for large datasets"},
        "Content Format": {
            "v1": "Use when working with existing Storage Format",
            "v2": "Use for new applications with ADF",
        },
    }

    for category, apis in patterns.items():
        print(f"   {category}:")
        for api, usage in apis.items():
            print(f"     {api}: {usage}")

    print("\n✅ API selection demonstrated!")


def demonstrate_performance_comparison():
    """
    Demonstrate performance comparison between APIs.
    """
    print("=== Performance Comparison ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()
    dual_manager = DualAPIManager(confluence)

    print("1. Comparing get_spaces performance...")

    try:
        comparison = dual_manager.compare_api_performance("get_spaces", limit=5)

        print("   Results:")
        for api_version in ["v1", "v2"]:
            result = comparison[api_version]
            if result["error"]:
                print(f"   {api_version}: Error - {result['error']}")
            else:
                time_str = f"{result['time']:.3f}s" if result["time"] else "N/A"
                count_str = str(result["result_count"]) if result["result_count"] else "N/A"
                print(f"   {api_version}: {time_str}, {count_str} results")

        # Calculate performance difference
        v1_time = comparison["v1"]["time"]
        v2_time = comparison["v2"]["time"]

        if v1_time and v2_time:
            if v2_time < v1_time:
                improvement = ((v1_time - v2_time) / v1_time) * 100
                print(f"   v2 is {improvement:.1f}% faster than v1")
            else:
                degradation = ((v2_time - v1_time) / v1_time) * 100
                print(f"   v1 is {degradation:.1f}% faster than v2")

    except Exception as e:
        print(f"   Error during performance comparison: {e}")

    print("\n2. Performance considerations...")

    considerations = {
        "Network Overhead": {
            "v1": "More verbose responses, higher bandwidth",
            "v2": "Optimized responses, lower bandwidth",
        },
        "Parsing Complexity": {"v1": "Complex Storage Format parsing", "v2": "Structured ADF parsing"},
        "Pagination Efficiency": {
            "v1": "Offset-based, degrades with large offsets",
            "v2": "Cursor-based, consistent performance",
        },
        "Caching": {"v1": "Traditional HTTP caching", "v2": "Enhanced caching with better cache keys"},
    }

    for aspect, comparison in considerations.items():
        print(f"   {aspect}:")
        for api, description in comparison.items():
            print(f"     {api}: {description}")

    print("\n✅ Performance comparison completed!")


def demonstrate_migration_strategies():
    """
    Demonstrate strategies for migrating from v1 to v2 API.
    """
    print("=== Migration Strategies ===\n")

    print("1. Gradual migration approach...")

    migration_phases = [
        {
            "phase": "Phase 1: Assessment",
            "tasks": [
                "Audit existing v1 API usage",
                "Identify v2 equivalent operations",
                "Plan content format migration",
                "Set up dual API testing environment",
            ],
        },
        {
            "phase": "Phase 2: Infrastructure",
            "tasks": [
                "Implement dual API configuration",
                "Add API version selection logic",
                "Create content format converters",
                "Set up monitoring and logging",
            ],
        },
        {
            "phase": "Phase 3: Pilot Migration",
            "tasks": [
                "Migrate low-risk operations first",
                "Test with small user groups",
                "Monitor performance and errors",
                "Gather feedback and iterate",
            ],
        },
        {
            "phase": "Phase 4: Full Migration",
            "tasks": [
                "Migrate remaining operations",
                "Update documentation and training",
                "Monitor system stability",
                "Plan v1 API deprecation",
            ],
        },
    ]

    for phase_info in migration_phases:
        print(f"   {phase_info['phase']}:")
        for task in phase_info["tasks"]:
            print(f"     • {task}")
        print()

    print("2. Feature flag approach...")

    feature_flag_example = """
    ```python
    class ConfluenceService:
        def __init__(self, use_v2_api=False):
            self.confluence = ConfluenceCloud(url, token)
            self.use_v2_api = use_v2_api
            if use_v2_api:
                self.confluence.enable_v2_api()
        
        def create_page(self, space_id, title, content):
            if self.use_v2_api:
                return self._create_page_v2(space_id, title, content)
            else:
                return self._create_page_v1(space_id, title, content)
    ```
    """

    print(feature_flag_example)

    print("3. A/B testing strategy...")

    ab_testing_benefits = [
        "Compare performance between API versions",
        "Validate functionality equivalence",
        "Measure user experience impact",
        "Identify edge cases and issues",
        "Build confidence in migration",
    ]

    for benefit in ab_testing_benefits:
        print(f"   • {benefit}")

    print("\n4. Rollback planning...")

    rollback_considerations = [
        "Maintain v1 API compatibility during transition",
        "Implement quick API version switching",
        "Monitor key metrics and error rates",
        "Define rollback triggers and procedures",
        "Test rollback scenarios regularly",
    ]

    for consideration in rollback_considerations:
        print(f"   • {consideration}")

    print("\n✅ Migration strategies outlined!")


def demonstrate_best_practices():
    """
    Demonstrate best practices for dual API usage.
    """
    print("=== Best Practices for Dual API Usage ===\n")

    print("1. Configuration management...")

    config_practices = [
        "Use environment variables for API version selection",
        "Implement centralized API configuration",
        "Support runtime API switching for testing",
        "Document API version requirements clearly",
        "Version your API configuration changes",
    ]

    for practice in config_practices:
        print(f"   • {practice}")

    print("\n2. Error handling...")

    error_handling_example = """
    ```python
    def robust_api_call(operation, fallback_to_v1=True):
        try:
            # Try v2 API first
            confluence.enable_v2_api()
            return confluence._v2_client.operation()
        except Exception as e:
            if fallback_to_v1:
                logger.warning(f"v2 failed, falling back to v1: {e}")
                confluence.disable_v2_api()
                return confluence.operation()
            else:
                raise e
    ```
    """

    print(error_handling_example)

    print("3. Testing strategies...")

    testing_strategies = [
        "Test both API versions in CI/CD pipeline",
        "Use contract tests to ensure API compatibility",
        "Implement integration tests for dual API scenarios",
        "Test API switching and fallback mechanisms",
        "Monitor API usage patterns in production",
    ]

    for strategy in testing_strategies:
        print(f"   • {strategy}")

    print("\n4. Monitoring and observability...")

    monitoring_aspects = [
        "Track API version usage metrics",
        "Monitor performance differences",
        "Alert on API switching failures",
        "Log API selection decisions",
        "Measure migration progress",
    ]

    for aspect in monitoring_aspects:
        print(f"   • {aspect}")

    print("\n5. Documentation and training...")

    documentation_needs = [
        "Document when to use each API version",
        "Provide migration guides and examples",
        "Train team on dual API patterns",
        "Maintain API version compatibility matrix",
        "Update troubleshooting guides",
    ]

    for need in documentation_needs:
        print(f"   • {need}")

    print("\n✅ Best practices outlined!")


def main():
    """Main function demonstrating dual API configuration."""
    if CONFLUENCE_URL == "https://your-domain.atlassian.net" or API_TOKEN == "your-api-token":
        print("Please update the CONFLUENCE_URL and API_TOKEN variables with your credentials.")
        print("You can also set them as environment variables:")
        print("  export CONFLUENCE_URL='https://your-domain.atlassian.net'")
        print("  export CONFLUENCE_TOKEN='your-api-token'")
        return

    print("Confluence Cloud Dual API Configuration")
    print("=" * 45)
    print()

    # Run all demonstrations
    confluence, dual_manager = demonstrate_dual_api_setup()
    print("\n" + "-" * 45 + "\n")

    demonstrate_api_selection()
    print("\n" + "-" * 45 + "\n")

    demonstrate_performance_comparison()
    print("\n" + "-" * 45 + "\n")

    demonstrate_migration_strategies()
    print("\n" + "-" * 45 + "\n")

    demonstrate_best_practices()

    print("\n" + "=" * 45)
    print("Dual API configuration demonstration completed!")
    print("\nKey takeaways:")
    print("1. Use v2 API for new features and better performance")
    print("2. Keep v1 API for complex operations not yet in v2")
    print("3. Implement gradual migration with feature flags")
    print("4. Monitor both APIs during transition period")
    print("5. Plan for rollback scenarios and error handling")
    print("6. Document API selection criteria clearly")


if __name__ == "__main__":
    # Allow configuration via environment variables
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL", CONFLUENCE_URL)
    API_TOKEN = os.getenv("CONFLUENCE_TOKEN", API_TOKEN)
    TEST_SPACE_KEY = os.getenv("TEST_SPACE_KEY", TEST_SPACE_KEY)

    main()
