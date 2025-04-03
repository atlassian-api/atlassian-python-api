# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Jira V3 API support (Cloud and Server)
  - Base API implementation
  - Issue operations with ADF document format support
  - Enhanced error handling
  - Specialized client adapters for different Jira API areas
  - Rich text support via JiraADF helper
  - Improved pagination for search results
  - Migration guide from V2 to V3 API

### Fixed
- JQL pagination with small page sizes
- Various code style improvements to meet linting standards

### Changed
- Project versioning is now at 4.0.3
