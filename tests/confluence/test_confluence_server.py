# coding=utf-8
"""
Test cases for Confluence Server API client.
"""

import pytest
from unittest.mock import patch

from atlassian.confluence import ConfluenceServer


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
        mock_get.assert_called_once_with("content", params={"spaceKey": "TEST", "type": "page", **{}})
        assert result == {"results": [{"id": "123", "title": "Page in Space"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_all_blog_posts_from_space(self, mock_get, confluence_server):
        """Test get_all_blog_posts_from_space method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Blog Post in Space"}]}
        result = confluence_server.get_all_blog_posts_from_space("TEST")
        mock_get.assert_called_once_with("content", params={"spaceKey": "TEST", "type": "blogpost", **{}})
        assert result == {"results": [{"id": "456", "title": "Blog Post in Space"}]}

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
        mock_get.assert_called_once_with("content/123", expand="space")
        assert result == "TEST"

    # Space Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_spaces(self, mock_get, confluence_server):
        """Test get_spaces method."""
        mock_get.return_value = {"results": [{"key": "TEST", "name": "Test Space"}]}
        result = confluence_server.get_spaces()
        mock_get.assert_called_once_with("space", **{})
        assert result == {"results": [{"key": "TEST", "name": "Test Space"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_space(self, mock_get, confluence_server):
        """Test get_space method."""
        mock_get.return_value = {"key": "TEST", "name": "Test Space"}
        result = confluence_server.get_space("TEST")
        mock_get.assert_called_once_with("space/TEST", **{})
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
        mock_get.assert_called_once_with("content", params={"label": "label1", "type": "page", **{}})
        assert result == {"results": [{"id": "123", "title": "Page with Label"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_all_blog_posts_by_label(self, mock_get, confluence_server):
        """Test get_all_blog_posts_by_label method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Blog Post with Label"}]}
        result = confluence_server.get_all_blog_posts_by_label("label1")
        mock_get.assert_called_once_with("content", params={"label": "label1", "type": "blogpost", **{}})
        assert result == {"results": [{"id": "456", "title": "Blog Post with Label"}]}

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

    # Comment Management Tests
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
        mock_get.assert_called_once_with(
            "content", params={"spaceKey": "TEST", "type": "page", "status": "draft", **{}}
        )
        assert result == {"results": [{"id": "123", "title": "Draft Page"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_all_draft_blog_posts_from_space(self, mock_get, confluence_server):
        """Test get_all_draft_blog_posts_from_space method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Draft Blog Post"}]}
        result = confluence_server.get_all_draft_blog_posts_from_space("TEST")
        mock_get.assert_called_once_with(
            "content", params={"spaceKey": "TEST", "type": "blogpost", "status": "draft", **{}}
        )
        assert result == {"results": [{"id": "456", "title": "Draft Blog Post"}]}

    # Trash Management Tests
    @patch.object(ConfluenceServer, "get")
    def test_get_trash_content(self, mock_get, confluence_server):
        """Test get_trash_content method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Trashed Page"}]}
        result = confluence_server.get_trash_content("TEST")
        mock_get.assert_called_once_with("content", params={"spaceKey": "TEST", "status": "trashed", **{}})
        assert result == {"results": [{"id": "123", "title": "Trashed Page"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_all_pages_from_space_trash(self, mock_get, confluence_server):
        """Test get_all_pages_from_space_trash method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Trashed Page"}]}
        result = confluence_server.get_all_pages_from_space_trash("TEST")
        mock_get.assert_called_once_with(
            "content", params={"spaceKey": "TEST", "type": "page", "status": "trashed", **{}}
        )
        assert result == {"results": [{"id": "123", "title": "Trashed Page"}]}

    @patch.object(ConfluenceServer, "get")
    def test_get_all_blog_posts_from_space_trash(self, mock_get, confluence_server):
        """Test get_all_blog_posts_from_space_trash method."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Trashed Blog Post"}]}
        result = confluence_server.get_all_blog_posts_from_space_trash("TEST")
        mock_get.assert_called_once_with(
            "content", params={"spaceKey": "TEST", "type": "blogpost", "status": "trashed", **{}}
        )
        assert result == {"results": [{"id": "456", "title": "Trashed Blog Post"}]}

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
