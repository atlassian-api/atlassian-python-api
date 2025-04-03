#!/bin/bash
# Script to run Jira v3 API integration tests

# Check if .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found!"
  echo "Please create a .env file based on .env.example"
  exit 1
fi

# Load environment variables
echo "Loading environment variables from .env file..."
export $(grep -v '^#' .env | xargs)

# Function to run tests
run_tests() {
  test_type=$1
  test_file=$2
  test_class=$3

  echo "Running $test_type tests..."
  
  if [ -n "$test_class" ]; then
    echo "Testing class: $test_class"
    python -m unittest $test_file.$test_class -v
  else
    echo "Running all tests in: $test_file"
    python -m unittest $test_file -v
  fi
}

# Parse arguments
TEST_TYPE=""
TEST_CLASS=""

print_usage() {
  echo "Usage: $0 [--cloud|--server|--all] [--class TestClassName]"
  echo ""
  echo "Options:"
  echo "  --cloud        Run Jira Cloud v3 tests"
  echo "  --server       Run Jira Server v3 tests"
  echo "  --all          Run all Jira v3 tests (both Cloud and Server)"
  echo "  --class CLASS  Run specific test class (e.g. TestJiraV3Integration)"
  echo ""
  echo "Examples:"
  echo "  $0 --cloud"
  echo "  $0 --server --class TestJiraV3ServerIssuesIntegration"
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --cloud) TEST_TYPE="cloud"; shift ;;
    --server) TEST_TYPE="server"; shift ;;
    --all) TEST_TYPE="all"; shift ;;
    --class) TEST_CLASS="$2"; shift 2 ;;
    -h|--help) print_usage; exit 0 ;;
    *) echo "Unknown parameter: $1"; print_usage; exit 1 ;;
  esac
done

# Check for required arguments
if [ -z "$TEST_TYPE" ]; then
  echo "Error: Test type (--cloud, --server, or --all) must be specified."
  print_usage
  exit 1
fi

# Run tests based on arguments
if [ "$TEST_TYPE" = "cloud" ] || [ "$TEST_TYPE" = "all" ]; then
  # Check if cloud credentials are set
  if [ -z "$JIRA_URL" ] || [ -z "$JIRA_USERNAME" ] || [ -z "$JIRA_API_TOKEN" ]; then
    echo "Warning: Jira Cloud credentials not set. Skipping cloud tests."
  else
    run_tests "Jira Cloud" "tests.test_jira_v3_integration" "$TEST_CLASS"
  fi
fi

if [ "$TEST_TYPE" = "server" ] || [ "$TEST_TYPE" = "all" ]; then
  # Check if server credentials are set
  if [ -z "$JIRA_SERVER_URL" ] || [ -z "$JIRA_SERVER_USERNAME" ] || [ -z "$JIRA_SERVER_PASSWORD" ]; then
    echo "Warning: Jira Server credentials not set. Skipping server tests."
  else
    run_tests "Jira Server" "tests.test_jira_v3_server_integration" "$TEST_CLASS"
  fi
fi

echo "Testing completed." 