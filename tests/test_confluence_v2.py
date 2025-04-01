#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, Mock
from atlassian import ConfluenceV2

class TestConfluenceV2(unittest.TestCase):
    """
    Unit tests for ConfluenceV2 methods
    """
    
    def setUp(self):
        self.confluence = ConfluenceV2(
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
        response = self.confluence.get_page_by_id("123")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={})
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_page_by_id_with_body_format(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method with body_format
        response = self.confluence.get_page_by_id("123", body_format="storage")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={'body-format': 'storage'})
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_page_by_id_without_body(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method with get_body=False
        response = self.confluence.get_page_by_id("123", get_body=False)
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={'body-format': 'none'})
        self.assertEqual(response, mock_response)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get')
    def test_get_page_by_id_with_expand(self, mock_get):
        # Setup the mock
        mock_response = {"id": "123", "title": "Test Page"}
        mock_get.return_value = mock_response
        
        # Call the method with expand
        response = self.confluence.get_page_by_id("123", expand=["version", "history"])
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/pages/123', params={'expand': 'version,history'})
        self.assertEqual(response, mock_response)
        
    def test_get_page_by_id_invalid_body_format(self):
        # Test invalid body_format
        with self.assertRaises(ValueError):
            self.confluence.get_page_by_id("123", body_format="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_pages(self, mock_get_paged):
        # Setup the mock
        mock_pages = [{"id": "123", "title": "Test Page 1"}, {"id": "456", "title": "Test Page 2"}]
        mock_get_paged.return_value = mock_pages
        
        # Call the method
        response = self.confluence.get_pages()
        
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
        response = self.confluence.get_pages(
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
            self.confluence.get_pages(status="invalid")
            
    def test_get_pages_invalid_sort(self):
        # Test invalid sort
        with self.assertRaises(ValueError):
            self.confluence.get_pages(sort="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_child_pages(self, mock_get_paged):
        # Setup the mock
        mock_pages = [{"id": "123", "title": "Child Page 1"}, {"id": "456", "title": "Child Page 2"}]
        mock_get_paged.return_value = mock_pages
        
        # Call the method
        response = self.confluence.get_child_pages("PARENT123")
        
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
        response = self.confluence.get_child_pages(
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
            self.confluence.get_child_pages("PARENT123", status="draft")  # draft is invalid for child pages
            
    def test_get_child_pages_invalid_sort(self):
        # Test invalid sort
        with self.assertRaises(ValueError):
            self.confluence.get_child_pages("PARENT123", sort="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2.post')
    def test_create_page(self, mock_post):
        # Setup the mock
        mock_response = {"id": "123", "title": "New Page", "status": "current"}
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.confluence.create_page(
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
        response = self.confluence.create_page(
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
        response = self.confluence.create_page(
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
            self.confluence.create_page(
                space_id="SPACE123",
                title="Test Page",
                body="Test content",
                body_format="invalid"
            )
            
    def test_create_page_invalid_status(self):
        # Test invalid status
        with self.assertRaises(ValueError):
            self.confluence.create_page(
                space_id="SPACE123",
                title="Test Page",
                body="Test content",
                status="invalid"
            )
            
    def test_create_page_wiki_without_representation(self):
        # Test wiki format without representation
        with self.assertRaises(ValueError):
            self.confluence.create_page(
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
        response = self.confluence.update_page(
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
        response = self.confluence.update_page(
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
        response = self.confluence.update_page(
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
            self.confluence.update_page(
                page_id="123",
                body="Test content",
                body_format="invalid"
            )
            
    def test_update_page_invalid_status(self):
        # Test invalid status
        with self.assertRaises(ValueError):
            self.confluence.update_page(
                page_id="123",
                status="invalid"
            )
            
    @patch('atlassian.confluence_v2.ConfluenceV2.delete')
    def test_delete_page(self, mock_delete):
        # Setup the mock
        mock_delete.return_value = None
        
        # Call the method
        result = self.confluence.delete_page("123")
        
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
        response = self.confluence.search("test query")
        
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
        response = self.confluence.search(
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
            self.confluence.search(query="", cql=None)
            
    def test_search_invalid_body_format(self):
        # Test invalid body_format
        with self.assertRaises(ValueError):
            self.confluence.search("test", body_format="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2.search')
    def test_search_content(self, mock_search):
        # Setup the mock
        mock_results = [{"content": {"id": "123"}}, {"content": {"id": "456"}}]
        mock_search.return_value = {"results": mock_results}
        
        # Call the method
        response = self.confluence.search_content(
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
        response = self.confluence.search_content("test")
        
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
            self.confluence.search_content("test", type="invalid")
            
    def test_search_content_invalid_status(self):
        # Test invalid status
        with self.assertRaises(ValueError):
            self.confluence.search_content("test", status="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_spaces(self, mock_get_paged):
        # Setup the mock
        mock_spaces = [
            {"id": "123", "key": "TEST", "name": "Test Space"},
            {"id": "456", "key": "DEV", "name": "Development Space"}
        ]
        mock_get_paged.return_value = mock_spaces
        
        # Call the method
        response = self.confluence.get_spaces()
        
        # Assertions
        mock_get_paged.assert_called_once_with('api/v2/spaces', params={'limit': 25})
        self.assertEqual(response, mock_spaces)
        
    @patch('atlassian.confluence_v2.ConfluenceV2._get_paged')
    def test_get_spaces_with_filters(self, mock_get_paged):
        # Setup the mock
        mock_spaces = [{"id": "123", "key": "TEST", "name": "Test Space"}]
        mock_get_paged.return_value = mock_spaces
        
        # Call the method with filters
        response = self.confluence.get_spaces(
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
        response = self.confluence.get_space("123")
        
        # Assertions
        mock_get.assert_called_once_with('api/v2/spaces/123')
        self.assertEqual(response, mock_space)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get_spaces')
    def test_get_space_by_key(self, mock_get_spaces):
        # Setup the mock
        mock_spaces = [{"id": "123", "key": "TEST", "name": "Test Space"}]
        mock_get_spaces.return_value = mock_spaces
        
        # Call the method
        response = self.confluence.get_space_by_key("TEST")
        
        # Assertions
        mock_get_spaces.assert_called_once_with(keys=["TEST"], limit=1)
        self.assertEqual(response, mock_spaces[0])
        
    @patch('atlassian.confluence_v2.ConfluenceV2.get_spaces')
    def test_get_space_by_key_not_found(self, mock_get_spaces):
        # Setup the mock to return empty list (no spaces found)
        mock_get_spaces.return_value = []
        
        # Test the method raises ValueError for non-existent key
        with self.assertRaises(ValueError):
            self.confluence.get_space_by_key("NONEXISTENT")
            
    def test_get_spaces_invalid_type(self):
        # Test invalid space type
        with self.assertRaises(ValueError):
            self.confluence.get_spaces(type="invalid")
            
    def test_get_spaces_invalid_status(self):
        # Test invalid space status
        with self.assertRaises(ValueError):
            self.confluence.get_spaces(status="invalid")
            
    def test_get_spaces_invalid_sort(self):
        # Test invalid sort parameter
        with self.assertRaises(ValueError):
            self.confluence.get_spaces(sort="invalid")
            
    @patch('atlassian.confluence_v2.ConfluenceV2.search')
    def test_get_space_content(self, mock_search):
        # Setup the mock
        mock_results = [{"content": {"id": "123", "title": "Page 1"}}]
        mock_search.return_value = {"results": mock_results}
        
        # Call the method
        response = self.confluence.get_space_content("SPACE123")
        
        # Assertions
        mock_search.assert_called_once_with(query="", cql='space.id = "SPACE123"', limit=25)
        self.assertEqual(response, mock_results)
        
    @patch('atlassian.confluence_v2.ConfluenceV2.search')
    def test_get_space_content_with_filters(self, mock_search):
        # Setup the mock
        mock_results = [{"content": {"id": "123", "title": "Root Page"}}]
        mock_search.return_value = {"results": mock_results}
        
        # Call the method with filters
        response = self.confluence.get_space_content(
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
            self.confluence.get_space_content("SPACE123", sort="invalid")
            
if __name__ == '__main__':
    unittest.main() 