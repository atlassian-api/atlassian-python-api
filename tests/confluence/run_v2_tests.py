#!/usr/bin/env python3
# coding=utf-8
"""
Test runner for Confluence Cloud v2 API test suite.

This script provides a convenient way to run the v2 API tests with different
configurations and options.
"""

import sys
import os
import subprocess
import argparse


def run_command(cmd, description=""):
    """Run a command and return the result."""
    print(f"\n{'=' * 60}")
    if description:
        print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)

    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")

    try:
        import pytest

        print(f"✓ pytest {pytest.__version__}")
    except ImportError:
        print("✗ pytest not found. Install with: pip install pytest")
        return False

    try:
        import atlassian  # noqa: F401

        print("✓ atlassian-python-api available")
    except ImportError:
        print("✗ atlassian-python-api not found")
        return False

    return True


def run_unit_tests(verbose=False, coverage=False):
    """Run unit tests for v2 API."""
    cmd = ["python", "-m", "pytest"]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(
            [
                "--cov=atlassian.confluence.cloud.v2",
                "--cov=atlassian.adf",
                "--cov=atlassian.request_utils",
                "--cov-report=html",
                "--cov-report=term",
            ]
        )

    # Run specific v2 API tests
    cmd.extend(
        [
            "tests/confluence/test_confluence_cloud_v2.py",
            "tests/confluence/test_confluence_dual_api.py",
            "tests/test_adf.py",
            "tests/test_request_utils_v2.py",
            "-m",
            "not integration",
        ]
    )

    return run_command(cmd, "Unit tests for v2 API")


def run_integration_tests(verbose=False):
    """Run integration tests for v2 API."""
    # Check if integration test configuration is available
    config_vars = ["CONFLUENCE_URL", "CONFLUENCE_TOKEN", "CONFLUENCE_SPACE_ID"]
    missing_vars = [var for var in config_vars if not os.getenv(var)]

    if missing_vars:
        print(f"\n⚠️  Integration tests skipped. Missing environment variables: {', '.join(missing_vars)}")
        print("\nTo run integration tests, set the following environment variables:")
        print("- CONFLUENCE_URL: Your Confluence Cloud URL")
        print("- CONFLUENCE_TOKEN: Your API token")
        print("- CONFLUENCE_SPACE_ID: Test space ID")
        print("\nExample:")
        print("export CONFLUENCE_URL='https://your-domain.atlassian.net'")
        print("export CONFLUENCE_TOKEN='your-api-token'")
        print("export CONFLUENCE_SPACE_ID='123456789'")
        return False

    cmd = ["python", "-m", "pytest"]

    if verbose:
        cmd.append("-v")

    cmd.extend(["tests/confluence/test_confluence_cloud_v2.py", "-m", "integration"])

    return run_command(cmd, "Integration tests for v2 API")


def run_backward_compatibility_tests(verbose=False):
    """Run backward compatibility tests."""
    cmd = ["python", "-m", "pytest"]

    if verbose:
        cmd.append("-v")

    cmd.extend(
        [
            "tests/confluence/test_backward_compatibility.py",
            "tests/confluence/test_confluence_dual_api.py::TestDualAPIBackwardCompatibility",
        ]
    )

    return run_command(cmd, "Backward compatibility tests")


def run_performance_tests(verbose=False):
    """Run performance comparison tests."""
    print("\n" + "=" * 60)
    print("Performance Tests")
    print("=" * 60)
    print("Performance tests would compare v1 vs v2 API performance.")
    print("This is a placeholder for future implementation.")
    return True


def run_all_tests(verbose=False, coverage=False, include_integration=False):
    """Run all test suites."""
    results = []

    print("🚀 Running Confluence Cloud v2 API Test Suite")
    print("=" * 60)

    # Unit tests
    results.append(("Unit Tests", run_unit_tests(verbose, coverage)))

    # Backward compatibility tests
    results.append(("Backward Compatibility", run_backward_compatibility_tests(verbose)))

    # Integration tests (if configured and requested)
    if include_integration:
        results.append(("Integration Tests", run_integration_tests(verbose)))

    # Performance tests
    results.append(("Performance Tests", run_performance_tests(verbose)))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:<25} {status}")
        if not passed:
            all_passed = False

    print("=" * 60)
    overall_status = "✓ ALL TESTS PASSED" if all_passed else "✗ SOME TESTS FAILED"
    print(f"Overall Result: {overall_status}")

    return all_passed


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run Confluence Cloud v2 API tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_v2_tests.py --all                    # Run all tests except integration
  python run_v2_tests.py --all --integration      # Run all tests including integration
  python run_v2_tests.py --unit --coverage        # Run unit tests with coverage
  python run_v2_tests.py --integration            # Run only integration tests
  python run_v2_tests.py --compatibility          # Run only compatibility tests
        """,
    )

    parser.add_argument("--all", action="store_true", help="Run all test suites")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--compatibility", action="store_true", help="Run backward compatibility tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--check-deps", action="store_true", help="Check dependencies only")

    args = parser.parse_args()

    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing dependencies.")
        return 1

    if args.check_deps:
        print("\n✅ All dependencies are available.")
        return 0

    # Determine what to run
    if args.all:
        success = run_all_tests(args.verbose, args.coverage, args.integration)
    elif args.unit:
        success = run_unit_tests(args.verbose, args.coverage)
    elif args.integration:
        success = run_integration_tests(args.verbose)
    elif args.compatibility:
        success = run_backward_compatibility_tests(args.verbose)
    elif args.performance:
        success = run_performance_tests(args.verbose)
    else:
        # Default: run unit tests
        print("No specific test suite specified. Running unit tests by default.")
        print("Use --help to see all options.")
        success = run_unit_tests(args.verbose, args.coverage)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
