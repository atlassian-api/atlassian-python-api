# Jira Server V3 API Integration Tests

This document provides instructions for running the integration tests for the Jira Server V3 API implementation in the Atlassian Python API client.

## Prerequisites

1. A Jira Server instance with admin access
2. Python 3.6 or higher
3. Dependencies installed (`pip install -r requirements.txt`)

## Setting Up Environment Variables

1. Create a `.env` file in the root directory of the project based on the `.env.example` file:

```
# Jira Server credentials for integration tests
JIRA_SERVER_URL=https://your-server-instance.example.com
JIRA_SERVER_USERNAME=your-username
JIRA_SERVER_PASSWORD=your-password
JIRA_SERVER_PROJECT_KEY=TEST
```

2. Replace placeholders with your actual Jira Server instance details:
   - `JIRA_SERVER_URL`: Your Jira Server instance URL
   - `JIRA_SERVER_USERNAME`: Your username for the Jira Server instance
   - `JIRA_SERVER_PASSWORD`: Your password for the Jira Server instance
   - `JIRA_SERVER_PROJECT_KEY`: A project key in your Jira Server instance that can be used for testing

## Running Integration Tests

### Running Tests Manually

```bash
# Load environment variables (bash/zsh)
source .env
# Or in Windows PowerShell
# Get-Content .env | ForEach-Object { $data = $_.Split('='); if($data[0] -and $data[1]) { Set-Item -Path "env:$($data[0])" -Value $data[1] } }

# Run tests
python -m unittest tests/test_jira_v3_server_integration.py -v
```

### Running Specific Test Classes or Methods

To run a specific test class:

```bash
python -m unittest tests.test_jira_v3_server_integration.TestJiraV3ServerIntegration
```

To run a specific test method:

```bash
python -m unittest tests.test_jira_v3_server_integration.TestJiraV3ServerIntegration.test_get_current_user
```

### Running Tests in Offline Mode

You can run the tests without an actual Jira Server instance using the offline mode with mocks:

```bash
JIRA_OFFLINE_TESTS=true python -m unittest tests/test_jira_v3_server_integration.py -v
```

This mode uses mock responses to simulate a Jira Server instance, which is useful for:
- Running tests in CI environments without access to a Jira Server
- Quick validation of code changes without hitting rate limits
- Testing error handling without needing to reproduce errors on a real instance

### Using the Convenience Script

A convenience script is provided to simplify running tests:

```bash
# Run Jira Server tests
./run_jira_v3_tests.sh --server

# Run a specific class
./run_jira_v3_tests.sh --server --class TestJiraV3ServerIntegration
```

## Key Test Cases

The integration tests for Jira Server include the following key test cases:

1. **Core Functionality Tests (TestJiraV3ServerIntegration)**
   - `test_get_current_user`: Verifies authentication and user data
   - `test_get_all_projects`: Tests retrieving projects list
   - `test_get_project`: Tests retrieving a single project
   - `test_search_issues`: Tests JQL search functionality
   - `test_pagination_handling`: Tests server-specific pagination

2. **Issue Operations Tests (TestJiraV3ServerIssuesIntegration)**
   - `test_create_and_get_issue`: Tests issue creation and retrieval
   - `test_update_issue`: Tests updating issue fields
   - `test_get_issue_transitions`: Tests retrieving valid transitions
   - `test_issue_comments`: Tests adding/updating comments

3. **Permissions Tests (TestJiraV3ServerPermissionsIntegration)**
   - `test_permission_handling`: Tests handling of permission-sensitive operations
   - `test_get_my_permissions`: Tests retrieving the current user's permissions

## Test Categories

The integration tests for Jira Server cover the following areas:

1. **Core Jira Functionality**: Basic API operations working with the server instance
2. **Issue Operations**: Issue CRUD operations, transitions, comments
3. **Project Operations**: Project components and versions

## Differences Between Server and Cloud

The Jira Server tests are designed to handle the differences between Server and Cloud instances:

1. **Authentication**: Server uses username/password rather than API tokens
2. **Response Format**: Server responses may have different field names or structures
3. **Comment Format**: Server may handle rich text differently than Cloud
4. **Error Handling**: Server may have different error messages or codes

## Troubleshooting

If you encounter issues:

1. Verify your environment variables are correctly set in the `.env` file
2. Ensure your credentials are valid
3. Check that your user has sufficient permissions in the Jira Server instance
4. Verify network connectivity to your Jira Server instance

For specific test failures, examine the error messages which often contain details about the API response that caused the failure.

## Adapting Tests for Your Environment

You may need to adapt the tests to match your specific Jira Server configuration:

1. Edit `tests/test_jira_v3_server_integration.py` to update issue creation data:
   - Update issue types to match those available in your project
   - Add any required custom fields specific to your Jira configuration

2. For permission-sensitive tests, you can use the `check_permissions` helper method which will skip tests that require administrative privileges if your user doesn't have them.

## Known Limitations

1. **API Version Compatibility**: Some Jira Server versions may not fully support the v3 API
2. **Feature Availability**: Not all Cloud features are available in Server instances
3. **Self-Hosted Considerations**: Firewalls, VPNs, or custom configurations may impact test connectivity

## Debugging Integration Tests

For more detailed debugging:

1. Increase logging level by modifying the `logging.basicConfig(level=logging.DEBUG)` line in the test file
2. Add print statements in specific test methods
3. Use more specific test runs to isolate issues
4. Check Jira Server logs for additional error information

## Contributing New Tests

When adding new tests:

1. Follow the existing pattern of creating test methods within the appropriate test class
2. Ensure tests are isolated and do not depend on the state from other tests
3. Clean up any created resources (like issues) at the end of tests
4. Add proper assertions to verify both structure and content of responses
5. Consider differences between Server and Cloud APIs
6. Use the `check_permissions` helper to gracefully handle permission issues 