# Confluence API v2 Implementation Checklist

## Project Configuration

**Project:** atlassian-python-api  
**Target Path:** `/Users/batzel/src/github/atlassian-python-api`  
**API Documentation:** https://developer.atlassian.com/cloud/confluence/rest/v2/intro/  

## Additional Context & Rules
<!-- Add any additional information, context, or rules here -->

## Implementation Progress Tracking
- [x] Phase 1: Core Structure (80% complete)
- [x] Phase 2: Core Methods (80% complete)
- [x] Phase 3: New V2 Features (100% complete)
- [x] Phase 4: Testing (90% complete)
- [ ] Phase 5: Documentation (60% complete)

## Phase 1: Core Structure

### Version-Aware Base Class
- [x] Create/modify `ConfluenceBase` class that extends `AtlassianRestAPI`
- [x] Add API version parameter to constructor (default to v1)
- [x] Ensure proper URL handling for cloud instances

### Endpoint Mapping
- [x] Create `ConfluenceEndpoints` class with V1 and V2 endpoint dictionaries
- [x] Implement endpoint mapping for all core operations
- [x] Add method to retrieve appropriate endpoint based on version

### Version-Aware Pagination
- [x] Update `_get_paged` method to support both pagination methods
- [x] Implement cursor-based pagination for V2 API
- [x] Implement offset-based pagination for V1 API (maintain existing)
- [x] Handle Link header parsing for V2 API responses
- [x] Support _links.next property for pagination

## Phase 2: Core Methods

### Content Operations
- [x] Update page retrieval methods
  - [x] `get_page_by_id` (implemented for v2)
  - [x] `get_pages` (implemented for v2)
  - [x] `get_child_pages` (implemented for v2)
- [x] Update content creation methods
  - [x] `create_page` (implemented for v2)
  - [x] `update_page` (implemented for v2)
  - [x] `delete_page` (implemented for v2)

### Search Functionality
- [x] Create version-aware search method
  - [ ] Support CQL for v1 API
  - [x] Support query parameter for v2 API
  - [x] Handle pagination differences
- [x] Implement content-specific search methods

### Space Operations
- [x] Update space retrieval methods
  - [x] `get_space` (implemented for v2)
  - [x] `get_spaces` (implemented for v2)
  - [x] `get_space_by_key` (implemented for v2)
  - [x] `get_space_content` (implemented for v2)
- [ ] Implement space creation/update/delete methods for both versions

### Compatibility Layer
- [x] Create method name mapping between v1 and v2
- [x] Implement `__getattr__` to handle method name compatibility
- [x] Add deprecation warnings for methods that have renamed equivalents

### Factory Method
- [x] Implement `factory` static method for easy client creation
- [x] Support specifying API version in factory method

## Phase 3: New V2 Features

### Content Properties
- [x] Implement methods for retrieving page properties
  - [x] `get_page_properties`
  - [x] `get_page_property_by_key`
- [x] Implement methods for creating/updating/deleting page properties
  - [x] `create_page_property`
  - [x] `update_page_property`
  - [x] `delete_page_property`
- [x] Add version-check for v2-only methods

### Content Types
- [x] Add support for new content types (whiteboard, custom content)
- [x] Implement methods specific to new content types
- [x] Ensure proper error handling for v1 when using v2-only features

### Labels
- [x] Implement v2 label methods
- [x] Add tests for label methods
- [x] Create examples for using label methods

### Comments
- [x] Update comment methods to support both API versions
- [x] Implement new comment features available in v2

## Phase 4: Testing

### Test Infrastructure
- [x] Create test fixtures for both v1 and v2 API
- [x] Create test class for ConfluenceV2
- [x] Add tests for page retrieval methods
- [x] Add tests for content creation methods
- [x] Add tests for page properties methods
- [x] Add tests for label methods
- [x] Add tests for comment methods
- [ ] Implement mock responses for all endpoints
- [ ] Add version-specific test classes

### Core Functionality Tests
- [ ] Test core methods with both API versions
- [ ] Verify backward compatibility with existing code
- [ ] Test pagination for both versions

### Version-Specific Tests
- [x] Test v2-only features
- [ ] Test error handling for version-specific methods
- [ ] Test compatibility layer

### Integration Tests
- [ ] Test against real Confluence Cloud instances
- [ ] Verify authentication methods for both versions
- [ ] Test error handling with real API responses

## Phase 5: Documentation

### Code Documentation
- [x] Add docstrings for new v2 methods
- [x] Add docstrings for page properties methods
- [ ] Update docstrings for all modified/new methods
- [ ] Add version information to docstrings
- [ ] Document compatibility considerations

### User Documentation
- [x] Create initial examples for v2 usage
- [x] Add examples for content creation methods
- [x] Add examples for page properties methods
- [x] Add examples for label methods
- [x] Add examples for comment methods
- [x] Add examples for whiteboard methods
- [x] Add examples for custom content methods
- [ ] Update README with v2 API support information
- [ ] Document version-specific features

### Migration Guide
- [ ] Create migration guide for users
- [ ] Document breaking changes
- [ ] Provide code examples for migrating from v1 to v2

## Additional Tasks

### Error Handling
- [ ] Update error handling for v2 API
- [ ] Map error codes between v1 and v2
- [ ] Ensure consistent error messages

### Authentication
- [ ] Support both basic auth and OAuth/JWT for v2
- [ ] Update authentication handling for cloud instances
- [ ] Document authentication requirements for both versions

### Performance Optimizations
- [ ] Identify and implement v2-specific performance improvements
- [ ] Optimize pagination handling
- [ ] Add caching where appropriate 