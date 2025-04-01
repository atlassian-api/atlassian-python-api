#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, Mock, ANY
from atlassian import ConfluenceV2

class TestConfluenceV2(unittest.TestCase):
    """
    Unit tests for ConfluenceV2 methods
    """
    
    def setUp(self):
        self.confluence_v2 = ConfluenceV2(
            url="https://example.atlassian.net",
            username="username",
            password="password"
        )
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_page_by_id(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.get_page_by_id("123")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={})
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_page_by_id_with_body_format(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method with body_format
        response = self.confluence_v2.get_page_by_id("123", body_format="storage")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={'body-format': 'storage'})
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_page_by_id_without_body(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method with get_body=False
        response = self.confluence_v2.get_page_by_id("123", get_body=False)
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={'body-format': 'none'})
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_page_by_id_with_expand(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method with expand
        response = self.confluence_v2.get_page_by_id("123", expand=["version", "history"])
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={'expand': 'version,history'})
        self.assertEqual(response, mock_response)
        
    def test_get_page_by_id_invalid_body_format(self):
        # Test invalid body_format
        with self.assertRaises(ValueError):
            self.confluence_v2.get_page_by_id("123", body_format="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_pages(self, mock_get_paged):
        # Setup the mock
        mock_pages = [{"id": "123", "title": "Test Page 1"}, {"id": "456", "title": "Test Page 2"}]
        mock_get_paged.return_value = mock_pages
        
        # Call the method
        response = self.confluence_v2.get_pages()
        
        # Assertions
        mock_get_paged.assert_called_once_with('api/v2/pages', params={
            'limit': 25, 
            'status': 'current', 
            'body-format': 'none'
        })
        self.assertEqual(response, mock_pages)
        
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_pages_with_filters(self, mock_get_paged):
        # Setup the mock
        mock_pages = [{"id": "123", "title": "Test Page"}]
        mock_get_paged.return_value = mock_pages
        
        # Call the method with filters
        response = self.confluence_v2.get_pages(
            space_id="SPACE123",
            title="Test",
            status="current",
            body_format="storage",
            expand=["version"],
            limit=10,
            sort="title"
        )
        
        # Assertions
        expected_params = {
            'limit': 10,
            'space-id': 'SPACE123',
            'title': 'Test',
            'status': 'current',
            'body-format': 'none',
            'expand': 'version',
            'sort': 'title'
        }
        mock_get_paged.assert_called_once_with('api/v2/pages', params=expected_params)
        self.assertEqual(response, mock_pages)
        
    def test_get_pages_invalid_status(self):
        # Test invalid status
        with self.assertRaises(ValueError):
            self.confluence_v2.get_pages(status="invalid")
            
    def test_get_pages_invalid_sort(self):
        # Test invalid sort
        with self.assertRaises(ValueError):
            self.confluence_v2.get_pages(sort="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_child_pages(self, mock_get_paged):
        # Setup the mock
        mock_pages = [{"id": "123", "title": "Child Page 1"}, {"id": "456", "title": "Child Page 2"}]
        mock_get_paged.return_value = mock_pages
        
        # Call the method
        response = self.confluence_v2.get_child_pages("PARENT123")
        
        # Assertions
        mock_get_paged.assert_called_once_with(
            'api/v2/pages/PARENT123/children/page', 
            params={
                'limit': 25, 
                'status': 'current',
                'body-format': 'none'
            }
        )
        self.assertEqual(response, mock_pages)
        
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_child_pages_with_filters(self, mock_get_paged):
        # Setup the mock
        mock_pages = [{"id": "123", "title": "Child Page"}]
        mock_get_paged.return_value = mock_pages
        
        # Call the method with filters
        response = self.confluence_v2.get_child_pages(
            parent_id="PARENT123",
            status="current",
            body_format="storage",
            get_body=True,
            expand=["version"],
            limit=10,
            sort="child-position"
        )
        
        # Assertions
        expected_params = {
            'limit': 10,
            'status': 'current',
            'body-format': 'storage',
            'expand': 'version',
            'sort': 'child-position'
        }
        mock_get_paged.assert_called_once_with('api/v2/pages/PARENT123/children/page', params=expected_params)
        self.assertEqual(response, mock_pages)
        
    def test_get_child_pages_invalid_status(self):
        # Test invalid status
        with self.assertRaises(ValueError):
            self.confluence_v2.get_child_pages("PARENT123", status="draft")  # draft is invalid for child pages
            
    def test_get_child_pages_invalid_sort(self):
        # Test invalid sort
        with self.assertRaises(ValueError):
            self.confluence_v2.get_child_pages("PARENT123", sort="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_page(self, mock_post):
        # Setup the mock
        mock_response = {"id": "123", "title": "New Page", "status": "current"}
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.create_page(
            space_id="SPACE123",
            title="New Page",
            body="<p>This is the content</p>",
            body_format="storage"
        )
        
        # Assertions
        expected_data = {
            "spaceId": "SPACE123",
            "status": "current",
            "title": "New Page",
            "body": {
                "storage": {
                    "value": "<p>This is the content</p>"
                }
            }
        }
        mock_post.assert_called_once_with('api/v2/pages', data=expected_data)
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_page_with_parent(self, mock_post):
        # Setup the mock
        mock_response = {"id": "123", "title": "New Child Page"}
        mock_post.return_value = mock_response
        
        # Call the method with parent_id
        response = self.confluence_v2.create_page(
            space_id="SPACE123",
            title="New Child Page",
            body="<p>This is a child page</p>",
            parent_id="PARENT123",
            body_format="storage"
        )
        
        # Assertions
        expected_data = {
            "spaceId": "SPACE123",
            "status": "current",
            "title": "New Child Page",
            "body": {
                "storage": {
                    "value": "<p>This is a child page</p>"
                }
            },
            "parentId": "PARENT123"
        }
        mock_post.assert_called_once_with('api/v2/pages', data=expected_data)
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_page_with_wiki_format(self, mock_post):
        # Setup the mock
        mock_response = {"id": "123", "title": "Wiki Page"}
        mock_post.return_value = mock_response
        
        # Call the method with wiki format
        response = self.confluence_v2.create_page(
            space_id="SPACE123",
            title="Wiki Page",
            body="h1. Wiki Heading",
            body_format="wiki",
            representation="wiki"
        )
        
        # Assertions
        expected_data = {
            "spaceId": "SPACE123",
            "status": "current",
            "title": "Wiki Page",
            "body": {
                "wiki": {
                    "value": "h1. Wiki Heading",
                    "representation": "wiki"
                }
            }
        }
        mock_post.assert_called_once_with('api/v2/pages', data=expected_data)
        self.assertEqual(response, mock_response)
        
    def test_create_page_invalid_body_format(self):
        # Test invalid body_format
        with self.assertRaises(ValueError):
            self.confluence_v2.create_page(
                space_id="SPACE123",
                title="Test Page",
                body="Test content",
                body_format="invalid"
            )
            
    def test_create_page_invalid_status(self):
        # Test invalid status
        with self.assertRaises(ValueError):
            self.confluence_v2.create_page(
                space_id="SPACE123",
                title="Test Page",
                body="Test content",
                status="invalid"
            )
            
    def test_create_page_wiki_without_representation(self):
        # Test wiki format without representation
        with self.assertRaises(ValueError):
            self.confluence_v2.create_page(
                space_id="SPACE123",
                title="Test Page",
                body="h1. Wiki Content",
                body_format="wiki",
                # Missing representation="wiki"
            )
            
    @patch('atlassian.confluence_v2.ConfluenceV2.get_page_by_id')
    @patch('atlassian.confluence_v2.ConfluenceV2.put')
    def test_update_page(self, mock_put, mock_get_page):
        # Setup the mocks
        mock_page = {"id": "123", "title": "Existing Page", "version": {"number": 1}}
        mock_get_page.return_value = mock_page
        
        mock_response = {"id": "123", "title": "Updated Page", "version": {"number": 2}}
        mock_put.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.update_page(
            page_id="123",
            title="Updated Page",
            body="<p>Updated content</p>"
        )
        
        # Assertions
        expected_data = {
            "id": "123",
            "title": "Updated Page",
            "version": {
                "number": 2,
                "message": "Updated via Python API"
            },
            "body": {
                "storage": {
                    "value": "<p>Updated content</p>"
                }
            }
        }
        mock_put.assert_called_once_with('api/v2/pages/123', data=expected_data)
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.put')
    def test_update_page_with_explicit_version(self, mock_put):
        # Setup the mock
        mock_response = {"id": "123", "title": "Updated Page", "version": {"number": 5}}
        mock_put.return_value = mock_response
        
        # Call the method with explicit version
        response = self.confluence_v2.update_page(
            page_id="123",
            title="Updated Page",
            version=4  # Explicitly set version
        )
        
        # Assertions
        expected_data = {
            "id": "123",
            "title": "Updated Page",
            "version": {
                "number": 5,
                "message": "Updated via Python API"
            }
        }
        mock_put.assert_called_once_with('api/v2/pages/123', data=expected_data)
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.put')
    def test_update_page_status(self, mock_put):
        # Setup the mock
        mock_response = {"id": "123", "status": "archived"}
        mock_put.return_value = mock_response
        
        # Call the method to update status
        response = self.confluence_v2.update_page(
            page_id="123",
            status="archived",
            version=1
        )
        
        # Assertions
        expected_data = {
            "id": "123",
            "status": "archived",
            "version": {
                "number": 2,
                "message": "Updated via Python API"
            }
        }
        mock_put.assert_called_once_with('api/v2/pages/123', data=expected_data)
        self.assertEqual(response, mock_response)
        
    def test_update_page_invalid_body_format(self):
        # Test invalid body_format
        with self.assertRaises(ValueError):
            self.confluence_v2.update_page(
                page_id="123",
                body="Test content",
                body_format="invalid"
            )
            
    def test_update_page_invalid_status(self):
        # Test invalid status
        with self.assertRaises(ValueError):
            self.confluence_v2.update_page(
                page_id="123",
                status="invalid"
            )
            
    @patch('atlassian.confluence_v2.ConfluenceV2.delete')
    def test_delete_page(self, mock_delete):
        # Setup the mock
        mock_delete.return_value = None
        
        # Call the method
        result = self.confluence_v2.delete_page("123")
        
        # Assertions
        mock_delete.assert_called_once_with('api/v2/pages/123')
        self.assertTrue(result)
    
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_search(self, mock_get):
        # Setup the mock
        mock_response = {
            "results": [
                {"content": {"id": "123", "title": "Test Page"}},
                {"content": {"id": "456", "title": "Another Test Page"}}
            ],
            "_links": {"next": None}
        }
        mock_get.return_value = mock_response
        
        # Call the method with just query
        response = self.confluence_v2.search("test query")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/search', params={
            "limit": 25,
            "query": "test query"
        })
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_search_with_cql(self, mock_get):
        # Setup the mock
        mock_response = {"results": [{"content": {"id": "123"}}]}
        mock_get.return_value = mock_response
        
        # Call the method with CQL
        response = self.confluence_v2.search(
            query="", 
            cql="type = 'page' AND space.id = '123'",
            limit=10,
            excerpt=False
        )
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/search', params={
            "limit": 10,
            "cql": "type = 'page' AND space.id = '123'",
            "excerpt": "false"
        })
        self.assertEqual(response, mock_response)
        
    def test_search_no_query_or_cql(self):
        # Test missing both query and cql
        with self.assertRaises(ValueError):
            self.confluence_v2.search(query="", cql=None)
            
    def test_search_invalid_body_format(self):
        # Test invalid body_format
        with self.assertRaises(ValueError):
            self.confluence_v2.search("test", body_format="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2.search')
    def test_search_content(self, mock_search):
        # Setup the mock
        mock_results = [{"content": {"id": "123"}}, {"content": {"id": "456"}}]
        mock_search.return_value = {"results": mock_results}
        
        # Call the method
        response = self.confluence_v2.search_content(
            query="test",
            type="page",
            space_id="SPACE123",
            status="current",
            limit=10
        )
        
        # Assertions
        mock_search.assert_called_once_with(
            query="",
            cql='text ~ "test" AND type = "page" AND space.id = "SPACE123" AND status = "current"',
            limit=10
        )
        self.assertEqual(response, mock_results)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.search')
    def test_search_content_minimal(self, mock_search):
        # Setup the mock
        mock_results = [{"content": {"id": "123"}}]
        mock_search.return_value = {"results": mock_results}
        
        # Call the method with minimal parameters
        response = self.confluence_v2.search_content("test")
        
        # Assertions
        mock_search.assert_called_once_with(
            query="",
            cql='text ~ "test" AND status = "current"',
            limit=25
        )
        self.assertEqual(response, mock_results)
        
    def test_search_content_invalid_type(self):
        # Test invalid content type
        with self.assertRaises(ValueError):
            self.confluence_v2.search_content("test", type="invalid")
            
    def test_search_content_invalid_status(self):
        # Test invalid status
        with self.assertRaises(ValueError):
            self.confluence_v2.search_content("test", status="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_spaces(self, mock_get_paged):
        # Setup the mock
        mock_spaces = [
            {"id": "123", "key": "TEST", "name": "Test Space"},
            {"id": "456", "key": "DEV", "name": "Development Space"}
        ]
        mock_get_paged.return_value = mock_spaces
        
        # Call the method
        response = self.confluence_v2.get_spaces()
        
        # Assertions
        mock_get_paged.assert_called_once_with('api/v2/spaces', params={'limit': 25})
        self.assertEqual(response, mock_spaces)
        
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_spaces_with_filters(self, mock_get_paged):
        # Setup the mock
        mock_spaces = [{"id": "123", "key": "TEST", "name": "Test Space"}]
        mock_get_paged.return_value = mock_spaces
        
        # Call the method with filters
        response = self.confluence_v2.get_spaces(
            ids=["123", "456"],
            keys=["TEST", "DEV"],
            type="global",
            status="current",
            labels=["important", "documentation"],
            sort="name",
            limit=10
        )
        
        # Assertions
        expected_params = {
            'limit': 10,
            'id': '123,456',
            'key': 'TEST,DEV',
            'type': 'global',
            'status': 'current',
            'label': 'important,documentation',
            'sort': 'name'
        }
        mock_get_paged.assert_called_once_with('api/v2/spaces', params=expected_params)
        self.assertEqual(response, mock_spaces)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_space(self, mock_get):
        # Setup the mock
        mock_space = {"id": "123", "key": "TEST", "name": "Test Space"}
        mock_get.return_value = mock_space
        
        # Call the method
        response = self.confluence_v2.get_space("123")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/spaces/123')
        self.assertEqual(response, mock_space)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get_spaces')
    def test_get_space_by_key(self, mock_get_spaces):
        # Setup the mock
        mock_spaces = [{"id": "123", "key": "TEST", "name": "Test Space"}]
        mock_get_spaces.return_value = mock_spaces
        
        # Call the method
        response = self.confluence_v2.get_space_by_key("TEST")
        
        # Assertions
        mock_get_spaces.assert_called_once_with(keys=["TEST"], limit=1)
        self.assertEqual(response, mock_spaces[0])
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get_spaces')
    def test_get_space_by_key_not_found(self, mock_get_spaces):
        # Setup the mock to return empty list (no spaces found)
        mock_get_spaces.return_value = []
        
        # Test the method raises ValueError for non-existent key
        with self.assertRaises(ValueError):
            self.confluence_v2.get_space_by_key("NONEXISTENT")
            
    def test_get_spaces_invalid_type(self):
        # Test invalid space type
        with self.assertRaises(ValueError):
            self.confluence_v2.get_spaces(type="invalid")
            
    def test_get_spaces_invalid_status(self):
        # Test invalid space status
        with self.assertRaises(ValueError):
            self.confluence_v2.get_spaces(status="invalid")
            
    def test_get_spaces_invalid_sort(self):
        # Test invalid sort parameter
        with self.assertRaises(ValueError):
            self.confluence_v2.get_spaces(sort="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2.search')
    def test_get_space_content(self, mock_search):
        # Setup the mock
        mock_results = [{"content": {"id": "123", "title": "Page 1"}}]
        mock_search.return_value = {"results": mock_results}
        
        # Call the method
        response = self.confluence_v2.get_space_content("SPACE123")
        
        # Assertions
        mock_search.assert_called_once_with(query="", cql='space.id = "SPACE123"', limit=25)
        self.assertEqual(response, mock_results)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.search')
    def test_get_space_content_with_filters(self, mock_search):
        # Setup the mock
        mock_results = [{"content": {"id": "123", "title": "Root Page"}}]
        mock_search.return_value = {"results": mock_results}
        
        # Call the method with filters
        response = self.confluence_v2.get_space_content(
            space_id="SPACE123",
            depth="root",
            sort="created",
            limit=10
        )
        
        # Assertions
        mock_search.assert_called_once_with(
            query="", 
            cql='space.id = "SPACE123" AND ancestor = root order by created asc', 
            limit=10
        )
        self.assertEqual(response, mock_results)
        
    def test_get_space_content_invalid_sort(self):
        # Test invalid sort parameter
        with self.assertRaises(ValueError):
            self.confluence_v2.get_space_content("SPACE123", sort="invalid")
            
    # Tests for Page Property Methods (Phase 3)
    
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_page_properties(self, mock_get_paged):
        # Setup the mock
        mock_properties = [
            {"id": "123", "key": "prop1", "value": {"num": 42}},
            {"id": "456", "key": "prop2", "value": "test value"}
        ]
        mock_get_paged.return_value = mock_properties
        
        # Call the method
        response = self.confluence_v2.get_page_properties("PAGE123")
        
        # Assertions
        mock_get_paged.assert_called_once_with('api/v2/pages/PAGE123/properties', params={'limit': 25})
        self.assertEqual(response, mock_properties)
        
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_page_properties_with_cursor(self, mock_get_paged):
        # Setup the mock
        mock_properties = [{"id": "123", "key": "prop1", "value": {"num": 42}}]
        mock_get_paged.return_value = mock_properties
        
        # Call the method with cursor
        response = self.confluence_v2.get_page_properties(
            page_id="PAGE123",
            cursor="next-page-cursor",
            limit=10
        )
        
        # Assertions
        mock_get_paged.assert_called_once_with('api/v2/pages/PAGE123/properties', params={
            'limit': 10,
            'cursor': 'next-page-cursor'
        })
        self.assertEqual(response, mock_properties)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_page_property_by_key(self, mock_get):
        # Setup the mock
        mock_property = {"id": "123", "key": "prop1", "value": {"num": 42}}
        mock_get.return_value = mock_property
        
        # Call the method
        response = self.confluence_v2.get_page_property_by_key("PAGE123", "prop1")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/PAGE123/properties/prop1')
        self.assertEqual(response, mock_property)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_page_property(self, mock_post):
        # Setup the mock
        mock_response = {"id": "123", "key": "test.prop", "value": {"data": "test"}}
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.create_page_property(
            page_id="PAGE123",
            property_key="test.prop",
            property_value={"data": "test"}
        )
        
        # Assertions
        expected_data = {
            "key": "test.prop",
            "value": {"data": "test"}
        }
        mock_post.assert_called_once_with('api/v2/pages/PAGE123/properties', data=expected_data)
        self.assertEqual(response, mock_response)
        
    def test_create_page_property_invalid_key(self):
        # Test with invalid property key (containing invalid characters)
        with self.assertRaises(ValueError):
            self.confluence_v2.create_page_property(
                page_id="PAGE123",
                property_key="invalid-key!",
                property_value="test"
            )
            
    @patch('atlassian.confluence_v2.ConfluenceV2.get_page_property_by_key')
    @patch('atlassian.confluence_v2.ConfluenceV2.put')
    def test_update_page_property(self, mock_put, mock_get_property):
        # Setup the mocks
        mock_current = {"id": "123", "key": "prop1", "version": {"number": 1}}
        mock_get_property.return_value = mock_current
        
        mock_response = {"id": "123", "key": "prop1", "value": "updated", "version": {"number": 2}}
        mock_put.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.update_page_property(
            page_id="PAGE123",
            property_key="prop1",
            property_value="updated"
        )
        
        # Assertions
        expected_data = {
            "key": "prop1",
            "value": "updated",
            "version": {
                "number": 2,
                "message": "Updated via Python API"
            }
        }
        mock_put.assert_called_once_with('api/v2/pages/PAGE123/properties/prop1', data=expected_data)
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.put')
    def test_update_page_property_with_explicit_version(self, mock_put):
        # Setup the mock
        mock_response = {"id": "123", "key": "prop1", "value": "updated", "version": {"number": 5}}
        mock_put.return_value = mock_response
        
        # Call the method with explicit version
        response = self.confluence_v2.update_page_property(
            page_id="PAGE123",
            property_key="prop1",
            property_value="updated",
            version=4  # Explicitly set version
        )
        
        # Assertions
        expected_data = {
            "key": "prop1",
            "value": "updated",
            "version": {
                "number": 5,
                "message": "Updated via Python API"
            }
        }
        mock_put.assert_called_once_with('api/v2/pages/PAGE123/properties/prop1', data=expected_data)
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.delete')
    def test_delete_page_property(self, mock_delete):
        # Setup the mock
        mock_delete.return_value = None
        
        # Call the method
        result = self.confluence_v2.delete_page_property("PAGE123", "prop1")
        
        # Assertions
        mock_delete.assert_called_once_with('api/v2/pages/PAGE123/properties/prop1')
        self.assertTrue(result)
    
    # Tests for Label Methods (Phase 3)
    
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_page_labels(self, mock_get_paged):
        # Setup the mock
        mock_labels = [
            {"id": "123", "name": "label1"},
            {"id": "456", "name": "label2"}
        ]
        mock_get_paged.return_value = mock_labels
        
        # Call the method
        response = self.confluence_v2.get_page_labels("PAGE123")
        
        # Assertions
        mock_get_paged.assert_called_once_with('api/v2/pages/PAGE123/labels', params={'limit': 25})
        self.assertEqual(response, mock_labels)
        
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_page_labels_with_filters(self, mock_get_paged):
        # Setup the mock
        mock_labels = [{"id": "123", "name": "team-label"}]
        mock_get_paged.return_value = mock_labels
        
        # Call the method with filters
        response = self.confluence_v2.get_page_labels(
            page_id="PAGE123",
            prefix="team-",
            cursor="next-page-cursor",
            limit=10
        )
        
        # Assertions
        mock_get_paged.assert_called_once_with('api/v2/pages/PAGE123/labels', params={
            'limit': 10,
            'prefix': 'team-',
            'cursor': 'next-page-cursor'
        })
        self.assertEqual(response, mock_labels)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_add_page_label(self, mock_post):
        # Setup the mock
        mock_response = {"id": "123", "name": "test-label"}
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.add_page_label("PAGE123", "test-label")
        
        # Assertions
        expected_data = {"name": "test-label"}
        mock_post.assert_called_once_with('api/v2/pages/PAGE123/labels', data=expected_data)
        self.assertEqual(response, mock_response)
        
    def test_add_page_label_empty(self):
        # Test with empty label
        with self.assertRaises(ValueError):
            self.confluence_v2.add_page_label("PAGE123", "")
            
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_add_page_labels(self, mock_post):
        # Setup the mock
        mock_response = [
            {"id": "123", "name": "label1"},
            {"id": "456", "name": "label2"}
        ]
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.add_page_labels("PAGE123", ["label1", "label2"])
        
        # Assertions
        expected_data = [{"name": "label1"}, {"name": "label2"}]
        mock_post.assert_called_once_with('api/v2/pages/PAGE123/labels', data=expected_data)
        self.assertEqual(response, mock_response)
        
    def test_add_page_labels_empty(self):
        # Test with empty labels list
        with self.assertRaises(ValueError):
            self.confluence_v2.add_page_labels("PAGE123", [])
            
    @patch('atlassian.confluence_v2.ConfluenceV2.delete')
    def test_delete_page_label(self, mock_delete):
        # Setup the mock
        mock_delete.return_value = None
        
        # Call the method
        result = self.confluence_v2.delete_page_label("PAGE123", "test-label")
        
        # Assertions
        mock_delete.assert_called_once_with('api/v2/pages/PAGE123/labels', params={"name": "test-label"})
        self.assertTrue(result)
        
    def test_delete_page_label_empty(self):
        # Test with empty label
        with self.assertRaises(ValueError):
            self.confluence_v2.delete_page_label("PAGE123", "")
            
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_space_labels(self, mock_get_paged):
        # Setup the mock
        mock_labels = [
            {"id": "123", "name": "label1"},
            {"id": "456", "name": "label2"}
        ]
        mock_get_paged.return_value = mock_labels
        
        # Call the method
        response = self.confluence_v2.get_space_labels("SPACE123")
        
        # Assertions
        mock_get_paged.assert_called_once_with('api/v2/spaces/SPACE123/labels', params={'limit': 25})
        self.assertEqual(response, mock_labels)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_add_space_label(self, mock_post):
        # Setup the mock
        mock_response = {"id": "123", "name": "test-label"}
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.add_space_label("SPACE123", "test-label")
        
        # Assertions
        expected_data = {"name": "test-label"}
        mock_post.assert_called_once_with('api/v2/spaces/SPACE123/labels', data=expected_data)
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_add_space_labels(self, mock_post):
        # Setup the mock
        mock_response = [
            {"id": "123", "name": "label1"},
            {"id": "456", "name": "label2"}
        ]
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.add_space_labels("SPACE123", ["label1", "label2"])
        
        # Assertions
        expected_data = [{"name": "label1"}, {"name": "label2"}]
        mock_post.assert_called_once_with('api/v2/spaces/SPACE123/labels', data=expected_data)
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.delete')
    def test_delete_space_label(self, mock_delete):
        # Setup the mock
        mock_delete.return_value = None
        
        # Call the method
        result = self.confluence_v2.delete_space_label("SPACE123", "test-label")
        
        # Assertions
        mock_delete.assert_called_once_with('api/v2/spaces/SPACE123/labels', params={"name": "test-label"})
        self.assertTrue(result)
            
    def test_delete_space_label(self):
        """Test deleting a label from a space"""
        space_id = "12345"
        label = "test-label"
        
        self.confluence_v2.delete(f"api/v2/spaces/{space_id}/labels/{label}")
        self.mock_response.json.return_value = {}
        
        result = self.confluence_v2.delete_space_label(space_id, label)
        self.assertTrue(result)
        
    # Comment methods tests
    
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_page_footer_comments(self, mock_get_paged):
        """Test retrieving footer comments for a page"""
        page_id = "12345"
        
        comments = [
            {"id": "1", "body": {"storage": {"value": "Test comment 1"}}},
            {"id": "2", "body": {"storage": {"value": "Test comment 2"}}}
        ]
        
        mock_get_paged.return_value = comments
        
        mock_return = self.confluence_v2.get_page_footer_comments(page_id)
        mock_get_paged.assert_called_with("api/v2/pages/12345/footer-comments", params={"limit": 25})
        self.assertEqual(mock_return, comments)
                                                  
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_page_footer_comments_with_parameters(self, mock_get_paged):
        """Test retrieving footer comments for a page with parameters"""
        page_id = "12345"
        
        comments = [
            {"id": "1", "body": {"storage": {"value": "Test comment 1"}}},
            {"id": "2", "body": {"storage": {"value": "Test comment 2"}}}
        ]
        
        mock_get_paged.return_value = comments
        
        mock_return = self.confluence_v2.get_page_footer_comments(
            page_id, 
            body_format="storage", 
            cursor="some-cursor", 
            limit=10, 
            sort="created-date"
        )
        mock_get_paged.assert_called_with("api/v2/pages/12345/footer-comments", 
                                   params={
                                       "limit": 10,
                                       "body-format": "storage",
                                       "cursor": "some-cursor",
                                       "sort": "created-date"
                                   })
        self.assertEqual(mock_return, comments)
                                                
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_page_inline_comments(self, mock_get_paged):
        """Test retrieving inline comments for a page"""
        page_id = "12345"
        
        comments = [
            {"id": "1", "body": {"storage": {"value": "Test comment 1"}}},
            {"id": "2", "body": {"storage": {"value": "Test comment 2"}}}
        ]
        
        mock_get_paged.return_value = comments
        
        mock_return = self.confluence_v2.get_page_inline_comments(page_id)
        mock_get_paged.assert_called_with("api/v2/pages/12345/inline-comments", params={"limit": 25})
        self.assertEqual(mock_return, comments)
                                                
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_blogpost_footer_comments(self, mock_get_paged):
        """Test retrieving footer comments for a blog post"""
        blogpost_id = "12345"
        
        comments = [
            {"id": "1", "body": {"storage": {"value": "Test comment 1"}}},
            {"id": "2", "body": {"storage": {"value": "Test comment 2"}}}
        ]
        
        mock_get_paged.return_value = comments
        
        mock_return = self.confluence_v2.get_blogpost_footer_comments(blogpost_id)
        mock_get_paged.assert_called_with("api/v2/blogposts/12345/footer-comments", params={"limit": 25})
        self.assertEqual(mock_return, comments)
                                                
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_blogpost_inline_comments(self, mock_get_paged):
        """Test retrieving inline comments for a blog post"""
        blogpost_id = "12345"
        
        comments = [
            {"id": "1", "body": {"storage": {"value": "Test comment 1"}}},
            {"id": "2", "body": {"storage": {"value": "Test comment 2"}}}
        ]
        
        mock_get_paged.return_value = comments
        
        mock_return = self.confluence_v2.get_blogpost_inline_comments(blogpost_id)
        mock_get_paged.assert_called_with("api/v2/blogposts/12345/inline-comments", params={"limit": 25})
        self.assertEqual(mock_return, comments)
                                                
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_attachment_comments(self, mock_get_paged):
        """Test retrieving comments for an attachment"""
        attachment_id = "12345"
        
        comments = [
            {"id": "1", "body": {"storage": {"value": "Test comment 1"}}},
            {"id": "2", "body": {"storage": {"value": "Test comment 2"}}}
        ]
        
        mock_get_paged.return_value = comments
        
        mock_return = self.confluence_v2.get_attachment_comments(attachment_id)
        mock_get_paged.assert_called_with("api/v2/attachments/12345/footer-comments", params={"limit": 25})
        self.assertEqual(mock_return, comments)
                                                
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_custom_content_comments(self, mock_get_paged):
        """Test retrieving comments for custom content"""
        custom_content_id = "12345"
        
        comments = [
            {"id": "1", "body": {"storage": {"value": "Test comment 1"}}},
            {"id": "2", "body": {"storage": {"value": "Test comment 2"}}}
        ]
        
        mock_get_paged.return_value = comments
        
        mock_return = self.confluence_v2.get_custom_content_comments(custom_content_id)
        mock_get_paged.assert_called_with("api/v2/custom-content/12345/footer-comments", params={"limit": 25})
        self.assertEqual(mock_return, comments)
                                                
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_comment_children(self, mock_get_paged):
        """Test retrieving child comments for a comment"""
        comment_id = "12345"
        
        comments = [
            {"id": "1", "body": {"storage": {"value": "Test comment 1"}}},
            {"id": "2", "body": {"storage": {"value": "Test comment 2"}}}
        ]
        
        mock_get_paged.return_value = comments
        
        mock_return = self.confluence_v2.get_comment_children(comment_id)
        mock_get_paged.assert_called_with("api/v2/comments/12345/children", params={"limit": 25})
        self.assertEqual(mock_return, comments)
                                                
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_comment_by_id(self, mock_get):
        """Test retrieving a comment by ID"""
        comment_id = "12345"
        
        comment = {"id": "12345", "body": {"storage": {"value": "Test comment"}}}
        
        mock_get.return_value = comment
        
        result = self.confluence_v2.get_comment_by_id(comment_id)
        mock_get.assert_called_with("api/v2/comments/12345", params={})
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_comment_by_id_with_parameters(self, mock_get):
        """Test retrieving a comment by ID with parameters"""
        comment_id = "12345"
        
        comment = {"id": "12345", "body": {"storage": {"value": "Test comment"}}}
        
        mock_get.return_value = comment
        
        result = self.confluence_v2.get_comment_by_id(comment_id, body_format="storage", version=1)
        mock_get.assert_called_with("api/v2/comments/12345", params={"body-format": "storage", "version": 1})
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_page_footer_comment(self, mock_post):
        """Test creating a footer comment on a page"""
        page_id = "12345"
        body = "Test comment body"
        
        expected_data = {
            "pageId": page_id,
            "body": {
                "storage": {
                    "value": "Test comment body",
                    "representation": "storage"
                }
            }
        }
        
        comment = {"id": "comment-123", "body": {"storage": {"value": "Test comment body"}}}
        
        mock_post.return_value = comment
        
        result = self.confluence_v2.create_page_footer_comment(page_id, body)
        mock_post.assert_called_with("api/v2/comments", data=expected_data)
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_page_inline_comment(self, mock_post):
        """Test creating an inline comment on a page"""
        page_id = "12345"
        body = "Test comment body"
        inline_comment_properties = {
            "textSelection": "text to highlight",
            "textSelectionMatchCount": 3,
            "textSelectionMatchIndex": 1
        }
        
        expected_data = {
            "pageId": page_id,
            "body": {
                "storage": {
                    "value": "Test comment body",
                    "representation": "storage"
                }
            },
            "inlineCommentProperties": inline_comment_properties
        }
        
        comment = {"id": "comment-123", "body": {"storage": {"value": "Test comment body"}}}
        
        mock_post.return_value = comment
        
        result = self.confluence_v2.create_page_inline_comment(page_id, body, inline_comment_properties)
        mock_post.assert_called_with("api/v2/comments", data=expected_data)
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_blogpost_footer_comment(self, mock_post):
        """Test creating a footer comment on a blog post"""
        blogpost_id = "12345"
        body = "Test comment body"
        
        expected_data = {
            "blogPostId": blogpost_id,
            "body": {
                "storage": {
                    "value": "Test comment body",
                    "representation": "storage"
                }
            }
        }
        
        comment = {"id": "comment-123", "body": {"storage": {"value": "Test comment body"}}}
        
        mock_post.return_value = comment
        
        result = self.confluence_v2.create_blogpost_footer_comment(blogpost_id, body)
        mock_post.assert_called_with("api/v2/comments", data=expected_data)
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_custom_content_comment(self, mock_post):
        """Test creating a comment on custom content"""
        custom_content_id = "12345"
        body = "Test comment body"
        
        expected_data = {
            "customContentId": custom_content_id,
            "body": {
                "storage": {
                    "value": "Test comment body",
                    "representation": "storage"
                }
            }
        }
        
        comment = {"id": "comment-123", "body": {"storage": {"value": "Test comment body"}}}
        
        mock_post.return_value = comment
        
        result = self.confluence_v2.create_custom_content_comment(custom_content_id, body)
        mock_post.assert_called_with("api/v2/comments", data=expected_data)
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_attachment_comment(self, mock_post):
        """Test creating a comment on an attachment"""
        attachment_id = "12345"
        body = "Test comment body"
        
        expected_data = {
            "attachmentId": attachment_id,
            "body": {
                "storage": {
                    "value": "Test comment body",
                    "representation": "storage"
                }
            }
        }
        
        comment = {"id": "comment-123", "body": {"storage": {"value": "Test comment body"}}}
        
        mock_post.return_value = comment
        
        result = self.confluence_v2.create_attachment_comment(attachment_id, body)
        mock_post.assert_called_with("api/v2/comments", data=expected_data)
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_comment_reply(self, mock_post):
        """Test creating a reply to a comment"""
        comment_id = "12345"
        body = "Test reply body"
        
        expected_data = {
            "parentCommentId": comment_id,
            "body": {
                "storage": {
                    "value": "Test reply body",
                    "representation": "storage"
                }
            }
        }
        
        comment = {"id": "reply-123", "body": {"storage": {"value": "Test reply body"}}}
        
        mock_post.return_value = comment
        
        result = self.confluence_v2.create_comment_reply(comment_id, body)
        mock_post.assert_called_with("api/v2/comments", data=expected_data)
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.put')
    def test_update_comment(self, mock_put):
        """Test updating a comment"""
        comment_id = "12345"
        body = "Updated comment body"
        version = 1
        
        expected_data = {
            "version": {
                "number": 2
            },
            "body": {
                "storage": {
                    "representation": "storage",
                    "value": "Updated comment body"
                }
            }
        }
        
        comment = {"id": "12345", "body": {"storage": {"value": "Updated comment body"}}}
        
        mock_put.return_value = comment
        
        result = self.confluence_v2.update_comment(comment_id, body, version)
        mock_put.assert_called_with("api/v2/comments/12345", data=expected_data)
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.put')
    def test_update_comment_with_resolved(self, mock_put):
        """Test updating a comment with resolved status"""
        comment_id = "12345"
        body = "Updated comment body"
        version = 1
        resolved = True
        
        expected_data = {
            "version": {
                "number": 2
            },
            "body": {
                "storage": {
                    "representation": "storage",
                    "value": "Updated comment body"
                }
            },
            "resolved": True
        }
        
        comment = {"id": "12345", "body": {"storage": {"value": "Updated comment body"}}, "resolved": True}
        
        mock_put.return_value = comment
        
        result = self.confluence_v2.update_comment(comment_id, body, version, resolved=resolved)
        mock_put.assert_called_with("api/v2/comments/12345", data=expected_data)
        self.assertEqual(result, comment)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.delete')
    def test_delete_comment(self, mock_delete):
        """Test deleting a comment"""
        comment_id = "12345"
        
        mock_delete.return_value = None
        
        result = self.confluence_v2.delete_comment(comment_id)
        mock_delete.assert_called_with("api/v2/comments/12345")
        self.assertTrue(result)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.delete')
    def test_delete_space_label(self, mock_delete):
        """Test deleting a space label"""
        space_id = "12345"
        label = "test-label"
        
        mock_delete.return_value = None
        
        result = self.confluence_v2.delete_space_label(space_id, label)
        mock_delete.assert_called_with("api/v2/spaces/12345/labels/test-label")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main() 