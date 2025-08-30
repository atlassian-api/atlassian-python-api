# coding=utf-8
"""
Test cases for Confluence Cloud API client.
"""

import pytest
from unittest.mock import patch

from atlassian.confluence import ConfluenceCloud


@pytest.fixture
def confluence_cloud():
    """Fixture for ConfluenceCloud client."""
    return ConfluenceCloud(url="https://test.atlassian.net", token="test-token", cloud=True)


class TestConfluenceCloud:
    """Test cases for ConfluenceCloud client."""

    def test_init_defaults(self):
        """Test ConfluenceCloud client initialization with default values."""
        confluence = ConfluenceCloud(url="https://test.atlassian.net", token="test-token")
        assert confluence.api_version == "2"
        assert confluence.api_root == "wiki/api/v2"
        assert confluence.cloud is True

    def test_init_custom_values(self):
        """Test ConfluenceCloud client initialization with custom values."""
        confluence = ConfluenceCloud(
            url="https://test.atlassian.net", token="test-token", api_version="1", api_root="custom/api/root"
        )
        # The class should respect custom values when provided
        assert confluence.api_version == "1"
        assert confluence.api_root == "custom/api/root"

    # Content Management Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_content(self, mock_get, confluence_cloud):
        """Test get_content method."""
        mock_get.return_value = {"id": "123", "title": "Test Page", "type": "page"}
        result = confluence_cloud.get_content("123")
        mock_get.assert_called_once_with("content/123", **{})
        assert result == {"id": "123", "title": "Test Page", "type": "page"}

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_by_type(self, mock_get, confluence_cloud):
        """Test get_content_by_type method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Test Page"}]}
        result = confluence_cloud.get_content_by_type("page")
        mock_get.assert_called_once_with("content", params={"type": "page", **{}})
        assert result == {"results": [{"id": "123", "title": "Test Page"}]}

    @patch.object(ConfluenceCloud, "post")
    def test_create_content(self, mock_post, confluence_cloud):
        """Test create_content method."""
        content_data = {"title": "New Page", "type": "page", "spaceId": "TEST"}
        mock_post.return_value = {"id": "456", "title": "New Page", "type": "page"}
        result = confluence_cloud.create_content(content_data)
        mock_post.assert_called_once_with("content", data=content_data, **{})
        assert result == {"id": "456", "title": "New Page", "type": "page"}

    @patch.object(ConfluenceCloud, "put")
    def test_update_content(self, mock_put, confluence_cloud):
        """Test update_content method."""
        content_data = {"title": "Updated Page"}
        mock_put.return_value = {"id": "123", "title": "Updated Page"}
        result = confluence_cloud.update_content("123", content_data)
        mock_put.assert_called_once_with("content/123", data=content_data, **{})
        assert result == {"id": "123", "title": "Updated Page"}

    @patch.object(ConfluenceCloud, "delete")
    def test_delete_content(self, mock_delete, confluence_cloud):
        """Test delete_content method."""
        mock_delete.return_value = {"success": True}
        result = confluence_cloud.delete_content("123")
        mock_delete.assert_called_once_with("content/123", **{})
        assert result == {"success": True}

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_children(self, mock_get, confluence_cloud):
        """Test get_content_children method."""
        mock_get.return_value = {"results": [{"id": "789", "title": "Child Page"}]}
        result = confluence_cloud.get_content_children("123")
        mock_get.assert_called_once_with("content/123/children", **{})
        assert result == {"results": [{"id": "789", "title": "Child Page"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_descendants(self, mock_get, confluence_cloud):
        """Test get_content_descendants method."""
        mock_get.return_value = {"results": [{"id": "999", "title": "Descendant Page"}]}
        result = confluence_cloud.get_content_descendants("123")
        mock_get.assert_called_once_with("content/123/descendants", **{})
        assert result == {"results": [{"id": "999", "title": "Descendant Page"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_ancestors(self, mock_get, confluence_cloud):
        """Test get_content_ancestors method."""
        mock_get.return_value = {"results": [{"id": "111", "title": "Ancestor Page"}]}
        result = confluence_cloud.get_content_ancestors("123")
        mock_get.assert_called_once_with("content/123/ancestors", **{})
        assert result == {"results": [{"id": "111", "title": "Ancestor Page"}]}

    # Space Management Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_spaces(self, mock_get, confluence_cloud):
        """Test get_spaces method."""
        mock_get.return_value = {"results": [{"id": "TEST", "name": "Test Space"}]}
        result = confluence_cloud.get_spaces()
        mock_get.assert_called_once_with("space", **{})
        assert result == {"results": [{"id": "TEST", "name": "Test Space"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_space(self, mock_get, confluence_cloud):
        """Test get_space method."""
        mock_get.return_value = {"id": "TEST", "name": "Test Space"}
        result = confluence_cloud.get_space("TEST")
        mock_get.assert_called_once_with("space/TEST", **{})
        assert result == {"id": "TEST", "name": "Test Space"}

    @patch.object(ConfluenceCloud, "post")
    def test_create_space(self, mock_post, confluence_cloud):
        """Test create_space method."""
        space_data = {"name": "New Space", "key": "NEW"}
        mock_post.return_value = {"id": "NEW", "name": "New Space", "key": "NEW"}
        result = confluence_cloud.create_space(space_data)
        mock_post.assert_called_once_with("space", data=space_data, **{})
        assert result == {"id": "NEW", "name": "New Space", "key": "NEW"}

    @patch.object(ConfluenceCloud, "put")
    def test_update_space(self, mock_put, confluence_cloud):
        """Test update_space method."""
        space_data = {"name": "Updated Space"}
        mock_put.return_value = {"id": "TEST", "name": "Updated Space"}
        result = confluence_cloud.update_space("TEST", space_data)
        mock_put.assert_called_once_with("space/TEST", data=space_data, **{})
        assert result == {"id": "TEST", "name": "Updated Space"}

    @patch.object(ConfluenceCloud, "delete")
    def test_delete_space(self, mock_delete, confluence_cloud):
        """Test delete_space method."""
        mock_delete.return_value = {"success": True}
        result = confluence_cloud.delete_space("TEST")
        mock_delete.assert_called_once_with("space/TEST", **{})
        assert result == {"success": True}

    @patch.object(ConfluenceCloud, "get")
    def test_get_space_content(self, mock_get, confluence_cloud):
        """Test get_space_content method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Page in Space"}]}
        result = confluence_cloud.get_space_content("TEST")
        mock_get.assert_called_once_with("space/TEST/content", **{})
        assert result == {"results": [{"id": "123", "title": "Page in Space"}]}

    # User Management Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_users(self, mock_get, confluence_cloud):
        """Test get_users method."""
        mock_get.return_value = {"results": [{"id": "user1", "name": "Test User"}]}
        result = confluence_cloud.get_users()
        mock_get.assert_called_once_with("user", **{})
        assert result == {"results": [{"id": "user1", "name": "Test User"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_user(self, mock_get, confluence_cloud):
        """Test get_user method."""
        mock_get.return_value = {"id": "user1", "name": "Test User"}
        result = confluence_cloud.get_user("user1")
        mock_get.assert_called_once_with("user/user1", **{})
        assert result == {"id": "user1", "name": "Test User"}

    @patch.object(ConfluenceCloud, "get")
    def test_get_current_user(self, mock_get, confluence_cloud):
        """Test get_current_user method."""
        mock_get.return_value = {"id": "current", "name": "Current User"}
        result = confluence_cloud.get_current_user()
        mock_get.assert_called_once_with("user/current", **{})
        assert result == {"id": "current", "name": "Current User"}

    # Group Management Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_groups(self, mock_get, confluence_cloud):
        """Test get_groups method."""
        mock_get.return_value = {"results": [{"id": "group1", "name": "Test Group"}]}
        result = confluence_cloud.get_groups()
        mock_get.assert_called_once_with("group", **{})
        assert result == {"results": [{"id": "group1", "name": "Test Group"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_group(self, mock_get, confluence_cloud):
        """Test get_group method."""
        mock_get.return_value = {"id": "group1", "name": "Test Group"}
        result = confluence_cloud.get_group("group1")
        mock_get.assert_called_once_with("group/group1", **{})
        assert result == {"id": "group1", "name": "Test Group"}

    @patch.object(ConfluenceCloud, "get")
    def test_get_group_members(self, mock_get, confluence_cloud):
        """Test get_group_members method."""
        mock_get.return_value = {"results": [{"id": "user1", "name": "Test User"}]}
        result = confluence_cloud.get_group_members("group1")
        mock_get.assert_called_once_with("group/group1/member", **{})
        assert result == {"results": [{"id": "user1", "name": "Test User"}]}

    # Label Management Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_labels(self, mock_get, confluence_cloud):
        """Test get_labels method."""
        mock_get.return_value = {"results": [{"id": "label1", "name": "Test Label"}]}
        result = confluence_cloud.get_labels()
        mock_get.assert_called_once_with("label", **{})
        assert result == {"results": [{"id": "label1", "name": "Test Label"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_labels(self, mock_get, confluence_cloud):
        """Test get_content_labels method."""
        mock_get.return_value = {"results": [{"id": "label1", "name": "Test Label"}]}
        result = confluence_cloud.get_content_labels("123")
        mock_get.assert_called_once_with("content/123/label", **{})
        assert result == {"results": [{"id": "label1", "name": "Test Label"}]}

    @patch.object(ConfluenceCloud, "post")
    def test_add_content_labels(self, mock_post, confluence_cloud):
        """Test add_content_labels method."""
        label_data = {"name": "New Label"}
        mock_post.return_value = {"id": "label2", "name": "New Label"}
        result = confluence_cloud.add_content_labels("123", label_data)
        mock_post.assert_called_once_with("content/123/label", data=label_data, **{})
        assert result == {"id": "label2", "name": "New Label"}

    @patch.object(ConfluenceCloud, "delete")
    def test_remove_content_label(self, mock_delete, confluence_cloud):
        """Test remove_content_label method."""
        mock_delete.return_value = {"success": True}
        result = confluence_cloud.remove_content_label("123", "label1")
        mock_delete.assert_called_once_with("content/123/label/label1", **{})
        assert result == {"success": True}

    # Attachment Management Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_attachments(self, mock_get, confluence_cloud):
        """Test get_attachments method."""
        mock_get.return_value = {"results": [{"id": "att1", "title": "Test Attachment"}]}
        result = confluence_cloud.get_attachments("123")
        mock_get.assert_called_once_with("content/123/child/attachment", **{})
        assert result == {"results": [{"id": "att1", "title": "Test Attachment"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_attachment(self, mock_get, confluence_cloud):
        """Test get_attachment method."""
        mock_get.return_value = {"id": "att1", "title": "Test Attachment"}
        result = confluence_cloud.get_attachment("att1")
        mock_get.assert_called_once_with("content/att1", **{})
        assert result == {"id": "att1", "title": "Test Attachment"}

    @patch.object(ConfluenceCloud, "post")
    def test_create_attachment(self, mock_post, confluence_cloud):
        """Test create_attachment method."""
        attachment_data = {"title": "New Attachment"}
        mock_post.return_value = {"id": "att2", "title": "New Attachment"}
        result = confluence_cloud.create_attachment("123", attachment_data)
        mock_post.assert_called_once_with("content/123/child/attachment", data=attachment_data, **{})
        assert result == {"id": "att2", "title": "New Attachment"}

    @patch.object(ConfluenceCloud, "put")
    def test_update_attachment(self, mock_put, confluence_cloud):
        """Test update_attachment method."""
        attachment_data = {"title": "Updated Attachment"}
        mock_put.return_value = {"id": "att1", "title": "Updated Attachment"}
        result = confluence_cloud.update_attachment("att1", attachment_data)
        mock_put.assert_called_once_with("content/att1", data=attachment_data, **{})
        assert result == {"id": "att1", "title": "Updated Attachment"}

    @patch.object(ConfluenceCloud, "delete")
    def test_delete_attachment(self, mock_delete, confluence_cloud):
        """Test delete_attachment method."""
        mock_delete.return_value = {"success": True}
        result = confluence_cloud.delete_attachment("att1")
        mock_delete.assert_called_once_with("content/att1", **{})
        assert result == {"success": True}

    # Comment Management Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_comments(self, mock_get, confluence_cloud):
        """Test get_comments method."""
        mock_get.return_value = {"results": [{"id": "comment1", "text": "Test Comment"}]}
        result = confluence_cloud.get_comments("123")
        mock_get.assert_called_once_with("content/123/child/comment", **{})
        assert result == {"results": [{"id": "comment1", "text": "Test Comment"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_comment(self, mock_get, confluence_cloud):
        """Test get_comment method."""
        mock_get.return_value = {"id": "comment1", "text": "Test Comment"}
        result = confluence_cloud.get_comment("comment1")
        mock_get.assert_called_once_with("content/comment1", **{})
        assert result == {"id": "comment1", "text": "Test Comment"}

    @patch.object(ConfluenceCloud, "post")
    def test_create_comment(self, mock_post, confluence_cloud):
        """Test create_comment method."""
        comment_data = {"text": "New Comment"}
        mock_post.return_value = {"id": "comment2", "text": "New Comment"}
        result = confluence_cloud.create_comment("123", comment_data)
        mock_post.assert_called_once_with("content/123/child/comment", data=comment_data, **{})
        assert result == {"id": "comment2", "text": "New Comment"}

    @patch.object(ConfluenceCloud, "put")
    def test_update_comment(self, mock_put, confluence_cloud):
        """Test update_comment method."""
        comment_data = {"text": "Updated Comment"}
        mock_put.return_value = {"id": "comment1", "text": "Updated Comment"}
        result = confluence_cloud.update_comment("comment1", comment_data)
        mock_put.assert_called_once_with("content/comment1", data=comment_data, **{})
        assert result == {"id": "comment1", "text": "Updated Comment"}

    @patch.object(ConfluenceCloud, "delete")
    def test_delete_comment(self, mock_delete, confluence_cloud):
        """Test delete_comment method."""
        mock_delete.return_value = {"success": True}
        result = confluence_cloud.delete_comment("comment1")
        mock_delete.assert_called_once_with("content/comment1", **{})
        assert result == {"success": True}

    # Search Tests
    @patch.object(ConfluenceCloud, "get")
    def test_search_content(self, mock_get, confluence_cloud):
        """Test search_content method."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Search Result"}]}
        result = confluence_cloud.search_content("type=page")
        mock_get.assert_called_once_with("content/search", params={"cql": "type=page", **{}})
        assert result == {"results": [{"id": "123", "title": "Search Result"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_search_spaces(self, mock_get, confluence_cloud):
        """Test search_spaces method."""
        mock_get.return_value = {"results": [{"id": "TEST", "name": "Test Space"}]}
        result = confluence_cloud.search_spaces("test")
        mock_get.assert_called_once_with("space/search", params={"query": "test", **{}})
        assert result == {"results": [{"id": "TEST", "name": "Test Space"}]}

    # Page Properties Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_content_properties(self, mock_get, confluence_cloud):
        """Test get_content_properties method."""
        mock_get.return_value = {"results": [{"key": "prop1", "value": "value1"}]}
        result = confluence_cloud.get_content_properties("123")
        mock_get.assert_called_once_with("content/123/property", **{})
        assert result == {"results": [{"key": "prop1", "value": "value1"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_property(self, mock_get, confluence_cloud):
        """Test get_content_property method."""
        mock_get.return_value = {"key": "prop1", "value": "value1"}
        result = confluence_cloud.get_content_property("123", "prop1")
        mock_get.assert_called_once_with("content/123/property/prop1", **{})
        assert result == {"key": "prop1", "value": "value1"}

    @patch.object(ConfluenceCloud, "post")
    def test_create_content_property(self, mock_post, confluence_cloud):
        """Test create_content_property method."""
        property_data = {"key": "prop2", "value": "value2"}
        mock_post.return_value = {"key": "prop2", "value": "value2"}
        result = confluence_cloud.create_content_property("123", property_data)
        mock_post.assert_called_once_with("content/123/property", data=property_data, **{})
        assert result == {"key": "prop2", "value": "value2"}

    @patch.object(ConfluenceCloud, "put")
    def test_update_content_property(self, mock_put, confluence_cloud):
        """Test update_content_property method."""
        property_data = {"value": "updated_value"}
        mock_put.return_value = {"key": "prop1", "value": "updated_value"}
        result = confluence_cloud.update_content_property("123", "prop1", property_data)
        mock_put.assert_called_once_with("content/123/property/prop1", data=property_data, **{})
        assert result == {"key": "prop1", "value": "updated_value"}

    @patch.object(ConfluenceCloud, "delete")
    def test_delete_content_property(self, mock_delete, confluence_cloud):
        """Test delete_content_property method."""
        mock_delete.return_value = {"success": True}
        result = confluence_cloud.delete_content_property("123", "prop1")
        mock_delete.assert_called_once_with("content/123/property/prop1", **{})
        assert result == {"success": True}

    # Template Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_templates(self, mock_get, confluence_cloud):
        """Test get_templates method."""
        mock_get.return_value = {"results": [{"id": "template1", "name": "Test Template"}]}
        result = confluence_cloud.get_templates()
        mock_get.assert_called_once_with("template", **{})
        assert result == {"results": [{"id": "template1", "name": "Test Template"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_template(self, mock_get, confluence_cloud):
        """Test get_template method."""
        mock_get.return_value = {"id": "template1", "name": "Test Template"}
        result = confluence_cloud.get_template("template1")
        mock_get.assert_called_once_with("template/template1", **{})
        assert result == {"id": "template1", "name": "Test Template"}

    # Analytics Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_content_analytics(self, mock_get, confluence_cloud):
        """Test get_content_analytics method."""
        mock_get.return_value = {"views": 100, "likes": 10}
        result = confluence_cloud.get_content_analytics("123")
        mock_get.assert_called_once_with("content/123/analytics", **{})
        assert result == {"views": 100, "likes": 10}

    @patch.object(ConfluenceCloud, "get")
    def test_get_space_analytics(self, mock_get, confluence_cloud):
        """Test get_space_analytics method."""
        mock_get.return_value = {"totalPages": 50, "totalUsers": 25}
        result = confluence_cloud.get_space_analytics("TEST")
        mock_get.assert_called_once_with("space/TEST/analytics", **{})
        assert result == {"totalPages": 50, "totalUsers": 25}

    # Export Tests
    @patch.object(ConfluenceCloud, "get")
    def test_export_content(self, mock_get, confluence_cloud):
        """Test export_content method."""
        mock_get.return_value = {"exportData": "base64_encoded_content"}
        result = confluence_cloud.export_content("123")
        mock_get.assert_called_once_with("content/123/export", **{})
        assert result == {"exportData": "base64_encoded_content"}

    @patch.object(ConfluenceCloud, "get")
    def test_export_space(self, mock_get, confluence_cloud):
        """Test export_space method."""
        mock_get.return_value = {"exportData": "base64_encoded_space"}
        result = confluence_cloud.export_space("TEST")
        mock_get.assert_called_once_with("space/TEST/export", **{})
        assert result == {"exportData": "base64_encoded_space"}

    # Utility Methods Tests
    @patch.object(ConfluenceCloud, "get")
    def test_get_metadata(self, mock_get, confluence_cloud):
        """Test get_metadata method."""
        mock_get.return_value = {"version": "2.0", "buildNumber": "123"}
        result = confluence_cloud.get_metadata()
        mock_get.assert_called_once_with("metadata", **{})
        assert result == {"version": "2.0", "buildNumber": "123"}

    @patch.object(ConfluenceCloud, "get")
    def test_get_health(self, mock_get, confluence_cloud):
        """Test get_health method."""
        mock_get.return_value = {"status": "healthy"}
        result = confluence_cloud.get_health()
        mock_get.assert_called_once_with("health", **{})
        assert result == {"status": "healthy"}
