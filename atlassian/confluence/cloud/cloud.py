#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Confluence Cloud API implementation
"""
import logging
import warnings
from typing import Dict, List, Optional, Union, Any, Tuple

from ..base import ConfluenceBase

log = logging.getLogger(__name__)

class ConfluenceCloud(ConfluenceBase):
    """
    Confluence Cloud API implementation class
    """

    def __init__(self, url: str, *args, **kwargs):
        """
        Initialize the ConfluenceCloud instance
        
        Args:
            url: The Confluence Cloud URL
            *args: Arguments to pass to ConfluenceBase
            **kwargs: Keyword arguments to pass to ConfluenceBase
        """
        # Cloud always uses V2 API
        kwargs.setdefault('api_version', 2)
        super().__init__(url, *args, **kwargs)

        # Warn about V1 method usage
        warnings.warn(
            "V1 methods are deprecated in ConfluenceCloud. Use V2 methods instead.",
            DeprecationWarning,
            stacklevel=2
        )
    
    def __getattr__(self, name):
        """
        Intercept attribute lookup to provide compatibility with v1 method names.
        
        Args:
            name: The attribute name being looked up
            
        Returns:
            The corresponding v2 method if a mapping exists
            
        Raises:
            AttributeError: If no mapping exists and the attribute isn't found
        """
        if name in self._compatibility_method_mapping:
            v2_method_name = self._compatibility_method_mapping[name]
            v2_method = getattr(self, v2_method_name)
            
            @functools.wraps(v2_method)
            def compatibility_wrapper(*args, **kwargs):
                warnings.warn(
                    f"The method '{name}' is deprecated in ConfluenceCloud. "
                    f"Use '{v2_method_name}' instead.",
                    DeprecationWarning, 
                    stacklevel=2
                )
                return v2_method(*args, **kwargs)
            
            return compatibility_wrapper
        
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def get_page_by_id(self, page_id: str, 
                       body_format: Optional[str] = None, 
                       get_body: bool = True,
                       expand: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Returns a page by ID in the v2 API format.
        
        API Version: 2 (Cloud only)
        
        Compatibility: This method provides similar functionality to the v1 get_page_by_id 
        but with a different parameter set and response structure.
        
        Args:
            page_id: The ID of the page to be returned
            body_format: (optional) The format of the page body to be returned. 
                         Valid values are 'storage', 'atlas_doc_format', or 'view'
            get_body: (optional) Whether to retrieve the page body. Default: True
            expand: (optional) A list of properties to expand in the response
                    Valid values: 'childTypes', 'children.page.metadata', 'children.attachment.metadata',
                    'children.comment.metadata', 'children', 'history', 'ancestors',
                    'body.atlas_doc_format', 'body.storage', 'body.view', 'version'
                    
        Returns:
            The page object in v2 API format
            
        Raises:
            HTTPError: If the API call fails
            ApiError: If the page does not exist or the user doesn't have permission to view it
        """
        endpoint = self.get_endpoint('page_by_id', id=page_id)
        params = {}
        
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
        
        if not get_body:
            params['body-format'] = 'none'
        
        if expand:
            params['expand'] = ','.join(expand)
            
        try:
            return self.get(endpoint, params=params)
        except Exception as e:
            log.error(f"Failed to retrieve page with ID {page_id}: {e}")
            raise

    def get_pages(self, 
                 space_id: Optional[str] = None,
                 title: Optional[str] = None,
                 status: Optional[str] = "current",
                 body_format: Optional[str] = None,
                 get_body: bool = False,
                 expand: Optional[List[str]] = None,
                 limit: int = 25,
                 sort: Optional[str] = None,
                 cursor: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns a list of pages based on the provided filters.
        
        API Version: 2 (Cloud only)
        
        Compatibility: This method is equivalent to get_all_pages_from_space in v1,
        but uses cursor-based pagination and supports more filtering options.
        
        Args:
            space_id: (optional) The ID of the space to get pages from
            title: (optional) Filter pages by title
            status: (optional) Filter pages by status, default is 'current'.
                   Valid values: 'current', 'archived', 'draft', 'trashed', 'deleted', 'any'
            body_format: (optional) The format of the page body to be returned. 
                         Valid values are 'storage', 'atlas_doc_format', or 'view'
            get_body: (optional) Whether to retrieve the page body. Default: False
            expand: (optional) A list of properties to expand in the response
            limit: (optional) Maximum number of pages to return per request. Default: 25
            sort: (optional) Sorting of the results. Format: [field] or [-field] for descending order
                 Valid fields: 'id', 'created-date', 'modified-date', 'title'
            cursor: (optional) Cursor for pagination. Use the cursor from _links.next in previous response
                    
        Returns:
            Dictionary containing results list and pagination information in v2 API format
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('page')
        params = {"limit": limit}
        
        if space_id:
            params["space-id"] = space_id
            
        if title:
            params["title"] = title
            
        if status:
            if status not in ('current', 'archived', 'draft', 'trashed', 'deleted', 'any'):
                raise ValueError("Status must be one of 'current', 'archived', 'draft', 'trashed', 'deleted', 'any'")
            params["status"] = status
            
        if not get_body:
            params['body-format'] = 'none'
        elif body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
        
        if expand:
            params['expand'] = ','.join(expand)
            
        if sort:
            valid_sort_fields = ['id', '-id', 'created-date', '-created-date', 
                                'modified-date', '-modified-date', 'title', '-title']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params['sort'] = sort
            
        if cursor:
            params["cursor"] = cursor
            
        try:
            return self.get(endpoint, params=params)
        except Exception as e:
            log.error(f"Failed to retrieve pages: {e}")
            raise
            
    def get_child_pages(self, 
                       parent_id: str,
                       status: Optional[str] = "current",
                       body_format: Optional[str] = None,
                       get_body: bool = False,
                       expand: Optional[List[str]] = None,
                       limit: int = 25,
                       sort: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Returns a list of child pages for the specified parent page.
        
        Args:
            parent_id: The ID of the parent page
            status: (optional) Filter pages by status, default is 'current'.
                   Valid values: 'current', 'archived', 'any'
            body_format: (optional) The format of the page body to be returned. 
                         Valid values are 'storage', 'atlas_doc_format', or 'view'
            get_body: (optional) Whether to retrieve the page body. Default: False
            expand: (optional) A list of properties to expand in the response
            limit: (optional) Maximum number of pages to return per request. Default: 25
            sort: (optional) Sorting of the results. Format: [field] or [-field] for descending order
                 Valid fields: 'id', 'created-date', 'modified-date', 'child-position'
                    
        Returns:
            List of child page objects in v2 API format
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('child_pages', id=parent_id)
        params = {"limit": limit}
            
        if status:
            # For child pages, only 'current', 'archived', and 'any' are valid
            if status not in ('current', 'archived', 'any'):
                raise ValueError("Status must be one of 'current', 'archived', 'any'")
            params["status"] = status
            
        if not get_body:
            params['body-format'] = 'none'
        elif body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
        
        if expand:
            params['expand'] = ','.join(expand)
            
        if sort:
            valid_sort_fields = ['id', '-id', 'created-date', '-created-date', 
                                'modified-date', '-modified-date', 
                                'child-position', '-child-position']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params['sort'] = sort
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to retrieve child pages: {e}")
            raise

    def create_page(self,
                    space_id: str,
                    title: str,
                    body: str,
                    parent_id: Optional[str] = None,
                    body_format: str = "storage",
                    status: str = "current",
                    representation: Optional[str] = None) -> Dict[str, Any]:
        """
        Creates a new page in Confluence.
        
        API Version: 2 (Cloud only)
        
        Compatibility: This method is equivalent to create_page in v1, but with parameter
        differences: space_id instead of space, simplified body format, and no content type.
        
        Args:
            space_id: The ID of the space where the page will be created
            title: The title of the page
            body: The content of the page
            parent_id: (optional) The ID of the parent page
            body_format: (optional) The format of the body. Default is 'storage'.
                         Valid values: 'storage', 'atlas_doc_format', 'wiki'
            status: (optional) The status of the page. Default is 'current'.
                    Valid values: 'current', 'draft'
            representation: (optional) The content representation - used only for wiki format.
                           Valid value: 'wiki'
                    
        Returns:
            The created page object in v2 API format
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If invalid parameters are provided
        """
        endpoint = self.get_endpoint('page')
        
        if body_format not in ('storage', 'atlas_doc_format', 'wiki'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'wiki'")
            
        if status not in ('current', 'draft'):
            raise ValueError("status must be one of 'current', 'draft'")
            
        if body_format == 'wiki' and representation != 'wiki':
            raise ValueError("representation must be 'wiki' when body_format is 'wiki'")
            
        data = {
            "spaceId": space_id,
            "status": status,
            "title": title,
            "body": {
                body_format: {
                    "value": body,
                    "representation": representation
                }
            }
        }
        
        # Remove representation field if None
        if representation is None:
            del data["body"][body_format]["representation"]
            
        # Add parent ID if provided
        if parent_id:
            data["parentId"] = parent_id
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create page: {e}")
            raise
            
    def update_page(self,
                    page_id: str,
                    title: Optional[str] = None,
                    body: Optional[str] = None,
                    body_format: str = "storage",
                    status: Optional[str] = None,
                    version: Optional[int] = None,
                    representation: Optional[str] = None) -> Dict[str, Any]:
        """
        Updates an existing page.
        
        API Version: 2 (Cloud only)
        
        Compatibility: This method is equivalent to update_page in v1, but requires
        the version number and uses a simplified body format. The v2 update requires
        at least one field (title, body, or status) to be provided.
        
        Args:
            page_id: The ID of the page to update
            title: (optional) The new title of the page
            body: (optional) The new content of the page
            body_format: (optional) The format of the body. Default is 'storage'.
                         Valid values: 'storage', 'atlas_doc_format', 'wiki'
            status: (optional) The new status of the page.
                    Valid values: 'current', 'draft', 'archived'
            version: (optional) The version number for concurrency control
                     If not provided, the current version will be incremented
            representation: (optional) The content representation - used only for wiki format.
                           Valid value: 'wiki'
                    
        Returns:
            The updated page object in v2 API format
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If invalid parameters are provided
        """
        endpoint = self.get_endpoint('page_by_id', id=page_id)
        
        # Validate parameters
        if body and body_format not in ('storage', 'atlas_doc_format', 'wiki'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'wiki'")
            
        if status and status not in ('current', 'draft', 'archived'):
            raise ValueError("status must be one of 'current', 'draft', 'archived'")
            
        if body_format == 'wiki' and representation != 'wiki':
            raise ValueError("representation must be 'wiki' when body_format is 'wiki'")
            
        # First, get the current page to get its version
        if version is None:
            try:
                current_page = self.get_page_by_id(page_id, get_body=False)
                version = current_page.get('version', {}).get('number', 1)
            except Exception as e:
                log.error(f"Failed to retrieve page for update: {e}")
                raise
                
        # Prepare update data
        data = {
            "id": page_id,
            "version": {
                "number": version + 1,  # Increment the version
                "message": "Updated via Python API"
            }
        }
        
        # Add optional fields
        if title:
            data["title"] = title
            
        if status:
            data["status"] = status
            
        if body:
            data["body"] = {
                body_format: {
                    "value": body
                }
            }
            if representation:
                data["body"][body_format]["representation"] = representation
            
        try:
            return self.put(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to update page: {e}")
            raise
            
    def delete_page(self, page_id: str) -> bool:
        """
        Deletes a page.
        
        Args:
            page_id: The ID of the page to delete
                    
        Returns:
            True if the page was successfully deleted, False otherwise
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('page_by_id', id=page_id)
        
        try:
            response = self.delete(endpoint)
            return True
        except Exception as e:
            log.error(f"Failed to delete page: {e}")
            raise

    def search(self, 
              query: str,
              cql: Optional[str] = None,
              cursor: Optional[str] = None,
              limit: int = 25,
              excerpt: bool = True,
              body_format: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for content in Confluence.
        
        Args:
            query: Text to search for
            cql: (optional) Confluence Query Language (CQL) expression to filter by
            cursor: (optional) Cursor to start searching from for pagination
            limit: (optional) Maximum number of results to return per request. Default: 25
            excerpt: (optional) Whether to include excerpts in the response. Default: True
            body_format: (optional) The format for the excerpt if excerpts are included.
                       Valid values: 'view', 'storage', or 'atlas_doc_format'
                       
        Returns:
            Dictionary with search results
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If invalid parameters are provided
        """
        endpoint = self.get_endpoint('search')
        params = {
            "limit": limit
        }
        
        # We need at least a text query or CQL
        if not query and not cql:
            raise ValueError("Either 'query' or 'cql' must be provided")
            
        if query:
            params["query"] = query
            
        if cql:
            params["cql"] = cql
            
        if cursor:
            params["cursor"] = cursor
            
        if not excerpt:
            params["excerpt"] = "false"
            
        if body_format:
            if body_format not in ('view', 'storage', 'atlas_doc_format'):
                raise ValueError("body_format must be one of 'view', 'storage', or 'atlas_doc_format'")
            params["body-format"] = body_format
            
        try:
            return self.get(endpoint, params=params)
        except Exception as e:
            log.error(f"Failed to perform search: {e}")
            raise
            
    def search_content(self, 
                      query: str, 
                      type: Optional[str] = None,
                      space_id: Optional[str] = None,
                      status: Optional[str] = "current",
                      limit: int = 25) -> List[Dict[str, Any]]:
        """
        Search for content with specific filters. This is a convenience method 
        that builds a CQL query and calls the search method.
        
        Args:
            query: Text to search for
            type: (optional) Content type to filter by. Valid values: 'page', 'blogpost', 'comment'
            space_id: (optional) Space ID to restrict search to
            status: (optional) Content status. Valid values: 'current', 'archived', 'draft', 'any'
            limit: (optional) Maximum number of results to return per request. Default: 25
                       
        Returns:
            List of content items matching the search criteria
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If invalid parameters are provided
        """
        cql_parts = []
        
        # Add text query
        cql_parts.append(f"text ~ \"{query}\"")
        
        # Add type filter
        if type:
            valid_types = ["page", "blogpost", "comment"]
            if type not in valid_types:
                raise ValueError(f"Type must be one of: {', '.join(valid_types)}")
            cql_parts.append(f"type = \"{type}\"")
            
        # Add space filter
        if space_id:
            cql_parts.append(f"space.id = \"{space_id}\"")
            
        # Add status filter
        if status:
            valid_statuses = ["current", "archived", "draft", "any"]
            if status not in valid_statuses:
                raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
            if status != "any":
                cql_parts.append(f"status = \"{status}\"")
                
        # Combine all CQL parts
        cql = " AND ".join(cql_parts)
        
        # Call the main search method
        result = self.search(query="", cql=cql, limit=limit)
        
        # Return just the results array
        return result.get("results", [])
        
    def get_spaces(self, 
                  ids: Optional[List[str]] = None,
                  keys: Optional[List[str]] = None,
                  type: Optional[str] = None,
                  status: Optional[str] = None,
                  labels: Optional[List[str]] = None,
                  sort: Optional[str] = None,
                  cursor: Optional[str] = None,
                  limit: int = 25) -> List[Dict[str, Any]]:
        """
        Returns all spaces, optionally filtered by provided parameters.
        
        Args:
            ids: (optional) List of space IDs to filter by
            keys: (optional) List of space keys to filter by
            type: (optional) Type of spaces to filter by. Valid values: 'global', 'personal'
            status: (optional) Status of spaces to filter by. Valid values: 'current', 'archived'
            labels: (optional) List of labels to filter by (matches any)
            sort: (optional) Sort order. Format: [field] or [-field] for descending
                  Valid fields: 'id', 'key', 'name', 'type', 'status'
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of spaces to return per request. Default: 25
                       
        Returns:
            List of space objects
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If invalid parameters are provided
        """
        endpoint = self.get_endpoint('spaces')
        params = {"limit": limit}
        
        # Add optional filters
        if ids:
            params["id"] = ",".join(ids)
            
        if keys:
            params["key"] = ",".join(keys)
            
        if type:
            if type not in ('global', 'personal'):
                raise ValueError("Type must be one of 'global', 'personal'")
            params["type"] = type
            
        if status:
            if status not in ('current', 'archived'):
                raise ValueError("Status must be one of 'current', 'archived'")
            params["status"] = status
            
        if labels:
            params["label"] = ",".join(labels)
            
        if sort:
            valid_sort_fields = ['id', '-id', 'key', '-key', 'name', '-name', 
                                'type', '-type', 'status', '-status']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params["sort"] = sort
            
        if cursor:
            params["cursor"] = cursor
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to retrieve spaces: {e}")
            raise
            
    def get_space(self, space_id: str) -> Dict[str, Any]:
        """
        Returns a specific space by ID.
        
        Args:
            space_id: The ID of the space to retrieve
                       
        Returns:
            Space object with details
            
        Raises:
            HTTPError: If the API call fails or the space doesn't exist
        """
        endpoint = self.get_endpoint('space_by_id', id=space_id)
        
        try:
            return self.get(endpoint)
        except Exception as e:
            log.error(f"Failed to retrieve space with ID {space_id}: {e}")
            raise
            
    def get_space_by_key(self, space_key: str) -> Dict[str, Any]:
        """
        Returns a specific space by key.
        This uses the get_spaces method with a key filter and returns the first match.
        
        Args:
            space_key: The key of the space to retrieve
                       
        Returns:
            Space object with details
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If no space with the specified key exists
        """
        try:
            spaces = self.get_spaces(keys=[space_key], limit=1)
            if not spaces:
                raise ValueError(f"No space found with key '{space_key}'")
            return spaces[0]
        except Exception as e:
            log.error(f"Failed to retrieve space with key {space_key}: {e}")
            raise
            
    def get_space_content(self,
                         space_id: str,
                         depth: Optional[str] = None,
                         sort: Optional[str] = None,
                         limit: int = 25) -> List[Dict[str, Any]]:
        """
        Returns the content of a space using the search method.
        This is a convenience method that builds a CQL query.
        
        Args:
            space_id: The ID of the space
            depth: (optional) Depth of the search. Valid values: 'root', 'all'
            sort: (optional) Sort order. Format: [field] or [-field] for descending
                  Valid fields: 'created', 'modified'
            limit: (optional) Maximum number of items to return. Default: 25
                       
        Returns:
            List of content items in the space
            
        Raises:
            HTTPError: If the API call fails
        """
        cql_parts = [f"space.id = \"{space_id}\""]
        
        # Add depth filter
        if depth == "root":
            cql_parts.append("ancestor = root")
        
        # Combine CQL parts
        cql = " AND ".join(cql_parts)
        
        # Define sort for the search
        search_params = {"cql": cql, "limit": limit}
        
        if sort:
            # Map sort fields to CQL sort fields
            sort_mappings = {
                "created": "created asc",
                "-created": "created desc",
                "modified": "lastmodified asc",
                "-modified": "lastmodified desc"
            }
            
            if sort in sort_mappings:
                search_params["cql"] += f" order by {sort_mappings[sort]}"
            else:
                valid_sorts = list(sort_mappings.keys())
                raise ValueError(f"Sort must be one of: {', '.join(valid_sorts)}")
                
        # Call search method
        result = self.search(query="", **search_params)
        
        # Return just the results array
        return result.get("results", [])
    
    def archive_space(self, space_key: str) -> Dict[str, Any]:
        """
        Archive a space.
        
        Args:
            space_key: The key of the space to archive
                       
        Returns:
            Response from the API
            
        Raises:
            HTTPError: If the API call fails or the space doesn't exist
        """
        endpoint = f"rest/api/space/{space_key}/archive"
        
        try:
            return self.put(endpoint, absolute=False)
        except Exception as e:
            log.error(f"Failed to archive space {space_key}: {e}")
            raise
            
    def get_trashed_contents_by_space(self, 
                                    space_key: str, 
                                    cursor: Optional[str] = None, 
                                    expand: Optional[List[str]] = None, 
                                    limit: int = 100) -> Dict[str, Any]:
        """
        Get trashed contents by space.
        
        Args:
            space_key: The key of the space
            cursor: (optional) Cursor for pagination
            expand: (optional) List of properties to expand
            limit: (optional) Maximum number of results to return. Default: 100
                       
        Returns:
            Response containing trashed content items
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = f"rest/api/space/{space_key}/content/trash"
        params = {"limit": limit}
        
        if cursor:
            params["cursor"] = cursor
            
        if expand:
            params["expand"] = ",".join(expand)
            
        try:
            return self.get(endpoint, params=params, absolute=False)
        except Exception as e:
            log.error(f"Failed to get trashed contents for space {space_key}: {e}")
            raise
    
    #--------------------------------------------------
    # Page Property Methods (Phase 3)
    #--------------------------------------------------
    
    def get_page_properties(self, page_id: str,
                           cursor: Optional[str] = None,
                           limit: int = 25) -> List[Dict[str, Any]]:
        """
        Returns all properties for a page.
        
        Args:
            page_id: The ID of the page
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of properties to return per request. Default: 25
                       
        Returns:
            List of page property objects
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('page_properties', id=page_id)
        params = {"limit": limit}
        
        if cursor:
            params["cursor"] = cursor
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to retrieve properties for page {page_id}: {e}")
            raise
    
    def get_page_property_by_key(self, page_id: str, property_key: str) -> Dict[str, Any]:
        """
        Returns a page property by key.
        
        Args:
            page_id: The ID of the page
            property_key: The key of the property to retrieve
                       
        Returns:
            The page property object
            
        Raises:
            HTTPError: If the API call fails or the property doesn't exist
        """
        endpoint = self.get_endpoint('page_property_by_key', id=page_id, key=property_key)
        
        try:
            return self.get(endpoint)
        except Exception as e:
            log.error(f"Failed to retrieve property {property_key} for page {page_id}: {e}")
            raise
    
    def create_page_property(self, page_id: str, 
                            property_key: str,
                            property_value: Any) -> Dict[str, Any]:
        """
        Creates a new property for a page.
        
        Args:
            page_id: The ID of the page
            property_key: The key of the property to create. Must only contain alphanumeric
                         characters and periods
            property_value: The value of the property. Can be any JSON-serializable value
                       
        Returns:
            The created page property object
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If the property_key has invalid characters
        """
        # Validate key format
        import re
        if not re.match(r'^[a-zA-Z0-9.]+$', property_key):
            raise ValueError("Property key must only contain alphanumeric characters and periods.")
        
        endpoint = self.get_endpoint('page_properties', id=page_id)
        
        data = {
            "key": property_key,
            "value": property_value
        }
        
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create property {property_key} for page {page_id}: {e}")
            raise
    
    def update_page_property(self, page_id: str, 
                            property_key: str,
                            property_value: Any,
                            version: Optional[int] = None) -> Dict[str, Any]:
        """
        Updates an existing property for a page.
        
        Args:
            page_id: The ID of the page
            property_key: The key of the property to update
            property_value: The new value of the property. Can be any JSON-serializable value
            version: (optional) The version number of the property for concurrency control.
                    If not provided, the current version will be retrieved and incremented
                       
        Returns:
            The updated page property object
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If the property doesn't exist
        """
        endpoint = self.get_endpoint('page_property_by_key', id=page_id, key=property_key)
        
        # Get current version if not provided
        if version is None:
            try:
                current_property = self.get_page_property_by_key(page_id, property_key)
                version = current_property.get('version', {}).get('number', 1)
            except Exception as e:
                raise ValueError(f"Property {property_key} doesn't exist for page {page_id}") from e
        
        data = {
            "key": property_key,
            "value": property_value,
            "version": {
                "number": version + 1,
                "message": "Updated via Python API"
            }
        }
        
        try:
            return self.put(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to update property {property_key} for page {page_id}: {e}")
            raise
    
    def delete_page_property(self, page_id: str, property_key: str) -> bool:
        """
        Deletes a property from a page.
        
        Args:
            page_id: The ID of the page
            property_key: The key of the property to delete
                       
        Returns:
            True if the property was successfully deleted, False otherwise
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('page_property_by_key', id=page_id, key=property_key)
        
        try:
            self.delete(endpoint)
            return True
        except Exception as e:
            log.error(f"Failed to delete property {property_key} for page {page_id}: {e}")
            raise

    #--------------------------------------------------
    # Label Methods (Phase 3)
    #--------------------------------------------------
    
    def get_page_labels(self, page_id: str, 
                       prefix: Optional[str] = None,
                       cursor: Optional[str] = None,
                       limit: int = 25) -> List[Dict[str, Any]]:
        """
        Returns all labels for a page.
        
        Args:
            page_id: The ID of the page
            prefix: (optional) Filter the results to labels with a specific prefix
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of labels to return per request. Default: 25
                       
        Returns:
            List of label objects
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('page_labels', id=page_id)
        params = {"limit": limit}
        
        if prefix:
            params["prefix"] = prefix
            
        if cursor:
            params["cursor"] = cursor
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to retrieve labels for page {page_id}: {e}")
            raise
    
    def add_page_label(self, page_id: str, label: str) -> Dict[str, Any]:
        """
        Adds a label to a page.
        
        Args:
            page_id: The ID of the page
            label: The label to add
                       
        Returns:
            The created label object
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If the label is invalid
        """
        if not label:
            raise ValueError("Label cannot be empty")
            
        endpoint = self.get_endpoint('page_labels', id=page_id)
        
        data = {
            "name": label
        }
        
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to add label '{label}' to page {page_id}: {e}")
            raise
    
    def add_page_labels(self, page_id: str, labels: List[str]) -> List[Dict[str, Any]]:
        """
        Adds multiple labels to a page.
        
        Args:
            page_id: The ID of the page
            labels: List of labels to add
                       
        Returns:
            List of created label objects
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If any of the labels are invalid
        """
        if not labels:
            raise ValueError("Labels list cannot be empty")
            
        endpoint = self.get_endpoint('page_labels', id=page_id)
        
        data = [{"name": label} for label in labels]
        
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to add labels {labels} to page {page_id}: {e}")
            raise
    
    def delete_page_label(self, page_id: str, label: str) -> bool:
        """
        Deletes a label from a page.
        
        Args:
            page_id: The ID of the page
            label: The label to delete
                       
        Returns:
            True if the label was successfully deleted, False otherwise
            
        Raises:
            HTTPError: If the API call fails
        """
        if not label:
            raise ValueError("Label cannot be empty")
            
        endpoint = self.get_endpoint('page_labels', id=page_id)
        params = {"name": label}
        
        try:
            self.delete(endpoint, params=params)
            return True
        except Exception as e:
            log.error(f"Failed to delete label '{label}' from page {page_id}: {e}")
            raise
    
    def get_space_labels(self, space_id: str,
                        prefix: Optional[str] = None,
                        cursor: Optional[str] = None,
                        limit: int = 25) -> List[Dict[str, Any]]:
        """
        Returns all labels for a space.
        
        Args:
            space_id: The ID of the space
            prefix: (optional) Filter the results to labels with a specific prefix
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of labels to return per request. Default: 25
                       
        Returns:
            List of label objects
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('space_labels', id=space_id)
        params = {"limit": limit}
        
        if prefix:
            params["prefix"] = prefix
            
        if cursor:
            params["cursor"] = cursor
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to retrieve labels for space {space_id}: {e}")
            raise
    
    def add_space_label(self, space_id: str, label: str) -> Dict[str, Any]:
        """
        Adds a label to a space.
        
        Args:
            space_id: The ID of the space
            label: The label to add
                       
        Returns:
            The created label object
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If the label is invalid
        """
        if not label:
            raise ValueError("Label cannot be empty")
            
        endpoint = self.get_endpoint('space_labels', id=space_id)
        
        data = {
            "name": label
        }
        
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to add label '{label}' to space {space_id}: {e}")
            raise
    
    def add_space_labels(self, space_id: str, labels: List[str]) -> List[Dict[str, Any]]:
        """
        Adds multiple labels to a space.
        
        Args:
            space_id: The ID of the space
            labels: List of labels to add
                       
        Returns:
            List of created label objects
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If any of the labels are invalid
        """
        if not labels:
            raise ValueError("Labels list cannot be empty")
            
        endpoint = self.get_endpoint('space_labels', id=space_id)
        
        data = [{"name": label} for label in labels]
        
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to add labels {labels} to space {space_id}: {e}")
            raise
    
    def delete_space_label(self, space_id: str, label: str) -> bool:
        """
        Delete a label from a space.
        
        Args:
            space_id: The ID of the space
            label: The name of the label to delete
                    
        Returns:
            True if successful
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('space_labels', id=space_id)
        
        try:
            self.delete(f"{endpoint}/{label}")
            return True
        except Exception as e:
            log.error(f"Failed to delete label '{label}' from space {space_id}: {e}")
            raise
            
    # Comment methods
    
    def get_page_footer_comments(self, 
                           page_id: str,
                           body_format: Optional[str] = None,
                           cursor: Optional[str] = None,
                           limit: int = 25,
                           sort: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get footer comments for a page.
        
        Args:
            page_id: ID of the page
            body_format: (optional) Format of the body to be returned. 
                        Valid values: 'storage', 'atlas_doc_format', 'view'
            cursor: (optional) Cursor to use for pagination
            limit: (optional) Maximum number of comments to return per request. Default: 25
            sort: (optional) Sort order for comments
                Valid values: 'created-date', '-created-date', 'modified-date', '-modified-date'
                
        Returns:
            List of footer comments
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('page_footer_comments', id=page_id)
        params = {"limit": limit}
        
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
            
        if cursor:
            params['cursor'] = cursor
            
        if sort:
            valid_sort_fields = ['created-date', '-created-date', 'modified-date', '-modified-date']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params['sort'] = sort
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get footer comments for page {page_id}: {e}")
            raise
            
    def get_page_inline_comments(self, 
                          page_id: str,
                          body_format: Optional[str] = None,
                          cursor: Optional[str] = None,
                          limit: int = 25,
                          sort: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get inline comments for a page.
        
        Args:
            page_id: ID of the page
            body_format: (optional) Format of the body to be returned. 
                        Valid values: 'storage', 'atlas_doc_format', 'view'
            cursor: (optional) Cursor to use for pagination
            limit: (optional) Maximum number of comments to return per request. Default: 25
            sort: (optional) Sort order for comments
                Valid values: 'created-date', '-created-date', 'modified-date', '-modified-date'
                
        Returns:
            List of inline comments
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('page_inline_comments', id=page_id)
        params = {"limit": limit}
        
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
            
        if cursor:
            params['cursor'] = cursor
            
        if sort:
            valid_sort_fields = ['created-date', '-created-date', 'modified-date', '-modified-date']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params['sort'] = sort
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get inline comments for page {page_id}: {e}")
            raise
            
    def get_blogpost_footer_comments(self, 
                              blogpost_id: str,
                              body_format: Optional[str] = None,
                              cursor: Optional[str] = None,
                              limit: int = 25,
                              sort: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get footer comments for a blog post.
        
        Args:
            blogpost_id: ID of the blog post
            body_format: (optional) Format of the body to be returned. 
                        Valid values: 'storage', 'atlas_doc_format', 'view'
            cursor: (optional) Cursor to use for pagination
            limit: (optional) Maximum number of comments to return per request. Default: 25
            sort: (optional) Sort order for comments
                Valid values: 'created-date', '-created-date', 'modified-date', '-modified-date'
                
        Returns:
            List of footer comments
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('blogpost_footer_comments', id=blogpost_id)
        params = {"limit": limit}
        
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
            
        if cursor:
            params['cursor'] = cursor
            
        if sort:
            valid_sort_fields = ['created-date', '-created-date', 'modified-date', '-modified-date']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params['sort'] = sort
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get footer comments for blog post {blogpost_id}: {e}")
            raise
            
    def get_blogpost_inline_comments(self, 
                             blogpost_id: str,
                             body_format: Optional[str] = None,
                             cursor: Optional[str] = None,
                             limit: int = 25,
                             sort: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get inline comments for a blog post.
        
        Args:
            blogpost_id: ID of the blog post
            body_format: (optional) Format of the body to be returned. 
                        Valid values: 'storage', 'atlas_doc_format', 'view'
            cursor: (optional) Cursor to use for pagination
            limit: (optional) Maximum number of comments to return per request. Default: 25
            sort: (optional) Sort order for comments
                Valid values: 'created-date', '-created-date', 'modified-date', '-modified-date'
                
        Returns:
            List of inline comments
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('blogpost_inline_comments', id=blogpost_id)
        params = {"limit": limit}
        
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
            
        if cursor:
            params['cursor'] = cursor
            
        if sort:
            valid_sort_fields = ['created-date', '-created-date', 'modified-date', '-modified-date']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params['sort'] = sort
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get inline comments for blog post {blogpost_id}: {e}")
            raise
            
    def get_attachment_comments(self, 
                          attachment_id: str,
                          body_format: Optional[str] = None,
                          cursor: Optional[str] = None,
                          limit: int = 25,
                          sort: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get comments for an attachment.
        
        Args:
            attachment_id: ID of the attachment
            body_format: (optional) Format of the body to be returned. 
                        Valid values: 'storage', 'atlas_doc_format', 'view'
            cursor: (optional) Cursor to use for pagination
            limit: (optional) Maximum number of comments to return per request. Default: 25
            sort: (optional) Sort order for comments
                Valid values: 'created-date', '-created-date', 'modified-date', '-modified-date'
                
        Returns:
            List of comments
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('attachment_comments', id=attachment_id)
        params = {"limit": limit}
        
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
            
        if cursor:
            params['cursor'] = cursor
            
        if sort:
            valid_sort_fields = ['created-date', '-created-date', 'modified-date', '-modified-date']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params['sort'] = sort
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get comments for attachment {attachment_id}: {e}")
            raise
            
    def get_custom_content_comments(self, 
                             custom_content_id: str,
                             body_format: Optional[str] = None,
                             cursor: Optional[str] = None,
                             limit: int = 25,
                             sort: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get comments for custom content.
        
        Args:
            custom_content_id: ID of the custom content
            body_format: (optional) Format of the body to be returned. 
                        Valid values: 'storage', 'atlas_doc_format', 'view'
            cursor: (optional) Cursor to use for pagination
            limit: (optional) Maximum number of comments to return per request. Default: 25
            sort: (optional) Sort order for comments
                Valid values: 'created-date', '-created-date', 'modified-date', '-modified-date'
                
        Returns:
            List of comments
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_comments', id=custom_content_id)
        params = {"limit": limit}
        
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
            
        if cursor:
            params['cursor'] = cursor
            
        if sort:
            valid_sort_fields = ['created-date', '-created-date', 'modified-date', '-modified-date']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params['sort'] = sort
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get comments for custom content {custom_content_id}: {e}")
            raise
            
    def get_comment_children(self, 
                       comment_id: str,
                       body_format: Optional[str] = None,
                       cursor: Optional[str] = None,
                       limit: int = 25,
                       sort: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get child comments for a comment.
        
        Args:
            comment_id: ID of the parent comment
            body_format: (optional) Format of the body to be returned. 
                        Valid values: 'storage', 'atlas_doc_format', 'view'
            cursor: (optional) Cursor to use for pagination
            limit: (optional) Maximum number of comments to return per request. Default: 25
            sort: (optional) Sort order for comments
                Valid values: 'created-date', '-created-date', 'modified-date', '-modified-date'
                
        Returns:
            List of child comments
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment_children', id=comment_id)
        params = {"limit": limit}
        
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
            
        if cursor:
            params['cursor'] = cursor
            
        if sort:
            valid_sort_fields = ['created-date', '-created-date', 'modified-date', '-modified-date']
            if sort not in valid_sort_fields:
                raise ValueError(f"Sort must be one of: {', '.join(valid_sort_fields)}")
            params['sort'] = sort
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get child comments for comment {comment_id}: {e}")
            raise
            
    def get_comment_by_id(self, 
                    comment_id: str,
                    body_format: Optional[str] = None,
                    version: Optional[int] = None) -> Dict[str, Any]:
        """
        Get a comment by ID.
        
        Args:
            comment_id: ID of the comment
            body_format: (optional) Format of the body to be returned. 
                        Valid values: 'storage', 'atlas_doc_format', 'view'
            version: (optional) Version number to retrieve
                
        Returns:
            Comment details
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment_by_id', id=comment_id)
        params = {}
        
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'view'")
            params['body-format'] = body_format
            
        if version:
            params['version'] = version
            
        try:
            return self.get(endpoint, params=params)
        except Exception as e:
            log.error(f"Failed to get comment {comment_id}: {e}")
            raise
            
    def create_page_footer_comment(self,
                            page_id: str,
                            body: str,
                            body_format: str = "storage") -> Dict[str, Any]:
        """
        Create a footer comment on a page.
        
        Args:
            page_id: ID of the page
            body: Body of the comment
            body_format: (optional) Format of the comment body. 
                        Valid values: 'storage', 'atlas_doc_format', 'wiki'
                
        Returns:
            The created comment
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment')
        
        if body_format not in ('storage', 'atlas_doc_format', 'wiki'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'wiki'")
            
        data = {
            "pageId": page_id,
            "body": {
                body_format: {
                    "representation": body_format,
                    "value": body
                }
            }
        }
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create footer comment on page {page_id}: {e}")
            raise
            
    def create_page_inline_comment(self,
                            page_id: str,
                            body: str,
                            inline_comment_properties: Dict[str, Any],
                            body_format: str = "storage") -> Dict[str, Any]:
        """
        Create an inline comment on a page.
        
        Args:
            page_id: ID of the page
            body: Body of the comment
            inline_comment_properties: Properties for inline comment, e.g.:
                {
                   "textSelection": "text to highlight",
                   "textSelectionMatchCount": 3,
                   "textSelectionMatchIndex": 1
                }
            body_format: (optional) Format of the comment body. 
                        Valid values: 'storage', 'atlas_doc_format', 'wiki'
                
        Returns:
            The created comment
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment')
        
        if body_format not in ('storage', 'atlas_doc_format', 'wiki'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'wiki'")
            
        required_props = ['textSelection', 'textSelectionMatchCount', 'textSelectionMatchIndex']
        for prop in required_props:
            if prop not in inline_comment_properties:
                raise ValueError(f"inline_comment_properties must contain '{prop}'")
            
        data = {
            "pageId": page_id,
            "body": {
                body_format: {
                    "representation": body_format,
                    "value": body
                }
            },
            "inlineCommentProperties": inline_comment_properties
        }
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create inline comment on page {page_id}: {e}")
            raise
            
    def create_blogpost_footer_comment(self,
                               blogpost_id: str,
                               body: str,
                               body_format: str = "storage") -> Dict[str, Any]:
        """
        Create a footer comment on a blog post.
        
        Args:
            blogpost_id: ID of the blog post
            body: Body of the comment
            body_format: (optional) Format of the comment body. 
                        Valid values: 'storage', 'atlas_doc_format', 'wiki'
                
        Returns:
            The created comment
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment')
        
        if body_format not in ('storage', 'atlas_doc_format', 'wiki'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'wiki'")
            
        data = {
            "blogPostId": blogpost_id,
            "body": {
                body_format: {
                    "representation": body_format,
                    "value": body
                }
            }
        }
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create footer comment on blog post {blogpost_id}: {e}")
            raise
            
    def create_custom_content_comment(self,
                              custom_content_id: str,
                              body: str,
                              body_format: str = "storage") -> Dict[str, Any]:
        """
        Create a comment on custom content.
        
        Args:
            custom_content_id: ID of the custom content
            body: Body of the comment
            body_format: (optional) Format of the comment body. 
                        Valid values: 'storage', 'atlas_doc_format', 'wiki'
                
        Returns:
            The created comment
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment')
        
        if body_format not in ('storage', 'atlas_doc_format', 'wiki'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'wiki'")
            
        data = {
            "customContentId": custom_content_id,
            "body": {
                body_format: {
                    "representation": body_format,
                    "value": body
                }
            }
        }
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create comment on custom content {custom_content_id}: {e}")
            raise
            
    def create_attachment_comment(self,
                           attachment_id: str,
                           body: str,
                           body_format: str = "storage") -> Dict[str, Any]:
        """
        Create a comment on an attachment.
        
        Args:
            attachment_id: ID of the attachment
            body: Body of the comment
            body_format: (optional) Format of the comment body. 
                        Valid values: 'storage', 'atlas_doc_format', 'wiki'
                
        Returns:
            The created comment
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment')
        
        if body_format not in ('storage', 'atlas_doc_format', 'wiki'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'wiki'")
            
        data = {
            "attachmentId": attachment_id,
            "body": {
                body_format: {
                    "representation": body_format,
                    "value": body
                }
            }
        }
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create comment on attachment {attachment_id}: {e}")
            raise
            
    def create_comment_reply(self,
                      parent_comment_id: str,
                      body: str,
                      body_format: str = "storage") -> Dict[str, Any]:
        """
        Create a reply to an existing comment.
        
        Args:
            parent_comment_id: ID of the parent comment
            body: Body of the comment
            body_format: (optional) Format of the comment body. 
                        Valid values: 'storage', 'atlas_doc_format', 'wiki'
                
        Returns:
            The created comment
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment')
        
        if body_format not in ('storage', 'atlas_doc_format', 'wiki'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'wiki'")
            
        data = {
            "parentCommentId": parent_comment_id,
            "body": {
                body_format: {
                    "representation": body_format,
                    "value": body
                }
            }
        }
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create reply to comment {parent_comment_id}: {e}")
            raise
            
    def update_comment(self,
                 comment_id: str,
                 body: str,
                 version: int,
                 body_format: str = "storage",
                 resolved: Optional[bool] = None) -> Dict[str, Any]:
        """
        Update an existing comment.
        
        Args:
            comment_id: ID of the comment
            body: Updated body of the comment
            version: Current version number of the comment (will increment by 1)
            body_format: (optional) Format of the comment body. 
                        Valid values: 'storage', 'atlas_doc_format', 'wiki'
            resolved: (optional) For inline comments - whether to mark as resolved
                
        Returns:
            The updated comment
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment_by_id', id=comment_id)
        
        if body_format not in ('storage', 'atlas_doc_format', 'wiki'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'wiki'")
            
        data = {
            "version": {
                "number": version + 1
            },
            "body": {
                body_format: {
                    "representation": body_format,
                    "value": body
                }
            }
        }
        
        if resolved is not None:
            data["resolved"] = resolved
            
        try:
            return self.put(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to update comment {comment_id}: {e}")
            raise
            
    def delete_comment(self, comment_id: str) -> bool:
        """
        Delete a comment.
        
        Args:
            comment_id: ID of the comment to delete
                
        Returns:
            True if successful
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('comment_by_id', id=comment_id)
            
        try:
            self.delete(endpoint)
            return True
        except Exception as e:
            log.error(f"Failed to delete comment {comment_id}: {e}")
            raise

    # V2-specific methods will be implemented here in Phase 2 and Phase 3 

    """
    ##############################################################################################
    #   Confluence Whiteboards API v2   #
    ##############################################################################################
    """
    
    def create_whiteboard(self, 
                         space_id: str, 
                         title: Optional[str] = None, 
                         parent_id: Optional[str] = None,
                         template_key: Optional[str] = None,
                         locale: Optional[str] = None) -> Dict[str, Any]:
        """
        Creates a new whiteboard in the specified space.
        
        Args:
            space_id: ID of the space where the whiteboard will be created
            title: (optional) Title of the new whiteboard
            parent_id: (optional) ID of the parent content
            template_key: (optional) Key of the template to use for the whiteboard
            locale: (optional) Locale for the template if template_key is provided
                
        Returns:
            Created whiteboard data
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('whiteboard')
        
        data = {
            "spaceId": space_id
        }
        
        if title is not None:
            data["title"] = title
            
        if parent_id is not None:
            data["parentId"] = parent_id
            
        if template_key is not None:
            data["templateKey"] = template_key
            
        if locale is not None:
            data["locale"] = locale
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create whiteboard in space {space_id}: {e}")
            raise
    
    def get_whiteboard_by_id(self, whiteboard_id: str) -> Dict[str, Any]:
        """
        Get a whiteboard by its ID.
        
        Args:
            whiteboard_id: ID of the whiteboard to retrieve
                
        Returns:
            Whiteboard data
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('whiteboard_by_id', id=whiteboard_id)
        
        try:
            return self.get(endpoint)
        except Exception as e:
            log.error(f"Failed to get whiteboard {whiteboard_id}: {e}")
            raise
            
    def delete_whiteboard(self, whiteboard_id: str) -> Dict[str, Any]:
        """
        Delete a whiteboard by its ID. 
        This moves the whiteboard to the trash, where it can be restored later.
        
        Args:
            whiteboard_id: ID of the whiteboard to delete
                
        Returns:
            Response data from the API
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('whiteboard_by_id', id=whiteboard_id)
        
        try:
            return self.delete(endpoint)
        except Exception as e:
            log.error(f"Failed to delete whiteboard {whiteboard_id}: {e}")
            raise
            
    def get_whiteboard_children(self, 
                               whiteboard_id: str, 
                               cursor: Optional[str] = None,
                               limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get the children of a whiteboard.
        
        Args:
            whiteboard_id: ID of the whiteboard
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of results to return
                
        Returns:
            List of whiteboard children
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('whiteboard_children', id=whiteboard_id)
        
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get children for whiteboard {whiteboard_id}: {e}")
            raise
            
    def get_whiteboard_ancestors(self, whiteboard_id: str) -> List[Dict[str, Any]]:
        """
        Get the ancestors of a whiteboard.
        
        Args:
            whiteboard_id: ID of the whiteboard
                
        Returns:
            List of ancestor content
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('whiteboard_ancestors', id=whiteboard_id)
        
        try:
            response = self.get(endpoint)
            return response.get("results", [])
        except Exception as e:
            log.error(f"Failed to get ancestors for whiteboard {whiteboard_id}: {e}")
            raise
    
    def get_space_whiteboards(self, 
                             space_id: str,
                             cursor: Optional[str] = None,
                             limit: int = 25) -> List[Dict[str, Any]]:
        """
        Get all whiteboards in a space.
        
        Args:
            space_id: ID or key of the space
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of results to return (default: 25)
                
        Returns:
            List of whiteboards in the space
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('whiteboard')
        
        params = {
            "spaceId": space_id, 
            "limit": limit
        }
        
        if cursor:
            params["cursor"] = cursor
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get whiteboards for space {space_id}: {e}")
            raise
    
    """
    ##############################################################################################
    #   Confluence Custom Content API (Cloud only)  #
    ##############################################################################################
    """
    
    def create_custom_content(self,
                             type: str,
                             title: str,
                             body: str,
                             space_id: Optional[str] = None,
                             page_id: Optional[str] = None,
                             blog_post_id: Optional[str] = None,
                             custom_content_id: Optional[str] = None,
                             status: str = "current",
                             body_format: str = "storage") -> Dict[str, Any]:
        """
        Creates a new custom content.
        
        Args:
            type: Type of custom content
            title: Title of the custom content
            body: Content body in the specified format
            space_id: (optional) ID of the containing space
            page_id: (optional) ID of the containing page
            blog_post_id: (optional) ID of the containing blog post
            custom_content_id: (optional) ID of the containing custom content
            status: (optional) Status of the custom content, default is "current".
                   Valid values are "current" or "draft"
            body_format: (optional) Format of the body. Default is "storage".
                        Valid values are "storage", "atlas_doc_format", or "raw"
                
        Returns:
            Created custom content data
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If invalid parameters are provided
        """
        endpoint = self.get_endpoint('custom_content')
        
        if body_format not in ('storage', 'atlas_doc_format', 'raw'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'raw'")
            
        if status not in ('current', 'draft'):
            raise ValueError("status must be one of 'current', 'draft'")
            
        # At least one container ID must be provided
        if not any([space_id, page_id, blog_post_id, custom_content_id]):
            raise ValueError("At least one container ID (space_id, page_id, blog_post_id, or custom_content_id) must be provided")
            
        data = {
            "type": type,
            "title": title,
            "body": {
                body_format: {
                    "representation": body_format,
                    "value": body
                }
            },
            "status": status
        }
        
        if space_id:
            data["spaceId"] = space_id
        if page_id:
            data["pageId"] = page_id
        if blog_post_id:
            data["blogPostId"] = blog_post_id
        if custom_content_id:
            data["customContentId"] = custom_content_id
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create custom content: {e}")
            raise
    
    def get_custom_content_by_id(self, 
                               custom_content_id: str,
                               body_format: Optional[str] = None) -> Dict[str, Any]:
        """
        Get custom content by its ID.
        
        Args:
            custom_content_id: ID of the custom content to retrieve
            body_format: (optional) Format to retrieve the body in.
                        Valid values: "storage", "atlas_doc_format", "raw", "view"
                
        Returns:
            Custom content data
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_by_id', id=custom_content_id)
        
        params = {}
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'raw', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'raw', 'view'")
            params["body-format"] = body_format
            
        try:
            return self.get(endpoint, params=params)
        except Exception as e:
            log.error(f"Failed to get custom content {custom_content_id}: {e}")
            raise
            
    def get_custom_content(self, 
                          type: Optional[str] = None,
                          space_id: Optional[str] = None,
                          page_id: Optional[str] = None,
                          blog_post_id: Optional[str] = None,
                          custom_content_id: Optional[str] = None,
                          id: Optional[List[str]] = None,
                          status: Optional[str] = None,
                          body_format: Optional[str] = None,
                          sort: Optional[str] = None,
                          cursor: Optional[str] = None,
                          limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get custom content with optional filtering.
        
        Args:
            type: (optional) Filter by custom content type
            space_id: (optional) Filter by space ID
            page_id: (optional) Filter by page ID
            blog_post_id: (optional) Filter by blog post ID
            custom_content_id: (optional) Filter by parent custom content ID
            id: (optional) List of custom content IDs to filter by
            status: (optional) Filter by status. Valid values: "current", "draft", "archived", "trashed", "deleted", "any"
            body_format: (optional) Format to retrieve the body in.
                        Valid values: "storage", "atlas_doc_format", "raw", "view"
            sort: (optional) Sort order. Example: "id", "-created-date"
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of results to return
                
        Returns:
            List of custom content
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content')
        
        params = {}
        if type:
            params["type"] = type
        if space_id:
            params["space-id"] = space_id
        if page_id:
            params["page-id"] = page_id
        if blog_post_id:
            params["blog-post-id"] = blog_post_id
        if custom_content_id:
            params["custom-content-id"] = custom_content_id
        if id:
            params["id"] = ",".join(id)
        if status:
            valid_statuses = ["current", "draft", "archived", "trashed", "deleted", "any"]
            if status not in valid_statuses:
                raise ValueError(f"status must be one of {valid_statuses}")
            params["status"] = status
        if body_format:
            if body_format not in ('storage', 'atlas_doc_format', 'raw', 'view'):
                raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'raw', 'view'")
            params["body-format"] = body_format
        if sort:
            params["sort"] = sort
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get custom content: {e}")
            raise
            
    def update_custom_content(self,
                           custom_content_id: str,
                           type: str,
                           title: str,
                           body: str,
                           status: str,
                           version_number: int,
                           space_id: Optional[str] = None,
                           page_id: Optional[str] = None,
                           blog_post_id: Optional[str] = None,
                           parent_custom_content_id: Optional[str] = None,
                           body_format: str = "storage",
                           version_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Updates existing custom content.
        
        Args:
            custom_content_id: ID of the custom content to update
            type: Type of custom content
            title: Title of the custom content
            body: Content body in the specified format
            status: Status of the custom content. Must be "current"
            version_number: New version number (should be current version number + 1)
            space_id: (optional) ID of the containing space (must be same as original)
            page_id: (optional) ID of the containing page
            blog_post_id: (optional) ID of the containing blog post
            parent_custom_content_id: (optional) ID of the containing custom content
            body_format: (optional) Format of the body. Default is "storage".
                        Valid values are "storage", "atlas_doc_format", or "raw"
            version_message: (optional) Message for the new version
                
        Returns:
            Updated custom content data
            
        Raises:
            HTTPError: If the API call fails
            ValueError: If invalid parameters are provided
        """
        endpoint = self.get_endpoint('custom_content_by_id', id=custom_content_id)
        
        if body_format not in ('storage', 'atlas_doc_format', 'raw'):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', 'raw'")
            
        if status != "current":
            raise ValueError("status must be 'current' for updates")
            
        data = {
            "id": custom_content_id,
            "type": type,
            "title": title,
            "body": {
                body_format: {
                    "representation": body_format,
                    "value": body
                }
            },
            "status": status,
            "version": {
                "number": version_number
            }
        }
        
        if version_message:
            data["version"]["message"] = version_message
            
        if space_id:
            data["spaceId"] = space_id
        if page_id:
            data["pageId"] = page_id
        if blog_post_id:
            data["blogPostId"] = blog_post_id
        if parent_custom_content_id:
            data["customContentId"] = parent_custom_content_id
            
        try:
            return self.put(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to update custom content {custom_content_id}: {e}")
            raise
            
    def delete_custom_content(self, custom_content_id: str) -> Dict[str, Any]:
        """
        Delete custom content by its ID.
        This moves the custom content to the trash, where it can be restored later.
        
        Args:
            custom_content_id: ID of the custom content to delete
                
        Returns:
            Response data from the API
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_by_id', id=custom_content_id)
        
        try:
            return self.delete(endpoint)
        except Exception as e:
            log.error(f"Failed to delete custom content {custom_content_id}: {e}")
            raise
            
    def get_custom_content_children(self, 
                                  custom_content_id: str, 
                                  cursor: Optional[str] = None,
                                  limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get the children of custom content.
        
        Args:
            custom_content_id: ID of the custom content
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of results to return
                
        Returns:
            List of custom content children
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_children', id=custom_content_id)
        
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get children for custom content {custom_content_id}: {e}")
            raise
            
    def get_custom_content_ancestors(self, custom_content_id: str) -> List[Dict[str, Any]]:
        """
        Get the ancestors of custom content.
        
        Args:
            custom_content_id: ID of the custom content
                
        Returns:
            List of ancestor content
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_ancestors', id=custom_content_id)
        
        try:
            response = self.get(endpoint)
            return response.get("results", [])
        except Exception as e:
            log.error(f"Failed to get ancestors for custom content {custom_content_id}: {e}")
            raise
            
    # Custom content labels methods
    
    def get_custom_content_labels(self, 
                               custom_content_id: str,
                               prefix: Optional[str] = None,
                               sort: Optional[str] = None,
                               cursor: Optional[str] = None,
                               limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieves labels for a custom content.
        
        Args:
            custom_content_id: ID of the custom content
            prefix: (optional) Filters labels by prefix
            sort: (optional) Sorts labels by specified field
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of results to return (default: 25)
                
        Returns:
            List of labels for the custom content
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_labels', id=custom_content_id)
        
        params = {}
        if prefix:
            params["prefix"] = prefix
        if sort:
            params["sort"] = sort
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get labels for custom content {custom_content_id}: {e}")
            raise
            
    def add_custom_content_label(self, custom_content_id: str, label: str, prefix: Optional[str] = None) -> Dict[str, Any]:
        """
        Adds a label to custom content.
        
        Args:
            custom_content_id: ID of the custom content
            label: The label to add
            prefix: (optional) The prefix for the label
                
        Returns:
            The added label
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_labels', id=custom_content_id)
        
        data = {
            "name": label,
        }
        
        if prefix:
            data["prefix"] = prefix
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to add label to custom content {custom_content_id}: {e}")
            raise
            
    def delete_custom_content_label(self, custom_content_id: str, label: str, prefix: Optional[str] = None) -> None:
        """
        Deletes a label from custom content.
        
        Args:
            custom_content_id: ID of the custom content
            label: The label to delete
            prefix: (optional) The prefix for the label
                
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_labels', id=custom_content_id)
        
        params = {
            "name": label
        }
        
        if prefix:
            params["prefix"] = prefix
            
        try:
            self.delete(endpoint, params=params)
        except Exception as e:
            log.error(f"Failed to delete label from custom content {custom_content_id}: {e}")
            raise
    
    # Custom content properties methods
    
    def get_custom_content_properties(self, 
                                    custom_content_id: str, 
                                    sort: Optional[str] = None,
                                    cursor: Optional[str] = None,
                                    limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieves properties for a custom content.
        
        Args:
            custom_content_id: ID of the custom content
            sort: (optional) Sorts properties by specified field
            cursor: (optional) Cursor for pagination
            limit: (optional) Maximum number of results to return (default: 25)
                
        Returns:
            List of properties for the custom content
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_properties', id=custom_content_id)
        
        params = {}
        if sort:
            params["sort"] = sort
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
            
        try:
            return list(self._get_paged(endpoint, params=params))
        except Exception as e:
            log.error(f"Failed to get properties for custom content {custom_content_id}: {e}")
            raise
            
    def get_custom_content_property_by_key(self, custom_content_id: str, property_key: str) -> Dict[str, Any]:
        """
        Retrieves a specific property for a custom content by key.
        
        Args:
            custom_content_id: ID of the custom content
            property_key: Key of the property to retrieve
                
        Returns:
            The property
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_property_by_key', id=custom_content_id, key=property_key)
        
        try:
            return self.get(endpoint)
        except Exception as e:
            log.error(f"Failed to get property {property_key} for custom content {custom_content_id}: {e}")
            raise
            
    def create_custom_content_property(self, custom_content_id: str, key: str, value: Any) -> Dict[str, Any]:
        """
        Creates a property for a custom content.
        
        Args:
            custom_content_id: ID of the custom content
            key: Key of the property
            value: Value of the property (must be JSON serializable)
                
        Returns:
            The created property
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_properties', id=custom_content_id)
        
        data = {
            "key": key,
            "value": value
        }
            
        try:
            return self.post(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to create property for custom content {custom_content_id}: {e}")
            raise
            
    def update_custom_content_property(self, 
                                     custom_content_id: str, 
                                     key: str, 
                                     value: Any, 
                                     version_number: int,
                                     version_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Updates a property for a custom content.
        
        Args:
            custom_content_id: ID of the custom content
            key: Key of the property to update
            value: New value of the property (must be JSON serializable)
            version_number: New version number (should be current version number + 1)
            version_message: (optional) Message for the new version
                
        Returns:
            The updated property
            
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_property_by_key', id=custom_content_id, key=key)
        
        data = {
            "key": key,
            "value": value,
            "version": {
                "number": version_number
            }
        }
        
        if version_message:
            data["version"]["message"] = version_message
            
        try:
            return self.put(endpoint, data=data)
        except Exception as e:
            log.error(f"Failed to update property {key} for custom content {custom_content_id}: {e}")
            raise
            
    def delete_custom_content_property(self, custom_content_id: str, key: str) -> None:
        """
        Deletes a property from a custom content.
        
        Args:
            custom_content_id: ID of the custom content
            key: Key of the property to delete
                
        Raises:
            HTTPError: If the API call fails
        """
        endpoint = self.get_endpoint('custom_content_property_by_key', id=custom_content_id, key=key)
        
        try:
            self.delete(endpoint)
        except Exception as e:
            log.error(f"Failed to delete property {key} from custom content {custom_content_id}: {e}")
            raise 