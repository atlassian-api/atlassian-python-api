#!/usr/bin/env python3
"""
Summary test file for the Confluence v2 API implementation.
This file imports and runs key test cases from all Confluence v2 test files.

Run this file to test the essential functionality of the Confluence v2 API:
    python -m unittest tests/test_confluence_v2_summary.py
"""

import unittest

# Import test classes from structure tests
from tests.test_confluence_v2_basic_structure import TestConfluenceV2BasicStructure

# Import test classes from mock tests (assuming this file exists)
try:
    from tests.test_confluence_v2_with_mocks import TestConfluenceV2WithMocks
except ImportError:
    print("Warning: tests/test_confluence_v2_with_mocks.py not found, skipping these tests")

# Import test classes from compatibility tests
try:
    from tests.test_confluence_version_compatibility import (
        TestConfluenceVersionCompatibility,
    )
except ImportError:
    print("Warning: tests/test_confluence_version_compatibility.py not found, skipping these tests")

# Note: Integration tests are not imported by default as they require real credentials


class TestConfluenceV2Summary(unittest.TestCase):
    """Summary test suite for the Confluence v2 API implementation."""

    def test_summary(self):
        """
        Dummy test to ensure the test runner works.
        The actual tests are imported from the other test files.
        """
        self.assertTrue(True)


if __name__ == "__main__":
    # Create test suite with all tests
    def create_test_suite():
        """Create a test suite with all tests."""
        test_suite = unittest.TestSuite()

        # Add basic structure tests
        test_suite.addTest(unittest.makeSuite(TestConfluenceV2BasicStructure))

        # Add mock tests if available
        if "TestConfluenceV2WithMocks" in globals():
            test_suite.addTest(unittest.makeSuite(TestConfluenceV2WithMocks))

        # Add compatibility tests if available
        if "TestConfluenceVersionCompatibility" in globals():
            test_suite.addTest(unittest.makeSuite(TestConfluenceVersionCompatibility))

        return test_suite

    # Run the tests
    runner = unittest.TextTestRunner()
    runner.run(create_test_suite())
