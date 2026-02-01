# coding=utf-8
"""
Test cases for Confluence Cloud v2 API client.

This test suite provides comprehensive coverage of the v2 API implementation,
including unit tests with mocks and integration tests for real API validation.
"""

import pytest
from unittest.mock import patch

from atlassian.confluence.cloud.v2 import ConfluenceCloudV2
from atlassian.adf import validate_adf_document


@pytest.fixture
def confluence_v2():
    """Fixture for ConfluenceCloudV2 client."""
    return ConfluenceCloudV2(url="https://test.atlassian.net", token="test-token", cloud=True)


@pytest.fixture
def sample_adf_content():
    """Fixture providing sample ADF content for testing."""
    return {
        "version": 1,
        "type": "doc",
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello, World!"}]}],
    }


@pytest.fixture
def sample_page_response():
    """Fixture providing sample page response from v2 API."""
    return {
        "id": "123456",
        "status": "current",
        "title": "Test Page",
        "spaceId": "SPACE123",
        "parentId": "789012",
        "authorId": "user123",
        "createdAt": "2024-01-01T00:00:00.000Z",
        "version": {
            "number": 1,
            "message": "Initial version",
            "minorEdit": False,
            "authorId": "user123",
            "createdAt": "2024-01-01T00:00:00.000Z",
        },
        "body": {
            "representation": "atlas_doc_format",
            "value": {
                "version": 1,
                "type": "doc",
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Test content"}]}],
            },
        },
        "_links": {
            "webui": "/spaces/SPACE123/pages/123456",
            "editui": "/pages/resumedraft.action?draftId=123456",
            "tinyui": "/x/SPACE123",
        },
    }


@pytest.fixture
def sample_pages_response():
    """Fixture providing sample pages list response from v2 API."""
    return {
        "results": [
            {"id": "123456", "status": "current", "title": "Test Page 1", "spaceId": "SPACE123"},
            {"id": "789012", "status": "current", "title": "Test Page 2", "spaceId": "SPACE123"},
        ],
        "_links": {"next": {"href": "/wiki/api/v2/pages?cursor=next_cursor_token", "cursor": "next_cursor_token"}},
    }


@pytest.fixture
def sample_spaces_response():
    """Fixture providing sample spaces list response from v2 API."""
    return {
        "results": [
            {
                "id": "SPACE123",
                "key": "TEST",
                "name": "Test Space",
                "type": "global",
                "status": "current",
                "authorId": "user123",
                "createdAt": "2024-01-01T00:00:00.000Z",
            }
        ],
        "_links": {"next": {"href": "/wiki/api/v2/spaces?cursor=next_cursor_token", "cursor": "next_cursor_token"}},
    }


class TestConfluenceCloudV2Initialization:
    """Test cases for ConfluenceCloudV2 client initialization."""

    def test_init_defaults(self):
        """Test ConfluenceCloudV2 client initialization with default values."""
        confluence = ConfluenceCloudV2(url="https://test.atlassian.net", token="test-token")
        assert confluence.cloud is True
        assert confluence.api_root == "wiki/api/v2"
        assert confluence.api_version == ""
        assert "Content-Type" in confluence.v2_headers
        assert confluence.v2_headers["Content-Type"] == "application/json"

    def test_init_custom_values(self):
        """Test ConfluenceCloudV2 client initialization with custom values."""
        confluence = ConfluenceCloudV2(
            url="https://test.atlassian.net", token="test-token", api_root="custom/api/root", api_version="custom"
        )
        # v2 API should override certain values
        assert confluence.cloud is True
        assert confluence.api_root == "custom/api/root"  # Custom value respected
        assert confluence.api_version == "custom"  # Custom value respected


class TestConfluenceCloudV2ContentPreparation:
    """Test cases for content preparation methods."""

    def test_prepare_adf_content(self, confluence_v2, sample_adf_content):
        """Test preparing ADF content for v2 API."""
        result = confluence_v2._prepare_content_for_v2(sample_adf_content, "adf")

        assert result["representation"] == "atlas_doc_format"
        assert result["value"] == sample_adf_content
        assert validate_adf_document(result["value"])

    def test_prepare_text_content(self, confluence_v2):
        """Test preparing plain text content for v2 API."""
        text_content = "Hello, World!"
        result = confluence_v2._prepare_content_for_v2(text_content)

        assert result["representation"] == "atlas_doc_format"
        assert validate_adf_document(result["value"])
        assert result["value"]["type"] == "doc"
        assert result["value"]["version"] == 1

    def test_prepare_storage_content(self, confluence_v2):
        """Test preparing storage format content for v2 API."""
        storage_content = "<p>Hello, World!</p>"
        result = confluence_v2._prepare_content_for_v2(storage_content, "storage")

        assert result["representation"] == "atlas_doc_format"
        assert validate_adf_document(result["value"])

    def test_prepare_invalid_adf_content(self, confluence_v2):
        """Test preparing invalid ADF content raises error."""
        invalid_adf = {"type": "invalid", "content": []}

        with pytest.raises(ValueError, match="Invalid ADF content structure"):
            confluence_v2._prepare_content_for_v2(invalid_adf, "adf")

    def test_prepare_unsupported_content_format(self, confluence_v2):
        """Test preparing content with unsupported format."""
        with pytest.raises(ValueError, match="Unsupported content format"):
            confluence_v2._prepare_content_for_v2({"invalid": "data"})


class TestConfluenceCloudV2PageOperations:
    """Test cases for page operations using v2 API."""

    @patch.object(ConfluenceCloudV2, "get")
    def test_get_page_by_id(self, mock_get, confluence_v2, sample_page_response):
        """Test get_page_by_id method."""
        mock_get.return_value = sample_page_response

        result = confluence_v2.get_page_by_id("123456")

        # Verify the correct endpoint was called
        expected_endpoint = confluence_v2._get_v2_endpoint("pages/123456")
        expected_headers = confluence_v2.v2_headers
        # Without expand, params should be empty
        mock_get.assert_called_once_with(expected_endpoint, params={}, headers=expected_headers)

        assert result == sample_page_response
        assert result["id"] == "123456"
        assert result["title"] == "Test Page"

    @patch.object(ConfluenceCloudV2, "get")
    def test_get_page_by_id_with_expand(self, mock_get, confluence_v2, sample_page_response):
        """Test get_page_by_id method with expand parameters."""
        mock_get.return_value = sample_page_response

        result = confluence_v2.get_page_by_id("123456", expand=["body", "version", "space"])

        expected_endpoint = confluence_v2._get_v2_endpoint("pages/123456")
        expected_params = {"body-format": "atlas_doc_format", "expand": "body,version,space"}
        expected_headers = confluence_v2.v2_headers
        mock_get.assert_called_once_with(expected_endpoint, params=expected_params, headers=expected_headers)

        assert result == sample_page_response

    @patch.object(ConfluenceCloudV2, "get")
    def test_get_pages(self, mock_get, confluence_v2, sample_pages_response):
        """Test get_pages method with cursor pagination."""
        mock_get.return_value = sample_pages_response

        result = confluence_v2.get_pages(space_id="SPACE123", limit=50)

        expected_endpoint = confluence_v2._get_v2_endpoint("pages")
        expected_params = {"limit": 50, "body-format": "atlas_doc_format", "space-id": "SPACE123"}
        expected_headers = confluence_v2.v2_headers
        mock_get.assert_called_once_with(expected_endpoint, params=expected_params, headers=expected_headers)

        assert result == sample_pages_response
        assert len(result["results"]) == 2
        assert "next" in result["_links"]

    @patch.object(ConfluenceCloudV2, "get")
    def test_get_pages_with_cursor(self, mock_get, confluence_v2, sample_pages_response):
        """Test get_pages method with cursor for pagination."""
        mock_get.return_value = sample_pages_response

        result = confluence_v2.get_pages(limit=25, cursor="test_cursor")

        expected_endpoint = confluence_v2._get_v2_endpoint("pages")
        expected_params = {"limit": 25, "body-format": "atlas_doc_format", "cursor": "test_cursor"}
        expected_headers = confluence_v2.v2_headers
        mock_get.assert_called_once_with(expected_endpoint, params=expected_params, headers=expected_headers)

        assert result == sample_pages_response

    @patch.object(ConfluenceCloudV2, "post")
    def test_create_page_with_adf(self, mock_post, confluence_v2, sample_adf_content, sample_page_response):
        """Test create_page method with ADF content."""
        mock_post.return_value = sample_page_response

        result = confluence_v2.create_page(
            space_id="SPACE123", title="Test Page", content=sample_adf_content, content_format="adf"
        )

        expected_endpoint = confluence_v2._get_v2_endpoint("pages")
        expected_data = {
            "spaceId": "SPACE123",
            "title": "Test Page",
            "body": {"representation": "atlas_doc_format", "value": sample_adf_content},
        }
        expected_headers = confluence_v2.v2_headers
        mock_post.assert_called_once_with(expected_endpoint, json=expected_data, headers=expected_headers)

        assert result == sample_page_response

    @patch.object(ConfluenceCloudV2, "post")
    def test_create_page_with_text(self, mock_post, confluence_v2, sample_page_response):
        """Test create_page method with plain text content."""
        mock_post.return_value = sample_page_response

        result = confluence_v2.create_page(
            space_id="SPACE123", title="Test Page", content="Hello, World!", parent_id="789012"
        )

        expected_endpoint = confluence_v2._get_v2_endpoint("pages")
        expected_headers = confluence_v2.v2_headers
        # Verify the call was made (content will be converted to ADF internally)
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        assert call_args[0][0] == expected_endpoint
        assert call_args[1]["json"]["spaceId"] == "SPACE123"
        assert call_args[1]["json"]["title"] == "Test Page"
        assert call_args[1]["json"]["parentId"] == "789012"
        assert call_args[1]["json"]["body"]["representation"] == "atlas_doc_format"
        assert validate_adf_document(call_args[1]["json"]["body"]["value"])
        assert call_args[1]["headers"] == expected_headers

        assert result == sample_page_response

    @patch.object(ConfluenceCloudV2, "put")
    def test_update_page(self, mock_put, confluence_v2, sample_adf_content, sample_page_response):
        """Test update_page method."""
        mock_put.return_value = sample_page_response

        result = confluence_v2.update_page(
            page_id="123456", title="Updated Title", content=sample_adf_content, content_format="adf", version=2
        )

        expected_endpoint = confluence_v2._get_v2_endpoint("pages/123456")
        expected_data = {
            "title": "Updated Title",
            "body": {"representation": "atlas_doc_format", "value": sample_adf_content},
            "version": {"number": 2},
        }
        expected_headers = confluence_v2.v2_headers
        mock_put.assert_called_once_with(expected_endpoint, json=expected_data, headers=expected_headers)

        assert result == sample_page_response

    @patch.object(ConfluenceCloudV2, "put")
    def test_update_page_title_only(self, mock_put, confluence_v2, sample_page_response):
        """Test update_page method with title only."""
        mock_put.return_value = sample_page_response

        result = confluence_v2.update_page(page_id="123456", title="New Title")

        expected_endpoint = confluence_v2._get_v2_endpoint("pages/123456")
        expected_data = {"title": "New Title"}
        expected_headers = confluence_v2.v2_headers
        mock_put.assert_called_once_with(expected_endpoint, json=expected_data, headers=expected_headers)

        assert result == sample_page_response

    @patch.object(ConfluenceCloudV2, "delete")
    def test_delete_page(self, mock_delete, confluence_v2):
        """Test delete_page method."""
        mock_delete.return_value = None

        result = confluence_v2.delete_page("123456")

        expected_endpoint = confluence_v2._get_v2_endpoint("pages/123456")
        expected_headers = confluence_v2.v2_headers
        mock_delete.assert_called_once_with(expected_endpoint, headers=expected_headers)

        assert result is None


class TestConfluenceCloudV2SpaceOperations:
    """Test cases for space operations using v2 API."""

    @patch.object(ConfluenceCloudV2, "get")
    def test_get_spaces(self, mock_get, confluence_v2, sample_spaces_response):
        """Test get_spaces method."""
        mock_get.return_value = sample_spaces_response

        result = confluence_v2.get_spaces(limit=50)

        expected_endpoint = confluence_v2._get_v2_endpoint("spaces")
        expected_params = {"limit": 50}
        expected_headers = confluence_v2.v2_headers
        mock_get.assert_called_once_with(expected_endpoint, params=expected_params, headers=expected_headers)

        assert result == sample_spaces_response
        assert len(result["results"]) == 1
        assert result["results"][0]["key"] == "TEST"

    @patch.object(ConfluenceCloudV2, "get")
    def test_get_spaces_with_cursor(self, mock_get, confluence_v2, sample_spaces_response):
        """Test get_spaces method with cursor pagination."""
        mock_get.return_value = sample_spaces_response

        result = confluence_v2.get_spaces(limit=25, cursor="test_cursor")

        expected_endpoint = confluence_v2._get_v2_endpoint("spaces")
        expected_params = {"limit": 25, "cursor": "test_cursor"}
        expected_headers = confluence_v2.v2_headers
        mock_get.assert_called_once_with(expected_endpoint, params=expected_params, headers=expected_headers)

        assert result == sample_spaces_response


class TestConfluenceCloudV2SearchOperations:
    """Test cases for search operations using v2 API."""

    @patch.object(ConfluenceCloudV2, "get")
    def test_search_pages(self, mock_get, confluence_v2, sample_pages_response):
        """Test search_pages method with CQL."""
        mock_get.return_value = sample_pages_response

        cql_query = "type=page AND space=TEST"
        result = confluence_v2.search_pages(cql_query, limit=50)

        expected_endpoint = confluence_v2._get_v2_endpoint("pages")
        expected_params = {"cql": cql_query, "limit": 50, "body-format": "atlas_doc_format"}
        expected_headers = confluence_v2.v2_headers
        mock_get.assert_called_once_with(expected_endpoint, params=expected_params, headers=expected_headers)

        assert result == sample_pages_response

    @patch.object(ConfluenceCloudV2, "get")
    def test_search_pages_with_cursor(self, mock_get, confluence_v2, sample_pages_response):
        """Test search_pages method with cursor pagination."""
        mock_get.return_value = sample_pages_response

        cql_query = "type=page"
        result = confluence_v2.search_pages(cql_query, limit=25, cursor="search_cursor")

        expected_endpoint = confluence_v2._get_v2_endpoint("pages")
        expected_params = {"cql": cql_query, "limit": 25, "body-format": "atlas_doc_format", "cursor": "search_cursor"}
        expected_headers = confluence_v2.v2_headers
        mock_get.assert_called_once_with(expected_endpoint, params=expected_params, headers=expected_headers)

        assert result == sample_pages_response


class TestConfluenceCloudV2UtilityMethods:
    """Test cases for utility methods."""

    def test_get_v2_endpoint(self, confluence_v2):
        """Test _get_v2_endpoint method."""
        endpoint = confluence_v2._get_v2_endpoint("pages")
        assert "wiki/api/v2" in endpoint
        assert endpoint.endswith("pages")

    def test_get_v2_endpoint_with_id(self, confluence_v2):
        """Test _get_v2_endpoint method with resource ID."""
        endpoint = confluence_v2._get_v2_endpoint("pages/123456")
        assert "wiki/api/v2" in endpoint
        assert endpoint.endswith("pages/123456")

    @patch.object(ConfluenceCloudV2, "get")
    def test_v2_request_get(self, mock_get, confluence_v2):
        """Test _v2_request method with GET."""
        mock_get.return_value = {"test": "data"}

        result = confluence_v2._v2_request("GET", "test/endpoint")

        expected_headers = confluence_v2.v2_headers
        mock_get.assert_called_once_with("test/endpoint", headers=expected_headers)
        assert result == {"test": "data"}

    @patch.object(ConfluenceCloudV2, "post")
    def test_v2_request_post(self, mock_post, confluence_v2):
        """Test _v2_request method with POST."""
        mock_post.return_value = {"created": "data"}

        result = confluence_v2._v2_request("POST", "test/endpoint", json={"test": "data"})

        expected_headers = confluence_v2.v2_headers
        mock_post.assert_called_once_with("test/endpoint", headers=expected_headers, json={"test": "data"})
        assert result == {"created": "data"}

    def test_v2_request_unsupported_method(self, confluence_v2):
        """Test _v2_request method with unsupported HTTP method."""
        with pytest.raises(ValueError, match="Unsupported HTTP method: PATCH"):
            confluence_v2._v2_request("PATCH", "test/endpoint")


class TestConfluenceCloudV2ErrorHandling:
    """Test cases for error handling in v2 API operations."""

    @patch.object(ConfluenceCloudV2, "get")
    def test_get_page_by_id_not_found(self, mock_get, confluence_v2):
        """Test get_page_by_id method when page is not found."""
        from atlassian.errors import ApiError

        mock_get.side_effect = ApiError("Page not found", status_code=404)

        with pytest.raises(ApiError):
            confluence_v2.get_page_by_id("nonexistent")

    @patch.object(ConfluenceCloudV2, "post")
    def test_create_page_permission_denied(self, mock_post, confluence_v2, sample_adf_content):
        """Test create_page method when permission is denied."""
        from atlassian.errors import ApiError

        mock_post.side_effect = ApiError("Permission denied", status_code=403)

        with pytest.raises(ApiError):
            confluence_v2.create_page(
                space_id="RESTRICTED", title="Test Page", content=sample_adf_content, content_format="adf"
            )

    @patch.object(ConfluenceCloudV2, "put")
    def test_update_page_version_conflict(self, mock_put, confluence_v2):
        """Test update_page method when version conflict occurs."""
        from atlassian.errors import ApiError

        mock_put.side_effect = ApiError("Version conflict", status_code=409)

        with pytest.raises(ApiError):
            confluence_v2.update_page(page_id="123456", title="Updated Title", version=1)  # Outdated version


class TestConfluenceCloudV2Integration:
    """
    Integration tests for Confluence Cloud v2 API.

    These tests require real Confluence Cloud credentials and are marked
    as integration tests. They can be skipped in CI/CD environments.

    To run integration tests:
    pytest -m integration tests/confluence/test_confluence_cloud_v2.py

    To skip integration tests:
    pytest -m "not integration" tests/confluence/test_confluence_cloud_v2.py
    """

    @pytest.fixture
    def confluence_integration(self):
        """
        Fixture for real Confluence Cloud integration testing.

        Requires environment variables:
        - CONFLUENCE_URL: Confluence Cloud URL
        - CONFLUENCE_TOKEN: API token
        - CONFLUENCE_SPACE_ID: Test space ID
        """
        import os

        url = os.getenv("CONFLUENCE_URL")
        token = os.getenv("CONFLUENCE_TOKEN")
        space_id = os.getenv("CONFLUENCE_SPACE_ID")

        if not all([url, token, space_id]):
            pytest.skip("Integration test credentials not configured")

        return {"client": ConfluenceCloudV2(url=url, token=token), "space_id": space_id}

    @pytest.mark.integration
    def test_integration_get_spaces(self, confluence_integration):
        """Integration test for get_spaces method."""
        client = confluence_integration["client"]

        result = client.get_spaces(limit=10)

        assert "results" in result
        assert isinstance(result["results"], list)
        if result["results"]:
            space = result["results"][0]
            assert "id" in space
            assert "key" in space
            assert "name" in space

    @pytest.mark.integration
    def test_integration_get_pages(self, confluence_integration):
        """Integration test for get_pages method."""
        client = confluence_integration["client"]
        space_id = confluence_integration["space_id"]

        result = client.get_pages(space_id=space_id, limit=5)

        assert "results" in result
        assert isinstance(result["results"], list)

    @pytest.mark.integration
    def test_integration_search_pages(self, confluence_integration):
        """Integration test for search_pages method."""
        client = confluence_integration["client"]
        space_id = confluence_integration["space_id"]

        cql_query = f"type=page AND space={space_id}"
        result = client.search_pages(cql_query, limit=5)

        assert "results" in result
        assert isinstance(result["results"], list)

    @pytest.mark.integration
    def test_integration_create_update_delete_page(self, confluence_integration):
        """Integration test for complete page lifecycle."""
        client = confluence_integration["client"]
        space_id = confluence_integration["space_id"]

        # Create test page with ADF content
        adf_content = {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "This is a test page created by the v2 API test suite."}],
                }
            ],
        }

        # Create page
        created_page = client.create_page(
            space_id=space_id, title="V2 API Test Page", content=adf_content, content_format="adf"
        )

        assert created_page["title"] == "V2 API Test Page"
        assert created_page["spaceId"] == space_id
        page_id = created_page["id"]

        try:
            # Get the created page
            retrieved_page = client.get_page_by_id(page_id, expand=["body", "version"])
            assert retrieved_page["id"] == page_id
            assert retrieved_page["title"] == "V2 API Test Page"

            # Update the page
            updated_adf = {
                "version": 1,
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": "This page has been updated by the v2 API test suite."}],
                    }
                ],
            }

            updated_page = client.update_page(
                page_id=page_id,
                title="Updated V2 API Test Page",
                content=updated_adf,
                content_format="adf",
                version=retrieved_page["version"]["number"] + 1,
            )

            assert updated_page["title"] == "Updated V2 API Test Page"

        finally:
            # Clean up: delete the test page
            client.delete_page(page_id)
