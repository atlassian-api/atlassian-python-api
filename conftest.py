"""Pytest collection configuration for repository-local diagnostic scripts."""

# These scripts perform live Confluence requests and are documented for manual
# execution in README_TEST_SCRIPTS.md.  Their names predate pytest's default
# ``test_*.py`` discovery pattern, so keep them out of the automated suite.
collect_ignore = ["test_pages.py", "test_search.py", "test_url_fix.py"]
