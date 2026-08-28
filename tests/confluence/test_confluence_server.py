# coding=utf-8
"""
Test cases for Confluence Server API client.
"""

import io
import logging

import pytest
from requests import HTTPError, Response
from types import SimpleNamespace
from unittest.mock import call, patch

from atlassian.confluence import ConfluenceServer
from atlassian.errors import ApiError, ApiNotAcceptable, ApiNotFoundError, ApiPermissionError, ApiValueError


@pytest.fixture
def confluence_server():
    """Fixture for ConfluenceServer client."""
    return ConfluenceServer(url="https://test.confluence.com", username="test", password="test", cloud=False)


class TestConfluenceServer:
    """Test cases for ConfluenceServer client."""

    def test_init_defaults(self):
        """Test ConfluenceServer client initialization with default values."""
        confluence = ConfluenceServer(url="https://test.confluence.com", username="test", password="test")
        assert confluence.api_version == "1.0"
        assert confluence.api_root == "rest/api"
        assert confluence.cloud is False
        assert confluence.url == "https://test.confluence.com"

    def test_init_custom_values(self):
        """Test ConfluenceServer client initialization with custom values."""
        confluence = ConfluenceServer(
            url="https://test.confluence.com",
            username="test",
            password="test",
            api_version="2.0",
            api_root="custom/api/root",
        )
        assert confluence.api_version == "2.0"
        assert confluence.api_root == "custom/api/root"

    def test_default_server_requests_preserve_legacy_urls(self):
        confluence = ConfluenceServer(url="https://test.confluence.com", token="test-token")
        response = Response()
        response.status_code = 200
        response.reason = "OK"
        response._content = b'{"id": "123"}'

        with patch.object(confluence._session, "request", return_value=response) as mock_request:
            assert confluence.get_page_by_id("123") == {"id": "123"}

        assert mock_request.call_args.kwargs["url"] == "https://test.confluence.com/rest/api/content/123"

    @pytest.mark.parametrize(
        ("method", "path", "kwargs", "expected_path"),
        [
            ("post", "rest/api/content", {"data": {}}, "rest/api/content"),
            ("put", "/rest/api/content/123", {"data": {}}, "rest/api/content/123"),
            ("delete", "rest/api/content/123", {"params": {}}, "rest/api/content/123"),
        ],
    )
    def test_legacy_rooted_request_paths_are_not_prefixed_twice(self, method, path, kwargs, expected_path):
        confluence = ConfluenceServer(url="https://test.confluence.com", token="test-token")
        response = Response()
        response.status_code = 200
        response.reason = "OK"

        with patch.object(confluence._session, "request", return_value=response) as mock_request:
            getattr(confluence, method)(path=path, advanced_mode=True, **kwargs)

        assert mock_request.call_args.kwargs["url"] == f"https://test.confluence.com/{expected_path}"

    def test_explicit_server_api_version_applies_to_unrooted_resources(self):
        confluence = ConfluenceServer(
            url="https://test.confluence.com",
            token="test-token",
            api_root="custom/api/root",
            api_version="2.0",
        )
        response = Response()
        response.status_code = 200
        response.reason = "OK"
        response._content = b'{"id": "123"}'

        with patch.object(confluence._session, "request", return_value=response) as mock_request:
            assert confluence.get_page_by_id("123") == {"id": "123"}

        assert mock_request.call_args.kwargs["url"] == "https://test.confluence.com/custom/api/root/2.0/content/123"

    def test_server_ui_exports_remain_site_relative(self):
        confluence = ConfluenceServer(url="https://test.confluence.com", token="test-token")
        response = Response()
        response.status_code = 200
        response.reason = "OK"
        response._content = b"%PDF-1.4"

        with patch.object(confluence._session, "request", return_value=response) as mock_request:
            assert confluence.get_page_as_pdf("123") == b"%PDF-1.4"
            pdf_url = mock_request.call_args.kwargs["url"]

            mock_request.reset_mock()
            response._content = b"word export"
            assert confluence.get_page_as_word("123") == b"word export"
            word_url = mock_request.call_args.kwargs["url"]

        assert pdf_url == "https://test.confluence.com/spaces/flyingpdf/pdfpageexport.action?pageId=123"
        assert word_url == "https://test.confluence.com/exportword?pageId=123"

    def test_bad_request_includes_confluence_validation_details(self, confluence_server):
        response = Response()
        response.status_code = 400
        response.reason = "Bad Request"
        response._content = (
            b'{"message":"Invalid storage format",'
            b'"detail":"The ac:link element is not closed",'
            b'"errors":{"body":"Invalid XHTML at line 17"}}'
        )

        with pytest.raises(HTTPError) as error:
            confluence_server.raise_for_status(response)
        assert "Invalid storage format" in str(error.value)
        assert "ac:link element is not closed" in str(error.value)
        assert "Invalid XHTML at line 17" in str(error.value)

    def test_bad_request_includes_a_bounded_non_json_response(self, confluence_server):
        response = Response()
        response.status_code = 400
        response.reason = "Bad Request"
        response._content = b"<html><body>Malformed XHTML near the table macro</body></html>"

        with pytest.raises(HTTPError, match="Malformed XHTML near the table macro"):
            confluence_server.raise_for_status(response)

    @patch.object(ConfluenceServer, "post")
    def test_create_page_includes_first_version_comment(self, mock_post, confluence_server):
        mock_post.return_value = {"id": "123"}

        confluence_server.create_page("TEAM", "Report", "<p>Body</p>", version_comment="Initial import")

        assert mock_post.call_args.kwargs["data"]["version"] == {"message": "Initial import"}

    @patch.object(ConfluenceServer, "get")
    @patch.object(ConfluenceServer, "post")
    def test_attach_content_checks_existing_attachments_before_create(self, mock_post, mock_get, confluence_server):
        content = io.BytesIO(b"new image")
        mock_get.return_value = {"results": []}
        mock_post.return_value = {"results": [{"id": "attachment-1"}]}

        confluence_server.attach_content(content, "diagram.png", "image/png", page_id="123")

        mock_get.assert_called_once_with(
            path="rest/api/content/123/child/attachment",
            headers={"X-Atlassian-Token": "no-check", "Accept": "application/json"},
        )
        assert mock_post.call_args.kwargs["path"] == "rest/api/content/123/child/attachment"
        assert mock_post.call_args.kwargs["headers"] == {
            "X-Atlassian-Token": "no-check",
            "Accept": "application/json",
        }
        assert mock_post.call_args.kwargs["files"] == {"file": ("diagram.png", content, "image/png")}

    @patch.object(ConfluenceServer, "get")
    @patch.object(ConfluenceServer, "post")
    def test_attach_content_normalizes_path_like_attachment_names(self, mock_post, mock_get, confluence_server):
        content = io.BytesIO(b"new image")
        mock_get.return_value = {"results": []}
        mock_post.return_value = {"results": [{"id": "attachment-1"}]}

        confluence_server.attach_content(content, r"reports\\daily/diagram.png", "image/png", page_id="123")

        assert mock_post.call_args.kwargs["files"] == {"file": ("diagram.png", content, "image/png")}

    def test_attach_content_rejects_empty_attachment_name(self, confluence_server):
        with pytest.raises(ApiValueError, match="must contain a filename"):
            confluence_server.attach_content(io.BytesIO(b"content"), "/", page_id="123")

    def test_download_attachments_accepts_historical_download_path_alias(self, confluence_server):
        with patch.object(confluence_server, "get_attachments_from_content", return_value={"results": []}):
            assert confluence_server.download_attachments_from_page("123", download_path="/tmp") == {
                "attachments_downloaded": 0,
                "path": "/tmp",
            }

    def test_download_attachments_rejects_conflicting_path_arguments(self, confluence_server):
        with pytest.raises(ApiValueError, match="only one"):
            confluence_server.download_attachments_from_page("123", path="/tmp/a", download_path="/tmp/b")

    @patch.object(ConfluenceServer, "put")
    def test_set_restrictions_for_content_uses_rest_setter(self, mock_put, confluence_server):
        restrictions = [{"operation": "read", "restrictions": {"user": [{"type": "known", "username": "ada"}]}}]
        mock_put.return_value = {"restrictions": restrictions}

        assert confluence_server.set_restrictions_for_content("123", restrictions) == {"restrictions": restrictions}
        mock_put.assert_called_once_with("rest/api/content/123/restriction", data=restrictions)

    def test_set_restrictions_for_content_requires_a_list(self, confluence_server):
        with pytest.raises(ApiValueError, match="must be a list"):
            confluence_server.set_restrictions_for_content("123", {"operation": "read"})

    @patch.object(ConfluenceServer, "get_page_child_by_type")
    @patch.object(ConfluenceServer, "get_page_as_pdf")
    def test_iter_page_tree_as_pdf_exports_every_descendant_in_tree_order(
        self, mock_get_pdf, mock_get_children, confluence_server
    ):
        mock_get_pdf.side_effect = [b"%PDF-root", b"%PDF-first", b"%PDF-grandchild", b"%PDF-second"]
        mock_get_children.side_effect = [
            iter([{"id": "first"}, {"id": "second"}]),
            iter([{"id": "grandchild"}]),
            iter([]),
            iter([]),
        ]

        assert list(confluence_server.iter_page_tree_as_pdf("root")) == [
            ("root", b"%PDF-root"),
            ("first", b"%PDF-first"),
            ("grandchild", b"%PDF-grandchild"),
            ("second", b"%PDF-second"),
        ]

    @patch.object(ConfluenceServer, "update_space")
    def test_set_space_homepage_uses_space_update_payload(self, mock_update_space, confluence_server):
        mock_update_space.return_value = {"key": "TEAM", "homepage": {"id": "123"}}

        assert confluence_server.set_space_homepage("TEAM", "123") == {
            "key": "TEAM",
            "homepage": {"id": "123"},
        }
        mock_update_space.assert_called_once_with("TEAM", {"homepage": {"id": "123"}})

    @patch.object(ConfluenceServer, "_get_paged")
    def test_get_all_page_versions_follows_paginated_history(self, mock_get_paged, confluence_server):
        mock_get_paged.return_value = iter([{"number": 2}, {"number": 1}])

        assert confluence_server.get_all_page_versions("123", limit=50, expand="collaborators") == [
            {"number": 2},
            {"number": 1},
        ]
        mock_get_paged.assert_called_once_with("content/123/version", params={"limit": 50, "expand": "collaborators"})

    @patch.object(ConfluenceServer, "get_page_by_id")
    def test_identical_page_content_is_logged_as_info_not_warning(self, mock_get_page, confluence_server, caplog):
        mock_get_page.side_effect = [
            {"title": "Status"},
            {"body": {"storage": {"value": "<p>unchanged</p>"}}},
        ]

        with caplog.at_level(logging.INFO, logger="atlassian.confluence.server"):
            assert confluence_server.is_page_content_is_already_updated("123", "<p>unchanged</p>", "Status")

        assert "Content of 123 is exactly the same" in caplog.text
        assert not [record for record in caplog.records if record.levelno == logging.WARNING]

    @patch.object(ConfluenceServer, "_insert_to_existing_page")
    def test_append_page_renders_structured_input_as_json_code_block(self, mock_insert, confluence_server):
        confluence_server.append_page("123", "Status", {"users": ["Ada"]})

        body = mock_insert.call_args.args[2]
        assert '<ac:structured-macro ac:name="code">' in body
        assert '<ac:parameter ac:name="language">json</ac:parameter>' in body
        assert '"users": [' in body
        assert '"Ada"' in body

    def test_append_page_rejects_structured_input_for_wiki_representation(self, confluence_server):
        with pytest.raises(ApiValueError, match="representation='storage'"):
            confluence_server.append_page("123", "Status", ["Ada"], representation="wiki")

    @patch.object(ConfluenceServer, "get_page_by_id")
    def test_get_tables_from_page_returns_consistent_empty_summary(self, mock_get_page, confluence_server):
        mock_get_page.return_value = {"body": {"storage": {"value": "<p>No tables</p>"}}}

        result = confluence_server.get_tables_from_page("123")

        assert result == {"page_id": "123", "number_of_tables_in_page": 0, "tables_content": []}

    @patch.object(ConfluenceServer, "get_page_by_id")
    def test_get_tables_from_page_returns_consistent_table_summary(self, mock_get_page, confluence_server):
        mock_get_page.return_value = {
            "body": {"storage": {"value": "<table><tr><th>Name</th><td>Value</td></tr></table>"}}
        }

        result = confluence_server.get_tables_from_page("123")

        assert result == {
            "page_id": "123",
            "number_of_tables_in_page": 1,
            "tables_content": [[["Name", "Value"]]],
        }

    @patch.object(ConfluenceServer, "get_page_id")
    def test_attach_content_raises_when_target_page_cannot_be_resolved(self, mock_get_page_id, confluence_server):
        mock_get_page_id.return_value = None

        with pytest.raises(ApiNotFoundError):
            confluence_server.attach_content(b"content", "attachment.txt", title="Missing", space="SPACE")

    @patch.object(ConfluenceServer, "history")
    def test_update_page_raises_when_target_page_cannot_be_resolved(self, mock_history, confluence_server):
        mock_history.return_value = None

        with pytest.raises(ApiNotFoundError):
            confluence_server.update_page("123", "Missing page")

    @pytest.mark.parametrize("method, args", [("remove_content", ("123",)), ("remove_page", ("123",))])
    @patch.object(ConfluenceServer, "delete")
    def test_delete_content_403_raises_explicit_permission_error(self, mock_delete, confluence_server, method, args):
        response = Response()
        response.status_code = 403
        mock_delete.side_effect = HTTPError(response=response)

        with pytest.raises(ApiPermissionError, match="does not have permission to trash or purge"):
            getattr(confluence_server, method)(*args)

    @patch.object(ConfluenceServer, "delete")
    def test_remove_page_returns_successful_delete_status(self, mock_delete, confluence_server):
        response = Response()
        response.status_code = 204
        mock_delete.return_value = response

        assert confluence_server.remove_page("123") == 204
        mock_delete.assert_called_once_with("rest/api/content/123", params={}, advanced_mode=True)

    @patch.object(ConfluenceServer, "delete")
    def test_remove_page_preserves_advanced_mode_response(self, mock_delete, confluence_server):
        response = Response()
        response.status_code = 204
        mock_delete.return_value = response
        confluence_server.advanced_mode = True

        assert confluence_server.remove_page("123") is response

    @patch.object(ConfluenceServer, "post")
    def test_set_page_property_deserializes_json_string_payload(self, mock_post, confluence_server):
        property_data = '{"key": "myprop", "value": {"hash": "1111"}}'

        confluence_server.set_page_property("123", property_data)

        mock_post.assert_called_once_with(
            path="content/123/property", data={"key": "myprop", "value": {"hash": "1111"}}
        )

    @patch.object(ConfluenceServer, "delete")
    @patch.object(ConfluenceServer, "get_page_child_by_type")
    def test_remove_page_recursively_lists_all_children_before_deleting(
        self, mock_get_children, mock_delete, confluence_server
    ):
        children_fully_listed = False

        def children():
            nonlocal children_fully_listed
            yield {"id": "first"}
            yield {"id": "second"}
            children_fully_listed = True

        mock_get_children.side_effect = [children(), iter(()), iter(())]

        def delete_after_children_are_listed(*args, **kwargs):
            assert children_fully_listed
            return Response()

        mock_delete.side_effect = delete_after_children_are_listed

        confluence_server.remove_page("root", recursive=True)

        assert children_fully_listed
        assert [call.args[0] for call in mock_delete.call_args_list] == [
            "rest/api/content/first",
            "rest/api/content/second",
            "rest/api/content/root",
        ]

    @patch.object(ConfluenceServer, "put")
    @patch.object(ConfluenceServer, "history")
    def test_update_page_uses_configured_api_root_without_duplicate_rest_api_prefix(
        self, mock_history, mock_put, confluence_server
    ):
        mock_history.return_value = {"lastUpdated": {"number": 1}}
        mock_put.return_value = {"id": "123"}

        result = confluence_server.update_page("123", "Updated", body="<p>Updated</p>", always_update=True)

        assert result == {"id": "123"}
        assert mock_put.call_args.args[0] == "content/123"
        assert mock_put.call_args.kwargs["data"]["body"] == {
            "storage": {"value": "<p>Updated</p>", "representation": "storage"}
        }

    @patch.object(ConfluenceServer, "put")
    @patch.object(ConfluenceServer, "history")
    def test_update_page_400_explains_storage_markup_requirements(self, mock_history, mock_put, confluence_server):
        mock_history.return_value = {"lastUpdated": {"number": 1}}
        response = Response()
        response.status_code = 400
        mock_put.side_effect = HTTPError(response=response)

        with pytest.raises(ApiValueError, match="valid storage XHTML"):
            confluence_server.update_page("123", "Updated", body="<p>Invalid & text</p>", always_update=True)

    @patch.object(ConfluenceServer, "post")
    def test_create_page_403_explains_that_space_key_is_required(self, mock_post, confluence_server):
        response = Response()
        response.status_code = 403
        mock_post.side_effect = HTTPError(response=response)

        with pytest.raises(ApiPermissionError, match="space key"):
            confluence_server.create_page("Space display name", "Title", "<p>Body</p>")

    @patch.object(ConfluenceServer, "get")
    def test_get_page_by_id_uses_configured_api_root_without_duplicate_rest_api_prefix(
        self, mock_get, confluence_server
    ):
        mock_get.return_value = {"id": "123"}

        assert confluence_server.get_page_by_id("123") == {"id": "123"}
        mock_get.assert_called_once_with("content/123", params={})

    @patch.object(ConfluenceServer, "get")
    def test_history_uses_configured_api_root_without_duplicate_rest_api_prefix(self, mock_get, confluence_server):
        mock_get.return_value = {"lastUpdated": {"number": 1}}

        assert confluence_server.history("123") == {"lastUpdated": {"number": 1}}
        mock_get.assert_called_once_with("content/123/history")

    @patch.object(ConfluenceServer, "get")
    def test_get_page_id_by_url_resolves_short_url(self, mock_get, confluence_server):
        mock_get.return_value = SimpleNamespace(
            url="https://test.confluence.com/pages/viewpage.action?pageId=40734334", content=b""
        )

        assert confluence_server.get_page_id_by_url("https://test.confluence.com/x/-_Z3") == "40734334"
        mock_get.assert_called_once_with("https://test.confluence.com/x/-_Z3", absolute=True, advanced_mode=True)

    @patch.object(ConfluenceServer, "get")
    def test_get_page_id_by_url_reads_display_page_metadata(self, mock_get, confluence_server):
        mock_get.return_value = SimpleNamespace(
            url="https://test.confluence.com/display/DOCS/A+page",
            content=b'<meta name="ajs-page-id" content="40734334">',
        )

        assert confluence_server.get_page_id_by_url("https://test.confluence.com/display/DOCS/A+page") == "40734334"

    @patch.object(ConfluenceServer, "get")
    def test_get_page_id_by_url_reads_page_id_query_without_request(self, mock_get, confluence_server):
        assert (
            confluence_server.get_page_id_by_url("https://test.confluence.com/pages/viewpage.action?pageId=40734334")
            == "40734334"
        )
        mock_get.assert_not_called()

    @patch.object(ConfluenceServer, "get_page_by_title")
    def test_page_exists_returns_false_for_not_found_response(self, mock_get_page_by_title, confluence_server):
        response = Response()
        response.status_code = 404
        mock_get_page_by_title.side_effect = HTTPError(response=response)

        assert confluence_server.page_exists("TEST", "Missing") is False

    @patch.object(ConfluenceServer, "get_page_by_id")
    def test_get_page_child_count_uses_expanded_child_metadata(self, mock_get_page, confluence_server):
        mock_get_page.return_value = {"children": {"page": {"size": 3, "results": [{"id": "1"}]}}}

        assert confluence_server.get_page_child_count("123") == 3
        assert confluence_server.page_has_children("123") is True
        mock_get_page.assert_called_with("123", expand="children.page")

    @patch.object(ConfluenceServer, "get_page_by_id")
    def test_page_has_children_uses_empty_children_result_when_size_is_absent(self, mock_get_page, confluence_server):
        mock_get_page.return_value = {"children": {"page": {"results": []}}}

        assert confluence_server.get_page_child_count("123") == 0
        assert confluence_server.page_has_children("123") is False

    def test_license_endpoints_explain_they_are_not_available_in_cloud(self):
        confluence = ConfluenceServer(url="https://test.atlassian.net", username="test", password="test", cloud=True)

        with pytest.raises(ApiNotAcceptable, match="Cloud does not provide license details"):
            confluence.get_license_details()

    @patch.object(ConfluenceServer, "remove_page_history")
    @patch.object(ConfluenceServer, "get_page_by_id")
    def test_remove_page_history_keep_version_uses_distinct_version_numbers(
        self, mock_get_page, mock_remove_history, confluence_server
    ):
        """Deleting a version must not assume Confluence renumbers history."""
        mock_get_page.return_value = {"title": "Test Page", "version": {"number": 5}}

        confluence_server.remove_page_history_keep_version("123", keep_last_versions=2)

        mock_get_page.assert_called_once_with(page_id="123", expand="version")
        assert mock_remove_history.call_args_list == [
            ((), {"page_id": "123", "version_number": 1}),
            ((), {"page_id": "123", "version_number": 2}),
            ((), {"page_id": "123", "version_number": 3}),
        ]

    def test_remove_page_history_keep_version_requires_positive_retention(self, confluence_server):
        with pytest.raises(ValueError, match="positive integer"):
            confluence_server.remove_page_history_keep_version("123", keep_last_versions=0)

    @patch.object(ConfluenceServer, "remove_page_history")
    @patch.object(ConfluenceServer, "get_page_by_id")
    def test_remove_page_history_keep_version_skips_versions_already_deleted(
        self, mock_get_page, mock_remove_history, confluence_server
    ):
        mock_get_page.return_value = {"title": "Test Page", "version": {"number": 5}}
        response = Response()
        response.status_code = 404
        mock_remove_history.side_effect = [HTTPError(response=response), None, None]

        confluence_server.remove_page_history_keep_version("123", keep_last_versions=2)

        assert mock_remove_history.call_args_list == [
            ((), {"page_id": "123", "version_number": 1}),
            ((), {"page_id": "123", "version_number": 2}),
            ((), {"page_id": "123", "version_number": 3}),
        ]

    @patch.object(ConfluenceServer, "get")
    def test_content_history_by_version_uses_supported_server_data_center_endpoint(self, mock_get, confluence_server):
        mock_get.return_value = {"number": 2}

        assert confluence_server.get_content_history_by_version_number("123", 2) == {"number": 2}
        mock_get.assert_called_once_with("content/123/version/2", params={})

    @patch.object(ConfluenceServer, "delete")
    def test_remove_content_history_uses_supported_server_data_center_endpoint(self, mock_delete, confluence_server):
        confluence_server.remove_content_history("123", 2)

        mock_delete.assert_called_once_with("content/123/version/2")

    @patch.object(ConfluenceServer, "get_content_history_by_version_number")
    def test_get_page_version_contributors_returns_collaborative_authors(self, mock_get_version, confluence_server):
        collaborators = [{"accountId": "first"}, {"accountId": "second"}]
        mock_get_version.return_value = {"collaborators": {"users": collaborators}}

        assert confluence_server.get_page_version_contributors("123", 2) == collaborators
        mock_get_version.assert_called_once_with("123", 2, expand="collaborators")

    @patch.object(ConfluenceServer, "get_content_history_by_version_number")
    def test_get_page_version_contributors_falls_back_to_saving_author(self, mock_get_version, confluence_server):
        author = {"username": "editor"}
        mock_get_version.return_value = {"by": author}

        assert confluence_server.get_page_version_contributors("123", 2) == [author]

    @patch.object(ConfluenceServer, "_get_paged")
    def test_iter_cql_follows_all_result_pages(self, mock_get_paged, confluence_server):
        mock_get_paged.return_value = iter([{"id": "1"}, {"id": "2"}])

        assert list(confluence_server.iter_cql("type=page", limit=250)) == [{"id": "1"}, {"id": "2"}]
        mock_get_paged.assert_called_once_with("rest/api/search", params={"start": 0, "limit": 250, "cql": "type=page"})

    @patch.object(ConfluenceServer, "iter_cql")
    def test_cql_all_materializes_iter_cql_results(self, mock_iter_cql, confluence_server):
        mock_iter_cql.return_value = iter([{"id": "1"}, {"id": "2"}])

        assert confluence_server.cql_all("type=page") == [{"id": "1"}, {"id": "2"}]
        mock_iter_cql.assert_called_once_with("type=page")

    @patch.object(ConfluenceServer, "create_page")
    @patch.object(ConfluenceServer, "page_exists", return_value=False)
    def test_update_or_create_creates_top_level_page_with_explicit_space(
        self, mock_page_exists, mock_create_page, confluence_server
    ):
        mock_create_page.return_value = {"id": "123", "_links": {"tinyui": "/x/abc"}}

        result = confluence_server.update_or_create(title="Top level", body="<p>Body</p>", space="TEAM")

        assert result["id"] == "123"
        mock_page_exists.assert_called_once_with("TEAM", "Top level")
        mock_create_page.assert_called_once_with(
            space="TEAM",
            parent_id=None,
            title="Top level",
            body="<p>Body</p>",
            representation="storage",
            editor=None,
            full_width=False,
        )

    @patch.object(ConfluenceServer, "create_page")
    @patch.object(ConfluenceServer, "page_exists", return_value=False)
    def test_update_or_create_passes_version_comment_when_creating(
        self, mock_page_exists, mock_create_page, confluence_server
    ):
        mock_create_page.return_value = {"id": "123", "_links": {"tinyui": "/x/abc"}}

        confluence_server.update_or_create(
            title="Top level", body="<p>Body</p>", space="TEAM", version_comment="Initial import"
        )

        assert mock_create_page.call_args.kwargs["version_comment"] == "Initial import"

    def test_update_or_create_requires_space_for_a_top_level_page(self, confluence_server):
        with pytest.raises(ApiValueError, match="space is required"):
            confluence_server.update_or_create(title="Top level", body="<p>Body</p>")

    @patch.object(ConfluenceServer, "create_page")
    @patch.object(ConfluenceServer, "page_exists")
    @patch.object(ConfluenceServer, "get_descendant_page_id", return_value="")
    def test_update_or_create_creates_when_same_title_is_under_another_parent(
        self, mock_descendant_id, mock_page_exists, mock_create_page, confluence_server
    ):
        mock_create_page.return_value = {"id": "new", "_links": {"tinyui": "/x/new"}}

        confluence_server.update_or_create("parent-a", "Report", "<p>Body</p>", space="TEAM")

        mock_descendant_id.assert_called_once_with("TEAM", "parent-a", "Report")
        mock_page_exists.assert_not_called()
        mock_create_page.assert_called_once_with(
            space="TEAM",
            parent_id="parent-a",
            title="Report",
            body="<p>Body</p>",
            representation="storage",
            editor=None,
            full_width=False,
        )

    @patch.object(ConfluenceServer, "update_page")
    @patch.object(ConfluenceServer, "page_exists")
    @patch.object(ConfluenceServer, "get_descendant_page_id", return_value="child-a")
    def test_update_or_create_updates_only_the_matching_child(
        self, mock_descendant_id, mock_page_exists, mock_update_page, confluence_server
    ):
        mock_update_page.return_value = {"id": "child-a", "_links": {"tinyui": "/x/child"}}

        confluence_server.update_or_create("parent-a", "Report", "<p>Body</p>", space="TEAM")

        mock_descendant_id.assert_called_once_with("TEAM", "parent-a", "Report")
        mock_page_exists.assert_not_called()
        mock_update_page.assert_called_once_with(
            parent_id="parent-a",
            page_id="child-a",
            title="Report",
            body="<p>Body</p>",
            representation="storage",
            minor_edit=False,
            version_comment=None,
            full_width=False,
        )

    @patch.object(ConfluenceServer, "update_page")
    def test_update_existing_page_preserves_confluence_image_storage_markup(self, mock_update_page, confluence_server):
        body = '<table><tr><td><ac:image><ri:attachment ri:filename="chart.png" /></ac:image></td></tr></table>'
        mock_update_page.return_value = {"id": "123"}

        result = confluence_server.update_existing_page("123", "Report", body)

        assert result == {"id": "123"}
        assert mock_update_page.call_args.kwargs["body"] == body

    @patch.object(ConfluenceServer, "_get_paged")
    def test_get_page_properties_follows_every_result_page(self, mock_get_paged, confluence_server):
        mock_get_paged.return_value = iter([{"key": "one"}, {"key": "two"}])

        assert confluence_server.get_page_properties("123", limit=50, expand="version") == [
            {"key": "one"},
            {"key": "two"},
        ]
        mock_get_paged.assert_called_once_with("content/123/property", params={"limit": 50, "expand": "version"})

    def test_get_page_properties_rejects_non_positive_limit(self, confluence_server):
        with pytest.raises(ValueError, match="limit must be greater than zero"):
            confluence_server.get_page_properties("123", limit=0)

    # Content Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_content(self, mock_get, confluence_server):
        """Test get_content method."""
        mock_get.return_value = {"id": "123", "title": "Test Page", "type": "page"}
        result = confluence_server.get_content("123")
        mock_get.assert_called_once_with("content/123", **{})
        assert result == {"id": "123", "title": "Test Page", "type": "page"}

    @patch.object(ConfluenceServer, "get")
    def test_get_content_by_type(self, mock_get, confluence_server):
        """Test get_content_by_type method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Test Page"}]}
        result = confluence_server.get_content_by_type("page")
        mock_get.assert_called_once_with("content", params={"type": "page", **{}})
        assert result == {"results": [{"id": "123", "title": "Test Page"}]}

    @patch.object(ConfluenceServer, "post")
    def test_create_content(self, mock_post, confluence_server):
        """Test create_content method."""
        content_data = {"title": "New Page", "type": "page", "space": {"key": "TEST"}}
        mock_post.return_value = {"id": "456", "title": "New Page", "type": "page"}
        result = confluence_server.create_content(content_data)
        mock_post.assert_called_once_with("content", data=content_data, **{})
        assert result == {"id": "456", "title": "New Page", "type": "page"}

    @patch.object(ConfluenceServer, "put")
    def test_update_content(self, mock_put, confluence_server):
        """Test update_content method."""
        content_data = {"title": "Updated Page"}
        mock_put.return_value = {"id": "123", "title": "Updated Page"}
        result = confluence_server.update_content("123", content_data)
        mock_put.assert_called_once_with("content/123", data=content_data, **{})
        assert result == {"id": "123", "title": "Updated Page"}

    @patch.object(ConfluenceServer, "delete")
    def test_delete_content(self, mock_delete, confluence_server):
        """Test delete_content method."""
        mock_delete.return_value = {"success": True}
        result = confluence_server.delete_content("123")
        mock_delete.assert_called_once_with("content/123", **{})
        assert result == {"success": True}

    @patch.object(ConfluenceServer, "get")
    def test_get_content_children(self, mock_get, confluence_server):
        """Test get_content_children method."""
        mock_get.return_value = {"results": [{"id": "789", "title": "Child Page"}]}
        result = confluence_server.get_content_children("123")
        mock_get.assert_called_once_with("content/123/child", **{})
        assert result == {"results": [{"id": "789", "title": "Child Page"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_content_descendants(self, mock_get, confluence_server):
        """Test get_content_descendants method."""
        mock_get.return_value = {"results": [{"id": "999", "title": "Descendant Page"}]}
        result = confluence_server.get_content_descendants("123")
        mock_get.assert_called_once_with("content/123/descendant", **{})
        assert result == {"results": [{"id": "999", "title": "Descendant Page"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_content_ancestors(self, mock_get, confluence_server):
        """Test get_content_ancestors method."""
        mock_get.return_value = {"results": [{"id": "111", "title": "Ancestor Page"}]}
        result = confluence_server.get_content_ancestors("123")
        mock_get.assert_called_once_with("content/123/ancestor", **{})
        assert result == {"results": [{"id": "111", "title": "Ancestor Page"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_content_by_title(self, mock_get, confluence_server):
        """Test get_content_by_title method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Test Page"}]}
        result = confluence_server.get_content_by_title("TEST", "Test Page")
        mock_get.assert_called_once_with("content", params={"spaceKey": "TEST", "title": "Test Page", **{}})
        assert result == {"results": [{"id": "123", "title": "Test Page"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_content_by_id(self, mock_get, confluence_server):
        """Test get_content_by_id method."""
        mock_get.return_value = {"id": "123", "title": "Test Page"}
        result = confluence_server.get_content_by_id("123")
        mock_get.assert_called_once_with("content/123", **{})
        assert result == {"id": "123", "title": "Test Page"}

    @patch.object(ConfluenceServer, "get")
    def test_get_all_pages_from_space(self, mock_get, confluence_server):
        """Test get_all_pages_from_space method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Page in Space"}]}
        result = confluence_server.get_all_pages_from_space("TEST")
        assert list(result) == [{"id": "123", "title": "Page in Space"}]
        mock_get.assert_called_once_with(
            "content",
            params={"spaceKey": "TEST", "type": "page", **{}},
            trailing=None,
            data=None,
            flags=None,
            absolute=False,
        )

    # Pagination Tests for _get_paged (fix for issue #1598)
    @patch.object(ConfluenceServer, "get")
    def test_pagination_with_next_link_as_string(self, mock_get, confluence_server):
        """Test multi-page pagination when _links.next is a string URL."""
        mock_get.side_effect = [
            {
                "results": [{"id": "1", "title": "Page 1"}],
                "_links": {"next": "https://test.confluence.com/rest/api/1.0/content?start=1"},
            },
            {
                "results": [{"id": "2", "title": "Page 2"}],
            },
        ]
        result = list(confluence_server.get_all_pages_from_space("TEST"))
        assert result == [{"id": "1", "title": "Page 1"}, {"id": "2", "title": "Page 2"}]
        assert mock_get.call_count == 2

    @patch.object(ConfluenceServer, "get")
    def test_pagination_with_next_link_as_dict(self, mock_get, confluence_server):
        """Test multi-page pagination when _links.next is a dict with href."""
        mock_get.side_effect = [
            {
                "results": [{"id": "1", "title": "Page 1"}],
                "_links": {"next": {"href": "https://test.confluence.com/rest/api/1.0/content?start=1"}},
            },
            {
                "results": [{"id": "2", "title": "Page 2"}],
            },
        ]
        result = list(confluence_server.get_all_pages_from_space("TEST"))
        assert result == [{"id": "1", "title": "Page 1"}, {"id": "2", "title": "Page 2"}]
        assert mock_get.call_count == 2

    @patch.object(ConfluenceServer, "get")
    def test_child_page_pagination_resolves_relative_next_link_without_leading_slash(self, mock_get, confluence_server):
        mock_get.side_effect = [
            {
                "results": [{"id": "1", "title": "Child 1"}],
                "_links": {"next": "rest/api/content/123/child/page?limit=25&start=25"},
            },
            {"results": [{"id": "2", "title": "Child 2"}]},
        ]

        result = list(confluence_server.get_page_child_by_type("123"))

        assert result == [{"id": "1", "title": "Child 1"}, {"id": "2", "title": "Child 2"}]
        second_call = mock_get.call_args_list[1]
        assert second_call.args[0] == "https://test.confluence.com/rest/api/content/123/child/page?limit=25&start=25"
        assert second_call.kwargs["absolute"] is True

    @patch.object(ConfluenceServer, "get")
    def test_pagination_stops_when_next_link_is_none(self, mock_get, confluence_server):
        """Test pagination stops when _links.next is explicitly None."""
        mock_get.return_value = {
            "results": [{"id": "1", "title": "Page 1"}],
            "_links": {"next": None},
        }
        result = list(confluence_server.get_all_pages_from_space("TEST"))
        assert result == [{"id": "1", "title": "Page 1"}]
        assert mock_get.call_count == 1

    @patch.object(ConfluenceServer, "get")
    def test_pagination_stops_when_next_link_dict_missing_href(self, mock_get, confluence_server):
        """Test pagination stops when _links.next is a dict without href."""
        mock_get.return_value = {
            "results": [{"id": "1", "title": "Page 1"}],
            "_links": {"next": {}},
        }
        result = list(confluence_server.get_all_pages_from_space("TEST"))
        assert result == [{"id": "1", "title": "Page 1"}]
        assert mock_get.call_count == 1

    @patch.object(ConfluenceServer, "get")
    def test_pagination_returns_empty_when_no_results_key(self, mock_get, confluence_server):
        """Test _get_paged returns immediately when response has no results key."""
        mock_get.return_value = {"error": "something went wrong"}
        result = list(confluence_server.get_all_pages_from_space("TEST"))
        assert result == []
        assert mock_get.call_count == 1

    @patch.object(ConfluenceServer, "get")
    def test_get_all_blog_posts_from_space(self, mock_get, confluence_server):
        """Test get_all_blog_posts_from_space method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Blog Post in Space"}]}
        result = confluence_server.get_all_blog_posts_from_space("TEST")
        assert list(result) == [{"id": "456", "title": "Blog Post in Space"}]
        mock_get.assert_called_once_with(
            "content",
            params={"spaceKey": "TEST", "type": "blogpost", **{}},
            trailing=None,
            data=None,
            flags=None,
            absolute=False,
        )

    @patch.object(ConfluenceServer, "get")
    def test_get_page_by_title(self, mock_get, confluence_server):
        """Test get_page_by_title method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Test Page"}]}
        result = confluence_server.get_page_by_title("TEST", "Test Page")
        mock_get.assert_called_once_with(
            "content", params={"spaceKey": "TEST", "title": "Test Page", "type": "page", **{}}
        )
        assert result == {"results": [{"id": "123", "title": "Test Page"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_blog_post_by_title(self, mock_get, confluence_server):
        """Test get_blog_post_by_title method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Test Blog Post"}]}
        result = confluence_server.get_blog_post_by_title("TEST", "Test Blog Post")
        mock_get.assert_called_once_with(
            "content", params={"spaceKey": "TEST", "title": "Test Blog Post", "type": "blogpost", **{}}
        )
        assert result == {"results": [{"id": "456", "title": "Test Blog Post"}]}

    @patch.object(ConfluenceServer, "get")
    def test_page_exists(self, mock_get, confluence_server):
        """Test page_exists method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Test Page"}]}
        result = confluence_server.page_exists("TEST", "Test Page")
        assert result is True

    @patch.object(ConfluenceServer, "get")
    def test_page_exists_false(self, mock_get, confluence_server):
        """Test page_exists method when page doesn't exist."""
        mock_get.return_value = {"results": []}
        result = confluence_server.page_exists("TEST", "Non-existent Page")
        assert result is False

    @patch.object(ConfluenceServer, "get")
    def test_blog_post_exists(self, mock_get, confluence_server):
        """Test blog_post_exists method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Test Blog Post"}]}
        result = confluence_server.blog_post_exists("TEST", "Test Blog Post")
        assert result is True

    @patch.object(ConfluenceServer, "get")
    def test_blog_post_exists_false(self, mock_get, confluence_server):
        """Test blog_post_exists method when blog post doesn't exist."""
        mock_get.return_value = {"results": []}
        result = confluence_server.blog_post_exists("TEST", "Non-existent Blog Post")
        assert result is False

    @patch.object(ConfluenceServer, "get")
    def test_get_content_id_page(self, mock_get, confluence_server):
        """Test get_content_id method for page."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Test Page"}]}
        result = confluence_server.get_content_id("TEST", "Test Page", "page")
        assert result == "123"

    @patch.object(ConfluenceServer, "get")
    def test_get_content_id_blogpost(self, mock_get, confluence_server):
        """Test get_content_id method for blog post."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Test Blog Post"}]}
        result = confluence_server.get_content_id("TEST", "Test Blog Post", "blogpost")
        assert result == "456"

    def test_get_content_id_invalid_type(self, confluence_server):
        """Test get_content_id method with invalid content type."""
        with pytest.raises(ValueError, match="content_type must be 'page' or 'blogpost'"):
            confluence_server.get_content_id("TEST", "Test", "invalid")

    @patch.object(ConfluenceServer, "get")
    def test_get_page_space(self, mock_get, confluence_server):
        """Test get_page_space method."""
        mock_get.return_value = {"space": {"key": "TEST"}}
        result = confluence_server.get_page_space("123")
        mock_get.assert_called_once_with("content/123", params={"expand": "space"})
        assert result == "TEST"

    def test_get_page_space_uses_expand_query_param(self, confluence_server):
        """get_page_space must pass expand via params so AtlassianRestAPI.get() accepts the call."""
        response = Response()
        response.status_code = 200
        response.reason = "OK"
        response._content = b'{"space": {"key": "TEST"}}'

        with patch.object(confluence_server._session, "request", return_value=response) as mock_request:
            result = confluence_server.get_page_space("123")

        assert result == "TEST"
        url = mock_request.call_args.kwargs["url"]
        params = mock_request.call_args.kwargs.get("params") or {}
        assert url.startswith("https://test.confluence.com/rest/api/content/123")
        expand = params.get("expand") if isinstance(params, dict) else None
        assert expand == "space" or "expand=space" in url

    @patch.object(ConfluenceServer, "get")
    def test_get_page_space_no_space(self, mock_get, confluence_server):
        """Test get_page_space returns None when page has no space."""
        mock_get.return_value = {"title": "Orphan Page"}
        result = confluence_server.get_page_space("456")
        mock_get.assert_called_once_with("content/456", params={"expand": "space"})
        assert result is None

    @patch.object(ConfluenceServer, "get")
    def test_get_page_space_empty_space(self, mock_get, confluence_server):
        """Test get_page_space returns None when space key is empty."""
        mock_get.return_value = {"space": {}}
        result = confluence_server.get_page_space("789")
        mock_get.assert_called_once_with("content/789", params={"expand": "space"})
        assert result is None

    # Space Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_spaces(self, mock_get, confluence_server):
        """Test get_spaces method."""
        mock_get.return_value = {"results": [{"key": "TEST", "name": "Test Space"}]}
        result = confluence_server.get_spaces()
        mock_get.assert_called_once_with("space", **{})
        assert result == {"results": [{"key": "TEST", "name": "Test Space"}]}

    @patch.object(ConfluenceServer, "get_all_spaces")
    def test_get_space_names_paginates(self, mock_get_all_spaces, confluence_server):
        mock_get_all_spaces.side_effect = [
            {"results": [{"name": "Engineering"}, {"name": "Operations"}], "totalSize": 3},
            {"results": [{"name": "Support"}], "totalSize": 3},
        ]

        assert confluence_server.get_space_names(limit=2) == ["Engineering", "Operations", "Support"]
        assert mock_get_all_spaces.call_args_list[1].kwargs["start"] == 2

    @patch.object(ConfluenceServer, "get")
    def test_get_space(self, mock_get, confluence_server):
        """Test get_space method."""
        mock_get.return_value = {"key": "TEST", "name": "Test Space"}
        result = confluence_server.get_space("TEST")
        mock_get.assert_called_once_with(
            "space/TEST",
        )
        assert result == {"key": "TEST", "name": "Test Space"}

    @patch.object(ConfluenceServer, "post")
    def test_create_space(self, mock_post, confluence_server):
        """Test create_space method."""
        space_data = {"name": "New Space", "key": "NEW"}
        mock_post.return_value = {"key": "NEW", "name": "New Space"}
        result = confluence_server.create_space(space_data)
        mock_post.assert_called_once_with("space", data=space_data, **{})
        assert result == {"key": "NEW", "name": "New Space"}

    @patch.object(ConfluenceServer, "put")
    def test_update_space(self, mock_put, confluence_server):
        """Test update_space method."""
        space_data = {"name": "Updated Space"}
        mock_put.return_value = {"key": "TEST", "name": "Updated Space"}
        result = confluence_server.update_space("TEST", space_data)
        mock_put.assert_called_once_with("space/TEST", data=space_data, **{})
        assert result == {"key": "TEST", "name": "Updated Space"}

    @patch.object(ConfluenceServer, "delete")
    def test_delete_space(self, mock_delete, confluence_server):
        """Test delete_space method."""
        mock_delete.return_value = {"success": True}
        result = confluence_server.delete_space("TEST")
        mock_delete.assert_called_once_with("space/TEST", **{})
        assert result == {"success": True}

    @patch.object(ConfluenceServer, "delete")
    def test_delete_missing_space_raises_api_not_found_error(self, mock_delete, confluence_server):
        response = Response()
        response.status_code = 404
        mock_delete.side_effect = HTTPError(response=response)

        with pytest.raises(ApiNotFoundError, match="There is no space with the given key"):
            confluence_server.delete_space("MISSING")

    @patch.object(ConfluenceServer, "get")
    def test_get_space_content(self, mock_get, confluence_server):
        """Test get_space_content method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Page in Space"}]}
        result = confluence_server.get_space_content("TEST")
        mock_get.assert_called_once_with("content", params={"spaceKey": "TEST", **{}})
        assert result == {"results": [{"id": "123", "title": "Page in Space"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_space_permissions(self, mock_get, confluence_server):
        """Test get_space_permissions method."""
        mock_get.return_value = {"results": [{"userName": "test", "permission": "ADMIN"}]}
        result = confluence_server.get_space_permissions("TEST")
        mock_get.assert_called_once_with("space/TEST/permission", **{})
        assert result == {"results": [{"userName": "test", "permission": "ADMIN"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_space_settings(self, mock_get, confluence_server):
        """Test get_space_settings method."""
        mock_get.return_value = {"settings": {"key": "value"}}
        result = confluence_server.get_space_settings("TEST")
        mock_get.assert_called_once_with("space/TEST/settings", **{})
        assert result == {"settings": {"key": "value"}}

    # User Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_users(self, mock_get, confluence_server):
        """Test get_users method."""
        mock_get.return_value = {"results": [{"username": "user1", "displayName": "Test User"}]}
        result = confluence_server.get_users()
        mock_get.assert_called_once_with("user", **{})
        assert result == {"results": [{"username": "user1", "displayName": "Test User"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_user(self, mock_get, confluence_server):
        """Test get_user method."""
        mock_get.return_value = {"username": "user1", "displayName": "Test User"}
        result = confluence_server.get_user("user1")
        mock_get.assert_called_once_with("user", params={"username": "user1", **{}})
        assert result == {"username": "user1", "displayName": "Test User"}

    @patch.object(ConfluenceServer, "get")
    def test_get_current_user(self, mock_get, confluence_server):
        """Test get_current_user method."""
        mock_get.return_value = {"username": "current", "displayName": "Current User"}
        result = confluence_server.get_current_user()
        mock_get.assert_called_once_with("user/current", **{})
        assert result == {"username": "current", "displayName": "Current User"}

    @patch.object(ConfluenceServer, "get")
    def test_get_user_by_key(self, mock_get, confluence_server):
        """Test get_user_by_key method."""
        mock_get.return_value = {"username": "user1", "displayName": "Test User"}
        result = confluence_server.get_user_by_key("user1")
        mock_get.assert_called_once_with("user", params={"key": "user1", **{}})
        assert result == {"username": "user1", "displayName": "Test User"}

    # Group Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_groups(self, mock_get, confluence_server):
        """Test get_groups method."""
        mock_get.return_value = {"results": [{"name": "group1", "type": "group"}]}
        result = confluence_server.get_groups()
        mock_get.assert_called_once_with("group", **{})
        assert result == {"results": [{"name": "group1", "type": "group"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_group(self, mock_get, confluence_server):
        """Test get_group method."""
        mock_get.return_value = {"name": "group1", "type": "group"}
        result = confluence_server.get_group("group1")
        mock_get.assert_called_once_with("group", params={"groupname": "group1", **{}})
        assert result == {"name": "group1", "type": "group"}

    @patch.object(ConfluenceServer, "get")
    def test_get_group_members(self, mock_get, confluence_server):
        """Test get_group_members method."""
        mock_get.return_value = {"results": [{"username": "user1", "displayName": "Test User"}]}
        result = confluence_server.get_group_members("group1")
        mock_get.assert_called_once_with("group/group1/member", **{})
        assert result == {"results": [{"username": "user1", "displayName": "Test User"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_group_members_warns_when_confluence_caps_limit(self, mock_get, confluence_server):
        mock_get.return_value = {"results": [], "limit": 200}

        with pytest.warns(UserWarning, match="capped get_group_members limit from 1000 to 200"):
            confluence_server.get_group_members("group1", limit=1000)

    @patch.object(ConfluenceServer, "get_group_members")
    def test_get_all_members_uses_returned_page_size_and_total_count(self, mock_get_group_members, confluence_server):
        mock_get_group_members.side_effect = [
            {"results": [{"username": "one"}, {"username": "two"}], "limit": 2, "totalCount": 3},
            {"results": [{"username": "three"}], "limit": 2, "totalCount": 3},
        ]

        assert confluence_server.get_all_members("group1") == [
            {"username": "one"},
            {"username": "two"},
            {"username": "three"},
        ]
        assert mock_get_group_members.call_args_list[1].kwargs["start"] == 2

    @patch.object(ConfluenceServer, "post")
    def test_add_user_to_group(self, mock_post, confluence_server):
        """Test add_user_to_group method."""
        mock_post.return_value = {"success": True}
        result = confluence_server.add_user_to_group("group1", "user1")
        mock_post.assert_called_once_with("group/group1/member", data={"name": "user1"}, **{})
        assert result == {"success": True}

    @patch.object(ConfluenceServer, "delete")
    def test_remove_user_from_group(self, mock_delete, confluence_server):
        """Test remove_user_from_group method."""
        mock_delete.return_value = {"success": True}
        result = confluence_server.remove_user_from_group("group1", "user1")
        mock_delete.assert_called_once_with("group/group1/member/user1", **{})
        assert result == {"success": True}

    # Label Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_labels(self, mock_get, confluence_server):
        """Test get_labels method."""
        mock_get.return_value = {"results": [{"name": "label1", "id": "1"}]}
        result = confluence_server.get_labels()
        mock_get.assert_called_once_with("label", **{})
        assert result == {"results": [{"name": "label1", "id": "1"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_content_labels(self, mock_get, confluence_server):
        """Test get_content_labels method."""
        mock_get.return_value = {"results": [{"name": "label1", "id": "1"}]}
        result = confluence_server.get_content_labels("123")
        mock_get.assert_called_once_with("content/123/label", **{})
        assert result == {"results": [{"name": "label1", "id": "1"}]}

    @patch.object(ConfluenceServer, "post")
    def test_add_content_labels(self, mock_post, confluence_server):
        """Test add_content_labels method."""
        label_data = {"name": "New Label"}
        mock_post.return_value = {"name": "New Label", "id": "2"}
        result = confluence_server.add_content_labels("123", label_data)
        mock_post.assert_called_once_with("content/123/label", data=label_data, **{})
        assert result == {"name": "New Label", "id": "2"}

    @patch.object(ConfluenceServer, "delete")
    def test_remove_content_label(self, mock_delete, confluence_server):
        """Test remove_content_label method."""
        mock_delete.return_value = {"success": True}
        result = confluence_server.remove_content_label("123", "label1")
        mock_delete.assert_called_once_with("content/123/label/label1", **{})
        assert result == {"success": True}

    @patch.object(ConfluenceServer, "get")
    def test_get_all_pages_by_label(self, mock_get, confluence_server):
        """Test get_all_pages_by_label method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Page with Label"}]}
        result = confluence_server.get_all_pages_by_label("label1")
        assert list(result) == [{"id": "123", "title": "Page with Label"}]
        mock_get.assert_called_once_with(
            "content",
            params={"label": "label1", "type": "page", **{}},
            trailing=None,
            data=None,
            flags=None,
            absolute=False,
        )

    @patch.object(ConfluenceServer, "get")
    def test_get_all_blog_posts_by_label(self, mock_get, confluence_server):
        """Test get_all_blog_posts_by_label method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Blog Post with Label"}]}
        result = confluence_server.get_all_blog_posts_by_label("label1")
        assert list(result) == [{"id": "456", "title": "Blog Post with Label"}]
        mock_get.assert_called_once_with(
            "content",
            params={"label": "label1", "type": "blogpost", **{}},
            trailing=None,
            data=None,
            flags=None,
            absolute=False,
        )

    # Attachment Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_attachments(self, mock_get, confluence_server):
        """Test get_attachments method."""
        mock_get.return_value = {"results": [{"id": "att1", "title": "Test Attachment"}]}
        result = confluence_server.get_attachments("123")
        mock_get.assert_called_once_with("content/123/child/attachment", **{})
        assert result == {"results": [{"id": "att1", "title": "Test Attachment"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_attachment(self, mock_get, confluence_server):
        """Test get_attachment method."""
        mock_get.return_value = {"id": "att1", "title": "Test Attachment"}
        result = confluence_server.get_attachment("att1")
        mock_get.assert_called_once_with("content/att1", **{})
        assert result == {"id": "att1", "title": "Test Attachment"}

    @patch.object(ConfluenceServer, "post")
    def test_create_attachment(self, mock_post, confluence_server):
        """Test create_attachment method."""
        attachment_data = {"title": "New Attachment"}
        mock_post.return_value = {"id": "att2", "title": "New Attachment"}
        result = confluence_server.create_attachment("123", attachment_data)
        mock_post.assert_called_once_with("content/123/child/attachment", data=attachment_data, **{})
        assert result == {"id": "att2", "title": "New Attachment"}

    @patch.object(ConfluenceServer, "put")
    def test_update_attachment(self, mock_put, confluence_server):
        """Test update_attachment method."""
        attachment_data = {"title": "Updated Attachment"}
        mock_put.return_value = {"id": "att1", "title": "Updated Attachment"}
        result = confluence_server.update_attachment("att1", attachment_data)
        mock_put.assert_called_once_with("content/att1", data=attachment_data, **{})
        assert result == {"id": "att1", "title": "Updated Attachment"}

    @patch.object(ConfluenceServer, "delete")
    def test_delete_attachment(self, mock_delete, confluence_server):
        """Test delete_attachment method."""
        mock_delete.return_value = {"success": True}
        result = confluence_server.delete_attachment("att1")
        mock_delete.assert_called_once_with("content/att1", **{})
        assert result == {"success": True}

    @patch.object(ConfluenceServer, "get")
    def test_download_attachment(self, mock_get, confluence_server):
        """Test download_attachment method."""
        mock_get.return_value = b"attachment_content"
        result = confluence_server.download_attachment("att1")
        mock_get.assert_called_once_with("content/att1/download", **{})
        assert result == b"attachment_content"

    @patch.object(ConfluenceServer, "get")
    @patch.object(ConfluenceServer, "get_attachments_from_content")
    def test_download_cloud_attachment_uses_content_attachment_endpoint(
        self, mock_get_attachments, mock_get, confluence_server
    ):
        """Cloud downloads must not use the deprecated ``_links.download`` URL."""
        confluence_server.cloud = True
        mock_get_attachments.return_value = {
            "results": [
                {
                    "id": "att123",
                    "title": "report.pdf",
                    "_links": {"download": "/download/attachments/123/att123"},
                }
            ]
        }
        mock_get.return_value = b"attachment_content"

        result = confluence_server.download_attachments_from_page("123", filename="report.pdf", to_memory=True)

        mock_get.assert_called_once_with(
            "rest/api/content/123/child/attachment/att123/download", not_json_response=True
        )
        assert result["report.pdf"].read() == b"attachment_content"

    @patch.object(ConfluenceServer, "get_attachments_from_content")
    def test_download_attachments_returns_empty_result_when_no_attachments(
        self, mock_get_attachments, confluence_server
    ):
        mock_get_attachments.return_value = {"results": []}

        assert confluence_server.download_attachments_from_page("123", to_memory=True) == {}
        assert confluence_server.download_attachments_from_page("123", path="/tmp") == {
            "attachments_downloaded": 0,
            "path": "/tmp",
        }

    @patch.object(ConfluenceServer, "get")
    @patch.object(ConfluenceServer, "get_attachments_from_content")
    def test_download_attachments_fetches_all_attachment_pages(self, mock_get_attachments, mock_get, confluence_server):
        mock_get_attachments.side_effect = [
            {
                "results": [
                    {"id": "att1", "title": "first.txt", "_links": {"download": "download/first"}},
                    {"id": "att2", "title": "second.txt", "_links": {"download": "download/second"}},
                ],
                "totalSize": 3,
            },
            {
                "results": [{"id": "att3", "title": "third.txt", "_links": {"download": "download/third"}}],
                "totalSize": 3,
            },
        ]
        mock_get.return_value = b"attachment_content"

        result = confluence_server.download_attachments_from_page("123", limit=2, to_memory=True)

        assert list(result) == ["first.txt", "second.txt", "third.txt"]
        assert mock_get_attachments.call_args_list[0].kwargs == {"page_id": "123", "start": 0, "limit": 2}
        assert mock_get_attachments.call_args_list[1].kwargs == {"page_id": "123", "start": 2, "limit": 2}

    # Comment Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_page_comments_expands_body_and_author_metadata(self, mock_get, confluence_server):
        mock_get.return_value = {
            "results": [
                {
                    "body": {"view": {"value": "<p>Comment</p>"}},
                    "history": {"createdBy": {"username": "author"}},
                    "version": {"by": {"username": "editor"}},
                }
            ]
        }

        result = confluence_server.get_page_comments("123", expand="body.view,history,version", limit=100)

        assert result["results"][0]["history"]["createdBy"]["username"] == "author"
        mock_get.assert_called_once_with(
            "rest/api/content/123/child/comment",
            params={"id": "123", "start": 0, "limit": 100, "expand": "body.view,history,version"},
        )

    @patch.object(ConfluenceServer, "get")
    def test_get_comments(self, mock_get, confluence_server):
        """Test get_comments method."""
        mock_get.return_value = {"results": [{"id": "comment1", "text": "Test Comment"}]}
        result = confluence_server.get_comments("123")
        mock_get.assert_called_once_with("content/123/child/comment", **{})
        assert result == {"results": [{"id": "comment1", "text": "Test Comment"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_comment(self, mock_get, confluence_server):
        """Test get_comment method."""
        mock_get.return_value = {"id": "comment1", "text": "Test Comment"}
        result = confluence_server.get_comment("comment1")
        mock_get.assert_called_once_with("content/comment1", **{})
        assert result == {"id": "comment1", "text": "Test Comment"}

    @patch.object(ConfluenceServer, "post")
    def test_create_comment(self, mock_post, confluence_server):
        """Test create_comment method."""
        comment_data = {"text": "New Comment"}
        mock_post.return_value = {"id": "comment2", "text": "New Comment"}
        result = confluence_server.create_comment("123", comment_data)
        mock_post.assert_called_once_with("content/123/child/comment", data=comment_data, **{})
        assert result == {"id": "comment2", "text": "New Comment"}

    @patch.object(ConfluenceServer, "put")
    def test_update_comment(self, mock_put, confluence_server):
        """Test update_comment method."""
        comment_data = {"text": "Updated Comment"}
        mock_put.return_value = {"id": "comment1", "text": "Updated Comment"}
        result = confluence_server.update_comment("comment1", comment_data)
        mock_put.assert_called_once_with("content/comment1", data=comment_data, **{})
        assert result == {"id": "comment1", "text": "Updated Comment"}

    @patch.object(ConfluenceServer, "delete")
    def test_delete_comment(self, mock_delete, confluence_server):
        """Test delete_comment method."""
        mock_delete.return_value = {"success": True}
        result = confluence_server.delete_comment("comment1")
        mock_delete.assert_called_once_with("content/comment1", **{})
        assert result == {"success": True}

    # Search Tests
    @patch.object(ConfluenceServer, "get")
    def test_search_content(self, mock_get, confluence_server):
        """Test search_content method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Search Result"}]}
        result = confluence_server.search_content("type=page")
        mock_get.assert_called_once_with("content/search", params={"cql": "type=page", **{}})
        assert result == {"results": [{"id": "123", "title": "Search Result"}]}

    @patch.object(ConfluenceServer, "get")
    def test_search_spaces(self, mock_get, confluence_server):
        """Test search_spaces method."""
        mock_get.return_value = {"results": [{"key": "TEST", "name": "Test Space"}]}
        result = confluence_server.search_spaces("test")
        mock_get.assert_called_once_with("space/search", params={"query": "test", **{}})
        assert result == {"results": [{"key": "TEST", "name": "Test Space"}]}

    # Page Properties Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_content_properties(self, mock_get, confluence_server):
        """Test get_content_properties method."""
        mock_get.return_value = {"results": [{"key": "prop1", "value": "value1"}]}
        result = confluence_server.get_content_properties("123")
        mock_get.assert_called_once_with("content/123/property", **{})
        assert result == {"results": [{"key": "prop1", "value": "value1"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_content_property(self, mock_get, confluence_server):
        """Test get_content_property method."""
        mock_get.return_value = {"key": "prop1", "value": "value1"}
        result = confluence_server.get_content_property("123", "prop1")
        mock_get.assert_called_once_with("content/123/property/prop1", **{})
        assert result == {"key": "prop1", "value": "value1"}

    @patch.object(ConfluenceServer, "post")
    def test_create_content_property(self, mock_post, confluence_server):
        """Test create_content_property method."""
        property_data = {"key": "prop2", "value": "value2"}
        mock_post.return_value = {"key": "prop2", "value": "value2"}
        result = confluence_server.create_content_property("123", property_data)
        mock_post.assert_called_once_with("content/123/property", data=property_data, **{})
        assert result == {"key": "prop2", "value": "value2"}

    @patch.object(ConfluenceServer, "put")
    def test_update_content_property(self, mock_put, confluence_server):
        """Test update_content_property method."""
        property_data = {"value": "updated_value"}
        mock_put.return_value = {"key": "prop1", "value": "updated_value"}
        result = confluence_server.update_content_property("123", "prop1", property_data)
        mock_put.assert_called_once_with("content/123/property/prop1", data=property_data, **{})
        assert result == {"key": "prop1", "value": "updated_value"}

    @patch.object(ConfluenceServer, "delete")
    def test_delete_content_property(self, mock_delete, confluence_server):
        """Test delete_content_property method."""
        mock_delete.return_value = {"success": True}
        result = confluence_server.delete_content_property("123", "prop1")
        mock_delete.assert_called_once_with("content/123/property/prop1", **{})
        assert result == {"success": True}

    # Template Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_templates(self, mock_get, confluence_server):
        """Test get_templates method."""
        mock_get.return_value = {"results": [{"id": "template1", "name": "Test Template"}]}
        result = confluence_server.get_templates()
        mock_get.assert_called_once_with("template", **{})
        assert result == {"results": [{"id": "template1", "name": "Test Template"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_template(self, mock_get, confluence_server):
        """Test get_template method."""
        mock_get.return_value = {"id": "template1", "name": "Test Template"}
        result = confluence_server.get_template("template1")
        mock_get.assert_called_once_with("template/template1", **{})
        assert result == {"id": "template1", "name": "Test Template"}

    @patch.object(ConfluenceServer, "put")
    def test_update_template_sends_a_json_object_not_a_json_string(self, mock_put, confluence_server):
        body = {"storage": {"value": "<p>Template</p>", "representation": "storage"}}

        confluence_server.create_or_update_template("Template", body, template_id="template-1")

        mock_put.assert_called_once_with(
            "rest/api/template",
            data={"name": "Template", "templateType": "page", "body": body, "templateId": "template-1"},
        )

    @patch.object(ConfluenceServer, "create_page")
    @patch.object(ConfluenceServer, "get_content_template")
    def test_create_page_from_template_preserves_storage_macros(
        self, mock_get_content_template, mock_create_page, confluence_server
    ):
        mock_get_content_template.return_value = {
            "body": {"storage": {"value": "<ac:structured-macro>[[TITLE]]</ac:structured-macro>"}}
        }
        mock_create_page.return_value = {"id": "123"}

        result = confluence_server.create_page_from_template(
            "DOCS", "Report", "template-1", parent_id="42", replacements={"[[TITLE]]": "August"}, editor="v2"
        )

        assert result == {"id": "123"}
        mock_create_page.assert_called_once_with(
            "DOCS",
            "Report",
            "<ac:structured-macro>August</ac:structured-macro>",
            parent_id="42",
            representation="storage",
            editor="v2",
        )

    # Draft Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_draft_content(self, mock_get, confluence_server):
        """Test get_draft_content method."""
        mock_get.return_value = {"id": "123", "title": "Draft Page", "status": "draft"}
        result = confluence_server.get_draft_content("123")
        mock_get.assert_called_once_with("content/123", params={"status": "draft", **{}})
        assert result == {"id": "123", "title": "Draft Page", "status": "draft"}

    @patch.object(ConfluenceServer, "get")
    def test_get_all_draft_pages_from_space(self, mock_get, confluence_server):
        """Test get_all_draft_pages_from_space method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Draft Page"}]}
        result = confluence_server.get_all_draft_pages_from_space("TEST")
        assert list(result) == [{"id": "123", "title": "Draft Page"}]
        mock_get.assert_called_once_with(
            "content",
            params={"spaceKey": "TEST", "type": "page", "status": "draft", **{}},
            trailing=None,
            data=None,
            flags=None,
            absolute=False,
        )

    @patch.object(ConfluenceServer, "get")
    def test_get_all_draft_blog_posts_from_space(self, mock_get, confluence_server):
        """Test get_all_draft_blog_posts_from_space method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Draft Blog Post"}]}
        result = confluence_server.get_all_draft_blog_posts_from_space("TEST")
        assert list(result) == [{"id": "456", "title": "Draft Blog Post"}]
        mock_get.assert_called_once_with(
            "content",
            params={"spaceKey": "TEST", "type": "blogpost", "status": "draft", **{}},
            trailing=None,
            data=None,
            flags=None,
            absolute=False,
        )

    # Trash Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_trash_content(self, mock_get, confluence_server):
        """Test get_trash_content method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Trashed Page"}]}
        result = confluence_server.get_trash_content("TEST")
        assert list(result) == [{"id": "123", "title": "Trashed Page"}]
        mock_get.assert_called_once_with(
            "content",
            params={"spaceKey": "TEST", "status": "trashed", **{}},
            trailing=None,
            data=None,
            flags=None,
            absolute=False,
        )

    @patch.object(ConfluenceServer, "get")
    def test_get_all_pages_from_space_trash(self, mock_get, confluence_server):
        """Test get_all_pages_from_space_trash method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Trashed Page"}]}
        result = confluence_server.get_all_pages_from_space_trash("TEST")
        assert list(result) == [{"id": "123", "title": "Trashed Page"}]
        mock_get.assert_called_once_with(
            "content",
            params={"spaceKey": "TEST", "type": "page", "status": "trashed", **{}},
            trailing=None,
            data=None,
            flags=None,
            absolute=False,
        )

    @patch.object(ConfluenceServer, "get")
    def test_get_all_spaces_accepts_category_label_filter(self, mock_get, confluence_server):
        mock_get.return_value = {"results": []}

        confluence_server.get_all_spaces(label="service", start=0, limit=500)

        mock_get.assert_called_once_with("rest/api/space", params={"limit": 500, "label": "service"})

    @patch.object(ConfluenceServer, "get")
    def test_get_all_blog_posts_from_space_trash(self, mock_get, confluence_server):
        """Test get_all_blog_posts_from_space_trash method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Trashed Blog Post"}]}
        result = confluence_server.get_all_blog_posts_from_space_trash("TEST")
        assert list(result) == [{"id": "456", "title": "Trashed Blog Post"}]
        mock_get.assert_called_once_with(
            "content",
            params={"spaceKey": "TEST", "type": "blogpost", "status": "trashed", **{}},
            trailing=None,
            data=None,
            flags=None,
            absolute=False,
        )

    # Export Tests
    @patch.object(ConfluenceServer, "get")
    def test_export_content(self, mock_get, confluence_server):
        """Test export_content method."""
        mock_get.return_value = {"exportData": "base64_encoded_content"}
        result = confluence_server.export_content("123")
        mock_get.assert_called_once_with("content/123/export", **{})
        assert result == {"exportData": "base64_encoded_content"}

    @patch.object(ConfluenceServer, "get")
    def test_export_space(self, mock_get, confluence_server):
        """Test export_space method."""
        mock_get.return_value = {"exportData": "base64_encoded_space"}
        result = confluence_server.export_space("TEST")
        mock_get.assert_called_once_with("space/TEST/export", **{})
        assert result == {"exportData": "base64_encoded_space"}

    @patch.object(
        ConfluenceServer, "get_space_export", side_effect=["https://example.test/eng", "https://example.test/hr"]
    )
    def test_iter_space_exports_is_sequential(self, mock_get_space_export, confluence_server):
        result = list(confluence_server.iter_space_exports(["ENG", "HR"], "html"))

        assert result == [("ENG", "https://example.test/eng"), ("HR", "https://example.test/hr")]
        assert mock_get_space_export.call_args_list == [call("ENG", "html"), call("HR", "html")]

    # Utility Methods Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_metadata(self, mock_get, confluence_server):
        """Test get_metadata method."""
        mock_get.return_value = {"version": "1.0", "buildNumber": "123"}
        result = confluence_server.get_metadata()
        mock_get.assert_called_once_with("metadata", **{})
        assert result == {"version": "1.0", "buildNumber": "123"}

    @patch.object(ConfluenceServer, "get")
    def test_get_health(self, mock_get, confluence_server):
        """Test get_health method."""
        mock_get.return_value = {"status": "healthy"}
        result = confluence_server.get_health()
        mock_get.assert_called_once_with("health", **{})
        assert result == {"status": "healthy"}

    @patch.object(ConfluenceServer, "get")
    def test_get_page_as_pdf_rejects_html_response(self, mock_get, confluence_server):
        mock_get.return_value.content = b"<html>Sign in</html>"

        with pytest.raises(ApiError, match="non-PDF content"):
            confluence_server.get_page_as_pdf("123")

        mock_get.assert_called_once_with(
            "spaces/flyingpdf/pdfpageexport.action?pageId=123",
            headers=confluence_server.form_token_headers,
            advanced_mode=True,
        )

    @patch.object(ConfluenceServer, "get")
    def test_get_page_as_word_returns_legacy_export_bytes(self, mock_get, confluence_server):
        """The Word endpoint is binary data, not a DOCX conversion endpoint."""
        export = b"MIME-Version: 1.0\r\nContent-Type: multipart/related\r\n"
        mock_get.return_value = export

        result = confluence_server.get_page_as_word("123")

        assert result == export
        mock_get.assert_called_once_with(
            "exportword?pageId=123", headers=confluence_server.form_token_headers, not_json_response=True
        )

    @patch.object(ConfluenceServer, "post")
    def test_reindex(self, mock_post, confluence_server):
        """Test reindex method."""
        mock_post.return_value = {"taskId": "task123"}
        result = confluence_server.reindex()
        mock_post.assert_called_once_with("reindex", **{})
        assert result == {"taskId": "task123"}

    @patch.object(ConfluenceServer, "get")
    def test_get_reindex_progress(self, mock_get, confluence_server):
        """Test get_reindex_progress method."""
        mock_get.return_value = {"progress": 50, "status": "running"}
        result = confluence_server.get_reindex_progress()
        mock_get.assert_called_once_with("reindex", **{})
        assert result == {"progress": 50, "status": "running"}
