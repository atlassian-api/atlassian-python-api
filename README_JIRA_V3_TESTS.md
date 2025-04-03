# Jira V3 API Integration Tests

This document provides instructions for running the integration tests for the Jira V3 API implementation in the Atlassian Python API client.

## Prerequisites

1. A Jira Cloud instance with admin access
2. API token for your Jira account
3. Python 3.6 or higher
4. Dependencies installed (`pip install -r requirements.txt`)

## Setting Up Environment Variables

1. Create a `.env` file in the root directory of the project based on the `.env.example` file:

```
# Jira credentials for integration tests
JIRA_URL=https://your-instance.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_API_TOKEN=your-api-token
JIRA_PROJECT_KEY=TEST
```

2. Replace placeholders with your actual Jira instance details:
   - `JIRA_URL`: Your Jira instance URL
   - `JIRA_USERNAME`: Your email address registered with Atlassian
   - `JIRA_API_TOKEN`: Your API token (can be generated at https://id.atlassian.com/manage-profile/security/api-tokens)
   - `JIRA_PROJECT_KEY`: A project key in your Jira instance that can be used for testing

## Running Integration Tests

### Using the Script

We've provided a convenience script that handles environment setup:

```bash
./run_integration_tests.sh
```

This script will:
1. Check for the existence of the `.env` file
2. Load environment variables
3. Run the integration tests

### Running Tests Manually

If you prefer to run tests manually:

```bash
# Load environment variables (bash/zsh)
source .env
# Or in Windows PowerShell
# Get-Content .env | ForEach-Object { $data = $_.Split('='); if($data[0] -and $data[1]) { Set-Item -Path "env:$($data[0])" -Value $data[1] } }

# Run tests
python -m unittest tests/test_jira_v3_integration.py -v
```

## Test Categories

The integration tests cover the following areas:

1. **Core Jira Functionality**: Issue CRUD operations, searching, etc.
2. **User Operations**: User retrieval, search, and group management
3. **Project Operations**: Project CRUD, components, versions
4. **Issue Type Operations**: Issue type retrieval and configuration
5. **RichText Operations**: ADF document creation and handling
6. **Jira Software Features**: Boards, sprints, and backlog operations
7. **Permissions and Security**: Permission schemes and security levels

## Troubleshooting

If you encounter issues:

1. Verify your environment variables are correctly set in the `.env` file
2. Ensure your API token is valid and not expired
3. Check that your user has sufficient permissions in the Jira instance
4. Verify network connectivity to your Jira instance

For specific test failures, examine the error messages which often contain details about the API response that caused the failure.

## Contributing New Tests

When adding new tests:

1. Follow the existing pattern of creating test methods within the appropriate test class
2. Ensure tests are isolated and do not depend on the state from other tests
3. Clean up any created resources (like issues) at the end of tests
4. Add proper assertions to verify both structure and content of responses 

## Current Test Status

Based on the initial test run, the following issues were encountered:

1. **Project Key Issues**: Many tests failed with 404 errors for the project key. Ensure that:
   - The `JIRA_PROJECT_KEY` in your `.env` file is correct and exists in your Jira instance
   - Your user has appropriate permissions to access the project

2. **Authentication/Permission Issues**: Some tests failed with 403 errors, suggesting:
   - Insufficient permissions for administrative operations (common for field configurations)
   - API token might have limited scopes or the user doesn't have admin rights

3. **Issue Creation Failures**: Several tests failed during issue creation with 400 Bad Request:
   - Verify that the issue type specified in the tests exists in your project
   - Check if your project requires additional mandatory fields not included in the test data

## Adapting Tests for Your Environment

You may need to adapt the tests to match your specific Jira configuration:

1. Edit `tests/test_jira_v3_integration.py` to update issue creation data:
   - Update issue types to match those available in your project
   - Add any required custom fields specific to your Jira configuration

2. For permission-sensitive tests, you can implement conditional tests:
   ```python
   @unittest.skipIf(not os.environ.get('JIRA_ADMIN_ACCESS'), 'Admin access required')
   def test_admin_only_function(self):
       # Test code requiring admin access
   ```

## Debugging Integration Tests

To get more detailed output when tests fail:

1. Add print statements to problematic tests (as has been done for `test_create_and_get_issue`)
2. Run specific tests individually for clearer output:
   ```bash
   python -m unittest tests.test_jira_v3_integration.TestJiraV3Integration.test_get_current_user
   ```
3. Check Jira server logs if you have access to them 