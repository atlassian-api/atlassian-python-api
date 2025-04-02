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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_page_by_id(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method
        response = self.confluence_v2.get_page_by_id("123")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={})
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_page_by_id_with_body_format(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method with body_format
        response = self.confluence_v2.get_page_by_id("123", body_format="storage")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={'body-format': 'storage'})
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_page_by_id_without_body(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method with get_body=False
        response = self.confluence_v2.get_page_by_id("123", get_body=False)
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={'body-format': 'none'})
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
            'body-format': 'storage',
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get_page_by_id')
    @patch('atlassian.confluence.cloud.ConfluenceCloud.put')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.put')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.put')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud.delete')
    def test_delete_page(self, mock_delete):
        # Setup the mock
        mock_delete.return_value = None
        
        # Call the method
        result = self.confluence_v2.delete_page("123")
        
        # Assertions
        mock_delete.assert_called_once_with('api/v2/pages/123')
        self.assertTrue(result)
    
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud.search')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.search')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_space(self, mock_get):
        # Setup the mock
        mock_space = {"id": "123", "key": "TEST", "name": "Test Space"}
        mock_get.return_value = mock_space
        
        # Call the method
        response = self.confluence_v2.get_space("123")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/spaces/123')
        self.assertEqual(response, mock_space)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get_spaces')
    def test_get_space_by_key(self, mock_get_spaces):
        # Setup the mock
        mock_spaces = [{"id": "123", "key": "TEST", "name": "Test Space"}]
        mock_get_spaces.return_value = mock_spaces
        
        # Call the method
        response = self.confluence_v2.get_space_by_key("TEST")
        
        # Assertions
        mock_get_spaces.assert_called_once_with(keys=["TEST"], limit=1)
        self.assertEqual(response, mock_spaces[0])
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get_spaces')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud.search')
    def test_get_space_content(self, mock_search):
        # Setup the mock
        mock_results = [{"content": {"id": "123", "title": "Page 1"}}]
        mock_search.return_value = {"results": mock_results}
        
        # Call the method
        response = self.confluence_v2.get_space_content("SPACE123")
        
        # Assertions
        mock_search.assert_called_once_with(query="", cql='space.id = "SPACE123"', limit=25)
        self.assertEqual(response, mock_results)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.search')
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
    
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_page_property_by_key(self, mock_get):
        # Setup the mock
        mock_property = {"id": "123", "key": "prop1", "value": {"num": 42}}
        mock_get.return_value = mock_property
        
        # Call the method
        response = self.confluence_v2.get_page_property_by_key("PAGE123", "prop1")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/PAGE123/properties/prop1')
        self.assertEqual(response, mock_property)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get_page_property_by_key')
    @patch('atlassian.confluence.cloud.ConfluenceCloud.put')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.put')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.delete')
    def test_delete_page_property(self, mock_delete):
        # Setup the mock
        mock_delete.return_value = None
        
        # Call the method
        result = self.confluence_v2.delete_page_property("PAGE123", "prop1")
        
        # Assertions
        mock_delete.assert_called_once_with('api/v2/pages/PAGE123/properties/prop1')
        self.assertTrue(result)
    
    # Tests for Label Methods (Phase 3)
    
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud.delete')
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
            
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
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
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.delete')
    def test_delete_space_label(self, mock_delete):
        """Test deleting a space label"""
        space_id = "12345"
        label = "test-label"
        
        mock_delete.return_value = None
        
        result = self.confluence_v2.delete_space_label(space_id, label)
        mock_delete.assert_called_with("api/v2/spaces/12345/labels/test-label")
        self.assertTrue(result)
    
    # Tests for Whiteboard methods
    
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
    def test_create_whiteboard(self, mock_post):
        """Test creating a whiteboard"""
        space_id = "123456"
        title = "Test Whiteboard"
        template_key = "timeline"
        locale = "en-US"
        parent_id = "789012"
        
        expected_data = {
            "spaceId": space_id,
            "title": title,
            "templateKey": template_key,
            "locale": locale,
            "parentId": parent_id
        }
        
        mock_post.return_value = {"id": "987654", "title": title}
        
        result = self.confluence_v2.create_whiteboard(
            space_id=space_id, 
            title=title, 
            parent_id=parent_id,
            template_key=template_key,
            locale=locale
        )
        
        mock_post.assert_called_with(
            "api/v2/whiteboards",
            data=expected_data
        )
        
        self.assertEqual(result["id"], "987654")
        self.assertEqual(result["title"], title)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_whiteboard_by_id(self, mock_get):
        """Test retrieving a whiteboard by ID"""
        whiteboard_id = "123456"
        mock_response = {"id": whiteboard_id, "title": "Test Whiteboard"}
        mock_get.return_value = mock_response
        
        result = self.confluence_v2.get_whiteboard_by_id(whiteboard_id)
        
        mock_get.assert_called_with(
            "api/v2/whiteboards/123456"
        )
        
        self.assertEqual(result, mock_response)
    
    @patch('atlassian.confluence.cloud.ConfluenceCloud.delete')
    def test_delete_whiteboard(self, mock_delete):
        """Test deleting a whiteboard"""
        whiteboard_id = "123456"
        mock_delete.return_value = {"status": "success"}
        
        result = self.confluence_v2.delete_whiteboard(whiteboard_id)
        
        mock_delete.assert_called_with(
            "api/v2/whiteboards/123456"
        )
        
        self.assertEqual(result["status"], "success")
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
    def test_get_whiteboard_children(self, mock_get_paged):
        """Test retrieving whiteboard children"""
        whiteboard_id = "123456"
        cursor = "next-page"
        limit = 25
        
        mock_get_paged.return_value = [
            {"id": "child1", "title": "Child 1"},
            {"id": "child2", "title": "Child 2"}
        ]
        
        result = self.confluence_v2.get_whiteboard_children(
            whiteboard_id=whiteboard_id,
            cursor=cursor,
            limit=limit
        )
        
        mock_get_paged.assert_called_with(
            "api/v2/whiteboards/123456/children",
            params={"cursor": cursor, "limit": limit}
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "child1")
        self.assertEqual(result[1]["id"], "child2")
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_whiteboard_ancestors(self, mock_get):
        """Test retrieving whiteboard ancestors"""
        whiteboard_id = "123456"
        mock_response = {
            "results": [
                {"id": "parent1", "type": "whiteboard"},
                {"id": "parent2", "type": "space"}
            ]
        }
        mock_get.return_value = mock_response
        
        result = self.confluence_v2.get_whiteboard_ancestors(whiteboard_id)
        
        mock_get.assert_called_with(
            "api/v2/whiteboards/123456/ancestors"
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "parent1")
        self.assertEqual(result[1]["id"], "parent2")
    
    # Tests for Custom Content methods
    
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
    def test_create_custom_content(self, mock_post):
        """Test creating custom content"""
        space_id = "123456"
        content_type = "my.custom.type"
        title = "Test Custom Content"
        body = "<p>Test body</p>"
        page_id = "789012"
        
        expected_data = {
            "type": content_type,
            "title": title,
            "body": {
                "storage": {
                    "representation": "storage",
                    "value": body
                }
            },
            "status": "current",
            "spaceId": space_id,
            "pageId": page_id
        }
        
        mock_post.return_value = {"id": "987654", "title": title}
        
        result = self.confluence_v2.create_custom_content(
            type=content_type,
            title=title,
            body=body,
            space_id=space_id,
            page_id=page_id
        )
        
        mock_post.assert_called_with(
            "api/v2/custom-content",
            data=expected_data
        )
        
        self.assertEqual(result["id"], "987654")
        self.assertEqual(result["title"], title)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_custom_content_by_id(self, mock_get):
        """Test retrieving custom content by ID"""
        custom_content_id = "123456"
        body_format = "storage"
        mock_response = {"id": custom_content_id, "title": "Test Custom Content"}
        mock_get.return_value = mock_response
        
        result = self.confluence_v2.get_custom_content_by_id(
            custom_content_id=custom_content_id,
            body_format=body_format
        )
        
        mock_get.assert_called_with(
            "api/v2/custom-content/123456",
            params={"body-format": body_format}
        )
        
        self.assertEqual(result, mock_response)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
    def test_get_custom_content(self, mock_get_paged):
        """Test retrieving custom content with filters"""
        content_type = "my.custom.type"
        space_id = "123456"
        page_id = "789012"
        status = "current"
        sort = "-created-date"
        limit = 25
        
        expected_params = {
            "type": content_type,
            "space-id": space_id,
            "page-id": page_id,
            "status": status,
            "sort": sort,
            "limit": limit
        }
        
        mock_get_paged.return_value = [
            {"id": "content1", "title": "Content 1"},
            {"id": "content2", "title": "Content 2"}
        ]
        
        result = self.confluence_v2.get_custom_content(
            type=content_type,
            space_id=space_id,
            page_id=page_id,
            status=status,
            sort=sort,
            limit=limit
        )
        
        mock_get_paged.assert_called_with(
            "api/v2/custom-content",
            params=expected_params
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "content1")
        self.assertEqual(result[1]["id"], "content2")
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.put')
    def test_update_custom_content(self, mock_put):
        """Test updating custom content"""
        custom_content_id = "123456"
        content_type = "my.custom.type"
        title = "Updated Title"
        body = "<p>Updated body</p>"
        space_id = "789012"
        version_number = 2
        version_message = "Update via test"
        
        expected_data = {
            "id": custom_content_id,
            "type": content_type,
            "title": title,
            "body": {
                "storage": {
                    "representation": "storage",
                    "value": body
                }
            },
            "status": "current",
            "version": {
                "number": version_number,
                "message": version_message
            },
            "spaceId": space_id
        }
        
        mock_put.return_value = {
            "id": custom_content_id, 
            "title": title,
            "version": {"number": version_number}
        }
        
        result = self.confluence_v2.update_custom_content(
            custom_content_id=custom_content_id,
            type=content_type,
            title=title,
            body=body,
            status="current",
            version_number=version_number,
            space_id=space_id,
            version_message=version_message
        )
        
        mock_put.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}",
            data=expected_data
        )
        
        self.assertEqual(result["id"], custom_content_id)
        self.assertEqual(result["title"], title)
        self.assertEqual(result["version"]["number"], version_number)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.delete')
    def test_delete_custom_content(self, mock_delete):
        """Test deleting custom content"""
        custom_content_id = "123456"
        mock_delete.return_value = {"status": "success"}
        
        result = self.confluence_v2.delete_custom_content(custom_content_id)
        
        mock_delete.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}"
        )
        
        self.assertEqual(result["status"], "success")
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
    def test_get_custom_content_children(self, mock_get_paged):
        """Test retrieving custom content children"""
        custom_content_id = "123456"
        cursor = "next-page"
        limit = 25
        
        mock_get_paged.return_value = [
            {"id": "child1", "title": "Child 1"},
            {"id": "child2", "title": "Child 2"}
        ]
        
        result = self.confluence_v2.get_custom_content_children(
            custom_content_id=custom_content_id,
            cursor=cursor,
            limit=limit
        )
        
        mock_get_paged.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/children",
            params={"cursor": cursor, "limit": limit}
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "child1")
        self.assertEqual(result[1]["id"], "child2")
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_custom_content_ancestors(self, mock_get):
        """Test retrieving custom content ancestors"""
        custom_content_id = "123456"
        mock_response = {
            "results": [
                {"id": "parent1", "type": "page"},
                {"id": "parent2", "type": "space"}
            ]
        }
        mock_get.return_value = mock_response
        
        result = self.confluence_v2.get_custom_content_ancestors(custom_content_id)
        
        mock_get.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/ancestors"
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "parent1")
        self.assertEqual(result[1]["id"], "parent2")
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
    def test_get_custom_content_labels(self, mock_get_paged):
        """Test retrieving custom content labels"""
        custom_content_id = "123456"
        prefix = "global"
        sort = "name"
        
        mock_get_paged.return_value = [
            {"id": "label1", "name": "test", "prefix": "global"},
            {"id": "label2", "name": "documentation"}
        ]
        
        result = self.confluence_v2.get_custom_content_labels(
            custom_content_id=custom_content_id,
            prefix=prefix,
            sort=sort
        )
        
        mock_get_paged.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/labels",
            params={"prefix": prefix, "sort": sort}
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "test")
        self.assertEqual(result[1]["name"], "documentation")
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
    def test_add_custom_content_label(self, mock_post):
        """Test adding a label to custom content"""
        custom_content_id = "123456"
        label = "test-label"
        prefix = "global"
        
        expected_data = {
            "name": label,
            "prefix": prefix
        }
        
        mock_post.return_value = {"id": "label1", "name": label, "prefix": prefix}
        
        result = self.confluence_v2.add_custom_content_label(
            custom_content_id=custom_content_id,
            label=label,
            prefix=prefix
        )
        
        mock_post.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/labels",
            data=expected_data
        )
        
        self.assertEqual(result["name"], label)
        self.assertEqual(result["prefix"], prefix)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.delete')
    def test_delete_custom_content_label(self, mock_delete):
        """Test deleting a label from custom content"""
        custom_content_id = "123456"
        label = "test-label"
        prefix = "global"
        
        self.confluence_v2.delete_custom_content_label(
            custom_content_id=custom_content_id,
            label=label,
            prefix=prefix
        )
        
        mock_delete.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/labels",
            params={"name": label, "prefix": prefix}
        )
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud._get_paged')
    def test_get_custom_content_properties(self, mock_get_paged):
        """Test retrieving custom content properties"""
        custom_content_id = "123456"
        sort = "key"
        limit = 25
        
        mock_get_paged.return_value = [
            {"id": "prop1", "key": "test-prop", "value": {"test": "value"}},
            {"id": "prop2", "key": "another-prop", "value": 123}
        ]
        
        result = self.confluence_v2.get_custom_content_properties(
            custom_content_id=custom_content_id,
            sort=sort,
            limit=limit
        )
        
        mock_get_paged.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/properties",
            params={"sort": sort, "limit": limit}
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["key"], "test-prop")
        self.assertEqual(result[1]["key"], "another-prop")
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.get')
    def test_get_custom_content_property_by_key(self, mock_get):
        """Test retrieving a specific custom content property"""
        custom_content_id = "123456"
        property_key = "test-prop"
        
        mock_response = {
            "id": "prop1", 
            "key": property_key, 
            "value": {"test": "value"},
            "version": {"number": 1}
        }
        mock_get.return_value = mock_response
        
        result = self.confluence_v2.get_custom_content_property_by_key(
            custom_content_id=custom_content_id,
            property_key=property_key
        )
        
        mock_get.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/properties/{property_key}"
        )
        
        self.assertEqual(result, mock_response)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.post')
    def test_create_custom_content_property(self, mock_post):
        """Test creating a custom content property"""
        custom_content_id = "123456"
        property_key = "test-prop"
        property_value = {"test": "value"}
        
        expected_data = {
            "key": property_key,
            "value": property_value
        }
        
        mock_post.return_value = {
            "id": "prop1", 
            "key": property_key, 
            "value": property_value
        }
        
        result = self.confluence_v2.create_custom_content_property(
            custom_content_id=custom_content_id,
            key=property_key,
            value=property_value
        )
        
        mock_post.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/properties",
            data=expected_data
        )
        
        self.assertEqual(result["key"], property_key)
        self.assertEqual(result["value"], property_value)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.put')
    def test_update_custom_content_property(self, mock_put):
        """Test updating a custom content property"""
        custom_content_id = "123456"
        property_key = "test-prop"
        property_value = {"test": "updated"}
        version_number = 2
        version_message = "Update via test"
        
        expected_data = {
            "key": property_key,
            "value": property_value,
            "version": {
                "number": version_number,
                "message": version_message
            }
        }
        
        mock_put.return_value = {
            "id": "prop1", 
            "key": property_key, 
            "value": property_value,
            "version": {"number": version_number}
        }
        
        result = self.confluence_v2.update_custom_content_property(
            custom_content_id=custom_content_id,
            key=property_key,
            value=property_value,
            version_number=version_number,
            version_message=version_message
        )
        
        mock_put.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/properties/{property_key}",
            data=expected_data
        )
        
        self.assertEqual(result["key"], property_key)
        self.assertEqual(result["value"], property_value)
        self.assertEqual(result["version"]["number"], version_number)
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.delete')
    def test_delete_custom_content_property(self, mock_delete):
        """Test deleting a custom content property"""
        custom_content_id = "123456"
        property_key = "test-prop"
        
        self.confluence_v2.delete_custom_content_property(
            custom_content_id=custom_content_id,
            key=property_key
        )
        
        mock_delete.assert_called_with(
            f"api/v2/custom-content/{custom_content_id}/properties/{property_key}"
        )
        
    @patch('atlassian.confluence.cloud.ConfluenceCloud.delete')
    def test_delete_comment(self, mock_delete):
        """Test deleting a comment"""
        comment_id = "12345"
        
        mock_delete.return_value = None
        
        result = self.confluence_v2.delete_comment(comment_id)
        mock_delete.assert_called_with("api/v2/comments/12345")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main() 