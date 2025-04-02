# Jira API v3 Implementation Checklist

## Project Configuration

**Project:** atlassian-python-api  
**Target Path:** `/Users/batzel/src/github/atlassian-python-api`  
**API Documentation:** 
- https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
- https://developer.atlassian.com/cloud/jira/software/rest/
- https://developer.atlassian.com/cloud/jira/service-desk/rest/

## Additional Context & Rules
- Maintain backward compatibility with v2 as much as possible
- Follow a similar implementation approach as the Confluence v2 implementation
- The primary difference in v3 is support for Atlassian Document Format (ADF) in text fields

## Implementation Progress Tracking
- [x] Phase 1: Core Structure (30% complete)
- [ ] Phase 2: Core Methods (0% complete)
- [ ] Phase 3: New V3 Features (0% complete)
- [ ] Phase 4: Testing (0% complete)
- [ ] Phase 5: Documentation (0% complete)

## Phase 1: Core Structure

### Version-Aware Base Class
- [x] Create `JiraBase` class that extends `AtlassianRestAPI`
- [x] Add API version parameter to constructor (default to v2)
- [ ] Move the current Jira class functionality to a version-specific implementation
- [x] Ensure proper URL handling for cloud instances

### Endpoint Mapping
- [x] Create `JiraEndpoints` class with V2 and V3 endpoint dictionaries
- [x] Implement endpoint mapping for all core operations
- [x] Add method to retrieve appropriate endpoint based on version

### Folder Structure
- [x] Create new directory structure with:
  - [x] `atlassian/jira/` as the base directory
  - [x] `atlassian/jira/base.py` for the base class
  - [x] `atlassian/jira/cloud/` for cloud-specific implementations
  - [x] `atlassian/jira/server/` for server-specific implementations
  - [x] `atlassian/jira/__init__.py` to maintain backward compatibility

### Version-Aware Pagination
- [x] Update `_get_paged` method to support both pagination methods
- [x] Implement proper pagination for V3 API
- [x] Maintain existing pagination for V2 API
- [ ] Handle pagination for cloud-specific endpoints

## Phase 2: Core Methods

### Authentication
- [ ] Ensure OAuth/JWT and basic auth work for both v2 and v3
- [ ] Support for API tokens for cloud instances
- [ ] Support for PATs (Personal Access Tokens) if applicable

### Issue Operations
- [ ] Update issue retrieval methods
  - [x] `get_issue` (implement for v3)
  - [ ] `issue_field_value` (implement for v3)
  - [ ] `get_issue_changelog` (implement for v3)
  - [ ] `get_issue_watchers` (implement for v3)
- [ ] Update issue creation/update methods
  - [ ] `create_issue` (implement for v3)
  - [ ] `update_issue` (implement for v3)
  - [ ] `delete_issue` (implement for v3)
  - [ ] Add ADF support for description and textArea fields

### Comment Operations
- [ ] Update comment methods
  - [x] `issue_add_comment` (implement for v3)
  - [ ] `issue_edit_comment` (implement for v3)
  - [ ] `issue_get_comment` (implement for v3)
  - [x] Add ADF support for comment bodies

### Worklog Operations
- [ ] Update worklog methods
  - [ ] `issue_add_json_worklog` (implement for v3)
  - [ ] `issue_worklog` (implement for v3)
  - [ ] `issue_get_worklog` (implement for v3)
  - [ ] Add ADF support for worklog comments

### Search Functionality
- [ ] Update search methods
  - [ ] `jql` (implement for v3)
  - [ ] `search` (implement for v3)
  - [ ] Ensure proper handling of ADF fields in results

### Project Operations
- [ ] Update project methods
  - [ ] `get_project` (implement for v3)
  - [ ] `get_all_projects` (implement for v3)
  - [ ] `create_project` (implement for v3)
  - [ ] `delete_project` (implement for v3)

### User Operations
- [ ] Update user methods
  - [ ] `get_user` (implement for v3)
  - [ ] `create_user` (implement for v3)
  - [ ] `delete_user` (implement for v3)
  - [ ] `user_find_by_user_string` (implement for v3)

### Compatibility Layer
- [x] Create method mapping between v2 and v3
- [ ] Implement `__getattr__` to handle method name compatibility
- [ ] Add deprecation warnings for methods that have renamed equivalents

### Factory Method
- [x] Implement `factory` static method for easy client creation
- [x] Support specifying API version in factory method

## Phase 3: New V3 Features

### Atlassian Document Format Support
- [x] Implement ADF helper methods for creating ADF content
- [ ] Create conversion utilities for plain text to ADF
- [ ] Add methods to handle ADF content in comments, descriptions, and text areas
- [ ] Add support for ADF inspection and manipulation

### Jira Software Specific Endpoints
- [ ] Add support for agile boards
- [ ] Add support for sprints
- [ ] Add support for backlog operations
- [ ] Add support for epics

### Jira Service Management Endpoints
- [ ] Add support for service desk operations
- [ ] Add support for customer operations
- [ ] Add support for request operations
- [ ] Add support for organization operations

### Enhanced Functionalites
- [ ] Support new custom field features
- [ ] Add webhook functionalities
- [ ] Support modern authentication methods
- [ ] Add new cloud-specific operations

## Phase 4: Testing

### Test Infrastructure
- [ ] Create test fixtures for both v2 and v3 API
- [ ] Create test class for JiraV3
- [ ] Add tests for issue methods
- [ ] Add tests for comment methods
- [ ] Add tests for worklog methods
- [ ] Add tests for search methods
- [ ] Add tests for user methods
- [ ] Add tests for project methods
- [ ] Implement mock responses for all endpoints
- [ ] Add version-specific test classes

### Core Functionality Tests
- [ ] Test core methods with both API versions
- [ ] Verify backward compatibility with existing code
- [ ] Test pagination for both versions
- [ ] Test ADF handling

### Version-Specific Tests
- [ ] Test v3-only features
- [ ] Test error handling for version-specific methods
- [ ] Test compatibility layer
- [ ] Test factory method

### Integration Tests
- [ ] Test against real Jira Cloud instances
- [ ] Verify authentication methods for both versions
- [ ] Test error handling with real API responses
- [ ] Test ADF handling with real data

## Phase 5: Documentation

### Code Documentation
- [ ] Add docstrings for new v3 methods
- [ ] Update docstrings for all modified methods
- [ ] Add version information to docstrings
- [ ] Document ADF handling
- [ ] Document compatibility considerations
- [ ] Document authentication requirements

### User Documentation
- [ ] Create initial examples for v3 usage
- [ ] Add examples for issue operations
- [ ] Add examples for comment operations
- [ ] Add examples for worklog operations
- [ ] Add examples for search operations
- [ ] Add examples for ADF handling
- [ ] Update README with v3 API support information
- [ ] Document version-specific features

### Migration Guide
- [ ] Create migration guide for users
- [ ] Document breaking changes (if any)
- [ ] Provide code examples for migrating from v2 to v3
- [ ] Document ADF conversion approaches 