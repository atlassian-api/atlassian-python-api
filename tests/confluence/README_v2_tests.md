# Confluence Cloud v2 API Test Suite

This directory contains comprehensive tests for the Confluence Cloud v2 API implementation, including unit tests, integration tests, and backward compatibility validation.

## Test Structure

### Core Test Files

- **`test_confluence_cloud_v2.py`** - Main v2 API client tests
  - Unit tests with mocks for all v2 API methods
  - Integration tests for real API validation
  - Error handling and edge cases

- **`test_confluence_dual_api.py`** - Dual API support tests
  - Tests for seamless v1/v2 API switching
  - Backward compatibility validation
  - API routing and fallback logic

- **`test_adf.py`** - ADF (Atlassian Document Format) tests
  - ADF document creation and validation
  - Content format conversion utilities
  - Complex ADF structure handling

- **`test_request_utils_v2.py`** - Request utilities tests
  - Content format detection
  - ADF content validation
  - HTTP header generation

### Support Files

- **`integration_test_config.py`** - Integration test configuration
  - Environment variable management
  - Test helper utilities
  - Cleanup and setup functions

- **`run_v2_tests.py`** - Test runner script
  - Convenient test execution
  - Coverage reporting
  - Dependency checking

- **`test_backward_compatibility.py`** - Existing backward compatibility tests

## Running Tests

### Quick Start

```bash
# Run all unit tests
python tests/confluence/run_v2_tests.py --unit

# Run all tests with coverage
python tests/confluence/run_v2_tests.py --all --coverage

# Check dependencies
python tests/confluence/run_v2_tests.py --check-deps
```

### Using pytest directly

```bash
# Unit tests only
pytest tests/confluence/test_confluence_cloud_v2.py -m "not integration" -v

# All v2 API tests (unit only)
pytest tests/confluence/test_confluence_cloud_v2.py tests/confluence/test_confluence_dual_api.py tests/test_adf.py tests/test_request_utils_v2.py -m "not integration"

# Integration tests (requires configuration)
pytest tests/confluence/test_confluence_cloud_v2.py -m integration -v

# Backward compatibility tests
pytest tests/confluence/test_backward_compatibility.py -v
```

### Test Categories

Tests are organized using pytest markers:

- **Unit tests** (default) - Fast tests with mocks
- **Integration tests** (`-m integration`) - Tests against real API
- **Slow tests** (`-m slow`) - Long-running tests

## Integration Tests

Integration tests require a real Confluence Cloud instance and proper authentication.

### Environment Variables

Set these environment variables to enable integration tests:

```bash
# Required
export CONFLUENCE_URL="https://your-domain.atlassian.net"
export CONFLUENCE_TOKEN="your-api-token"
export CONFLUENCE_SPACE_ID="123456789"

# Optional
export CONFLUENCE_SPACE_KEY="TESTSPACE"
export CONFLUENCE_TEST_PAGE_PREFIX="V2_API_TEST"
```

### Getting API Token

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Create an API token
3. Use your email and the token for authentication

### Test Space Setup

1. Create a dedicated test space in Confluence Cloud
2. Get the space ID from the space settings
3. Ensure your API token has write access to the space

### Running Integration Tests

```bash
# Set environment variables
export CONFLUENCE_URL="https://your-domain.atlassian.net"
export CONFLUENCE_TOKEN="your-api-token"
export CONFLUENCE_SPACE_ID="123456789"

# Run integration tests
python tests/confluence/run_v2_tests.py --integration

# Or with pytest directly
pytest tests/confluence/test_confluence_cloud_v2.py -m integration -v
```

## Test Coverage

The test suite covers:

### v2 API Client (`ConfluenceCloudV2`)
- ✅ Page operations (CRUD)
- ✅ Space operations (read)
- ✅ Search with CQL
- ✅ Cursor-based pagination
- ✅ ADF content handling
- ✅ Error handling
- ✅ Content format conversion

### Dual API Support (`Cloud`)
- ✅ API version routing
- ✅ Backward compatibility
- ✅ Configuration management
- ✅ Fallback mechanisms
- ✅ Convenience methods

### ADF Utilities
- ✅ Document creation
- ✅ Structure validation
- ✅ Format conversion
- ✅ Complex content handling

### Request Utilities
- ✅ Content format detection
- ✅ ADF validation
- ✅ Header generation

## Test Data and Fixtures

### Mock Data
Tests use realistic mock data that matches actual API responses:
- Sample page responses with ADF content
- Paginated results with cursor links
- Error responses for edge cases

### ADF Test Content
- Simple text paragraphs
- Complex documents with headings, lists, formatting
- Invalid ADF structures for error testing

### Integration Test Data
- Temporary test pages (auto-cleanup)
- Unique naming to avoid conflicts
- Comprehensive ADF content examples

## Continuous Integration

### GitHub Actions
Tests are designed to run in CI/CD environments:

```yaml
# Example GitHub Actions configuration
- name: Run v2 API Tests
  run: |
    python tests/confluence/run_v2_tests.py --unit --coverage
    
# Integration tests (with secrets)
- name: Run Integration Tests
  env:
    CONFLUENCE_URL: ${{ secrets.CONFLUENCE_URL }}
    CONFLUENCE_TOKEN: ${{ secrets.CONFLUENCE_TOKEN }}
    CONFLUENCE_SPACE_ID: ${{ secrets.CONFLUENCE_SPACE_ID }}
  run: |
    python tests/confluence/run_v2_tests.py --integration
```

### Local Development
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests with coverage
python tests/confluence/run_v2_tests.py --all --coverage

# View coverage report
open htmlcov/index.html
```

## Test Development Guidelines

### Adding New Tests

1. **Unit Tests**: Add to appropriate test class in `test_confluence_cloud_v2.py`
2. **Integration Tests**: Add to `TestConfluenceCloudV2Integration` class
3. **Mock Data**: Add fixtures for reusable test data
4. **Error Cases**: Include negative test cases

### Test Naming Convention
- `test_method_name_scenario` - Basic test naming
- `test_method_name_with_parameter` - Parameter variations
- `test_method_name_error_condition` - Error scenarios
- `test_integration_method_name` - Integration tests

### Mock Guidelines
- Use `@patch.object()` for specific method mocking
- Create realistic mock responses
- Test both success and error scenarios
- Verify correct API calls are made

### Integration Test Guidelines
- Always clean up created resources
- Use unique names to avoid conflicts
- Test complete workflows (create → read → update → delete)
- Handle API rate limits gracefully

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure atlassian-python-api is installed
pip install -e .

# Or install in development mode
pip install -e .[dev]
```

**Integration Test Failures**
```bash
# Check environment variables
echo $CONFLUENCE_URL
echo $CONFLUENCE_TOKEN
echo $CONFLUENCE_SPACE_ID

# Verify API token permissions
curl -H "Authorization: Bearer $CONFLUENCE_TOKEN" \
     "$CONFLUENCE_URL/wiki/api/v2/spaces/$CONFLUENCE_SPACE_ID"
```

**Mock Test Failures**
- Check that mock return values match expected API response format
- Verify mock is patching the correct method path
- Ensure test data fixtures are valid

### Debug Mode

```bash
# Run with verbose output
pytest tests/confluence/test_confluence_cloud_v2.py -v -s

# Run specific test
pytest tests/confluence/test_confluence_cloud_v2.py::TestConfluenceCloudV2PageOperations::test_create_page_with_adf -v -s

# Debug integration tests
pytest tests/confluence/test_confluence_cloud_v2.py -m integration -v -s --tb=long
```

## Contributing

When adding new v2 API features:

1. Add unit tests with mocks
2. Add integration tests if applicable
3. Update backward compatibility tests
4. Add ADF utilities tests if needed
5. Update this documentation

### Test Quality Checklist
- [ ] Unit tests cover all code paths
- [ ] Integration tests validate real API behavior
- [ ] Error cases are tested
- [ ] Backward compatibility is maintained
- [ ] Mock data is realistic
- [ ] Tests are properly documented
- [ ] Cleanup is handled correctly

## Performance Considerations

### Test Execution Speed
- Unit tests should run in < 10 seconds
- Integration tests may take 30-60 seconds
- Use `pytest-xdist` for parallel execution

### API Rate Limits
- Integration tests respect Confluence Cloud rate limits
- Use delays between API calls if needed
- Batch operations where possible

### Resource Usage
- Clean up test resources promptly
- Use minimal test data sets
- Avoid creating large numbers of test pages

## Future Enhancements

Planned test improvements:
- [ ] Property-based testing with Hypothesis
- [ ] Performance benchmarking tests
- [ ] Load testing for pagination
- [ ] Cross-version compatibility tests
- [ ] Security testing for authentication
- [ ] Fuzz testing for ADF content