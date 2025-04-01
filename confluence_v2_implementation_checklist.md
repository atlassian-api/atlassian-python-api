# Confluence API v2 Implementation Checklist

## Project Configuration

**Project:** atlassian-python-api  
**Target Path:** `/Users/batzel/src/github/atlassian-python-api`  
**API Documentation:** https://developer.atlassian.com/cloud/confluence/rest/v2/intro/  

## Additional Context & Rules
<!-- Add any additional information, context, or rules here -->

## Implementation Progress Tracking
- [x] Phase 1: Core Structure (80% complete)
- [ ] Phase 2: Core Methods (0% complete)
- [ ] Phase 3: New V2 Features (0% complete)
- [ ] Phase 4: Testing (10% complete)
- [ ] Phase 5: Documentation (0% complete)

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
- [ ] Update page retrieval methods
  - [ ] `get_page_by_id` (support both v1 and v2 endpoints)
  - [ ] `get_pages` (support both v1 and v2 endpoints)
  - [ ] `get_child_pages` (support both v1 and v2 endpoints)
- [ ] Update content creation methods
  - [ ] `create_page` (support both v1 and v2 request formats)
  - [ ] `update_page` (support both v1 and v2 request formats)
  - [ ] `delete_page` (support both v1 and v2 endpoints)

### Search Functionality
- [ ] Create version-aware search method
  - [ ] Support CQL for v1 API
  - [ ] Support query parameter for v2 API
  - [ ] Handle pagination differences
- [ ] Implement content-specific search methods

### Space Operations
- [ ] Update space retrieval methods
  - [ ] `get_space` (support both v1 and v2 endpoints)
  - [ ] `get_all_spaces` (support both v1 and v2 endpoints)
- [ ] Implement space creation/update/delete methods for both versions

### Compatibility Layer
- [ ] Create method name mapping between v1 and v2
- [ ] Implement `__getattr__` to handle method name compatibility
- [ ] Add deprecation warnings for methods that have renamed equivalents

### Factory Method
- [x] Implement `factory` static method for easy client creation
- [x] Support specifying API version in factory method

## Phase 3: New V2 Features

### Content Properties
- [ ] Implement methods for retrieving page properties
- [ ] Implement methods for creating/updating/deleting page properties
- [ ] Add version-check for v2-only methods

### Content Types
- [ ] Add support for new content types (whiteboard, custom content)
- [ ] Implement methods specific to new content types
- [ ] Ensure proper error handling for v1 when using v2-only features

### Labels
- [ ] Implement v2 label methods
- [ ] Update existing label methods to support both versions

### Comments
- [ ] Update comment methods to support both API versions
- [ ] Implement new comment features available in v2

## Phase 4: Testing

### Test Infrastructure
- [x] Create test fixtures for both v1 and v2 API
- [ ] Implement mock responses for all endpoints
- [ ] Add version-specific test classes

### Core Functionality Tests
- [ ] Test core methods with both API versions
- [ ] Verify backward compatibility with existing code
- [ ] Test pagination for both versions

### Version-Specific Tests
- [ ] Test v2-only features
- [ ] Test error handling for version-specific methods
- [ ] Test compatibility layer

### Integration Tests
- [ ] Test against real Confluence Cloud instances
- [ ] Verify authentication methods for both versions
- [ ] Test error handling with real API responses

## Phase 5: Documentation

### Code Documentation
- [ ] Update docstrings for all modified/new methods
- [ ] Add version information to docstrings
- [ ] Document compatibility considerations

### User Documentation
- [ ] Update README with v2 API support information
- [ ] Create examples for both v1 and v2 usage
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