# coding=utf-8
import unittest
from unittest.mock import patch, MagicMock, mock_open

from atlassian import Confluence, ConfluenceBase, ConfluenceV2, create_confluence


class TestConfluenceBase(unittest.TestCase):
    """Test cases for ConfluenceBase implementation"""

    def test_init_with_api_version_1(self):
        """Test initialization with API version 1"""
        client = Confluence('https://example.atlassian.net', api_version=1)
        self.assertEqual(client.api_version, 1)
        self.assertEqual(client.url, 'https://example.atlassian.net/wiki')

    def test_init_with_api_version_2(self):
        """Test initialization with API version 2"""
        client = Confluence('https://example.atlassian.net', api_version=2)
        self.assertEqual(client.api_version, 2)
        self.assertEqual(client.url, 'https://example.atlassian.net/wiki')

    def test_get_endpoint_v1(self):
        """Test retrieving v1 endpoint"""
        client = Confluence('https://example.atlassian.net', api_version=1)
        endpoint = client.get_endpoint('content')
        self.assertEqual(endpoint, '/rest/api/content')

    def test_get_endpoint_v2(self):
        """Test retrieving v2 endpoint"""
        client = Confluence('https://example.atlassian.net', api_version=2)
        endpoint = client.get_endpoint('content')
        self.assertEqual(endpoint, '/api/v2/pages')

    def test_invalid_api_version(self):
        """Test raising error with invalid API version"""
        with self.assertRaises(ValueError):
            ConfluenceBase('https://example.atlassian.net', api_version=3)

    def test_factory_v1(self):
        """Test factory method creating v1 client"""
        client = ConfluenceBase.factory('https://example.atlassian.net', api_version=1)
        self.assertIsInstance(client, Confluence)
        self.assertEqual(client.api_version, 1)

    def test_factory_v2(self):
        """Test factory method creating v2 client"""
        client = ConfluenceBase.factory('https://example.atlassian.net', api_version=2)
        self.assertIsInstance(client, ConfluenceV2)
        self.assertEqual(client.api_version, 2)

    def test_factory_default(self):
        """Test factory method with default version"""
        client = ConfluenceBase.factory('https://example.atlassian.net')
        self.assertIsInstance(client, Confluence)
        self.assertEqual(client.api_version, 1)

    def test_create_confluence_function_v1(self):
        """Test create_confluence function with v1"""
        client = create_confluence('https://example.atlassian.net', api_version=1)
        self.assertIsInstance(client, Confluence)
        self.assertEqual(client.api_version, 1)

    def test_create_confluence_function_v2(self):
        """Test create_confluence function with v2"""
        client = create_confluence('https://example.atlassian.net', api_version=2)
        self.assertIsInstance(client, ConfluenceV2)
        self.assertEqual(client.api_version, 2)

    @patch('requests.Session.request')
    def test_get_paged_v1(self, mock_request):
        """Test pagination with v1 API"""
        # Mock response for first page
        first_response = MagicMock()
        first_response.json.return_value = {
            'results': [{'id': '1', 'title': 'Page 1'}],
            'start': 0,
            'limit': 1,
            'size': 1, 
            '_links': {'next': '/rest/api/content?start=1&limit=1'}
        }
        
        # Mock response for second page
        second_response = MagicMock()
        second_response.json.return_value = {
            'results': [{'id': '2', 'title': 'Page 2'}],
            'start': 1,
            'limit': 1,
            'size': 1,
            '_links': {}
        }
        
        # Set up mock request to return the responses in sequence
        mock_request.side_effect = [first_response, second_response]
        
        # Create client and call _get_paged
        client = Confluence('https://example.atlassian.net', api_version=1)
        endpoint = '/rest/api/content'
        params = {'limit': 1}
        
        results = list(client._get_paged(endpoint, params=params))
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], '1')
        self.assertEqual(results[1]['id'], '2')
        
        # Verify the API was called with correct parameters
        calls = mock_request.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][1]['params'], {'limit': 1})
        self.assertEqual(calls[1][1]['params'], {'start': 1, 'limit': 1})

    @patch('requests.Session.request')
    def test_get_paged_v2(self, mock_request):
        """Test pagination with v2 API"""
        # Mock response for first page
        first_response = MagicMock()
        first_response.json.return_value = {
            'results': [{'id': '1', 'title': 'Page 1'}],
            '_links': {'next': '/api/v2/pages?cursor=next_cursor'}
        }
        
        # Mock response for second page
        second_response = MagicMock()
        second_response.json.return_value = {
            'results': [{'id': '2', 'title': 'Page 2'}],
            '_links': {}
        }
        
        # Set up mock request to return the responses in sequence
        mock_request.side_effect = [first_response, second_response]
        
        # Create client and call _get_paged
        client = ConfluenceV2('https://example.atlassian.net')
        endpoint = '/api/v2/pages'
        params = {'limit': 1}
        
        results = list(client._get_paged(endpoint, params=params))
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], '1')
        self.assertEqual(results[1]['id'], '2')
        
        # Verify the API was called with correct parameters
        calls = mock_request.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][1]['params'], {'limit': 1})
        self.assertEqual(calls[1][1]['params'], {'cursor': 'next_cursor'})


class TestConfluenceV2(unittest.TestCase):
    """Test cases for ConfluenceV2 implementation"""

    def test_init(self):
        """Test ConfluenceV2 initialization sets correct API version"""
        client = ConfluenceV2('https://example.atlassian.net')
        self.assertEqual(client.api_version, 2)
        self.assertEqual(client.url, 'https://example.atlassian.net/wiki')

    def test_init_with_explicit_version(self):
        """Test ConfluenceV2 initialization with explicit API version"""
        client = ConfluenceV2('https://example.atlassian.net', api_version=2)
        self.assertEqual(client.api_version, 2)
        
        # Should ignore attempt to set version to 1
        client = ConfluenceV2('https://example.atlassian.net', api_version=1)
        self.assertEqual(client.api_version, 2)


if __name__ == '__main__':
    unittest.main() 