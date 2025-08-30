# coding=utf-8

from .base import ConfluenceCloudBase


class Cloud(ConfluenceCloudBase):
    """
    Confluence Cloud REST API wrapper
    """

    def __init__(self, url="https://api.atlassian.com/", *args, **kwargs):
        # Set default values only if not provided
        if "cloud" not in kwargs:
            kwargs["cloud"] = True
        if "api_version" not in kwargs:
            kwargs["api_version"] = "2"
        if "api_root" not in kwargs:
            kwargs["api_root"] = "wiki/api/v2"
        url = url.strip("/")
        super(Cloud, self).__init__(url, *args, **kwargs)

    # Content Management
    def get_content(self, content_id, **kwargs):
        """Get content by ID."""
        return self.get(f"content/{content_id}", **kwargs)

    def get_content_by_type(self, content_type, **kwargs):
        """Get content by type (page, blogpost, etc.)."""
        return self.get("content", params={"type": content_type, **kwargs})

    def create_content(self, data, **kwargs):
        """Create new content."""
        return self.post("content", data=data, **kwargs)

    def update_content(self, content_id, data, **kwargs):
        """Update existing content."""
        return self.put(f"content/{content_id}", data=data, **kwargs)

    def delete_content(self, content_id, **kwargs):
        """Delete content."""
        return self.delete(f"content/{content_id}", **kwargs)

    def get_content_children(self, content_id, **kwargs):
        """Get child content."""
        return self.get(f"content/{content_id}/children", **kwargs)

    def get_content_descendants(self, content_id, **kwargs):
        """Get descendant content."""
        return self.get(f"content/{content_id}/descendants", **kwargs)

    def get_content_ancestors(self, content_id, **kwargs):
        """Get ancestor content."""
        return self.get(f"content/{content_id}/ancestors", **kwargs)

    # Space Management
    def get_spaces(self, **kwargs):
        """Get all spaces."""
        return self.get("space", **kwargs)

    def get_space(self, space_id, **kwargs):
        """Get space by ID."""
        return self.get(f"space/{space_id}", **kwargs)

    def create_space(self, data, **kwargs):
        """Create new space."""
        return self.post("space", data=data, **kwargs)

    def update_space(self, space_id, data, **kwargs):
        """Update existing space."""
        return self.put(f"space/{space_id}", data=data, **kwargs)

    def delete_space(self, space_id, **kwargs):
        """Delete space."""
        return self.delete(f"space/{space_id}", **kwargs)

    def get_space_content(self, space_id, **kwargs):
        """Get space content."""
        return self.get(f"space/{space_id}/content", **kwargs)

    # User Management
    def get_users(self, **kwargs):
        """Get all users."""
        return self.get("user", **kwargs)

    def get_user(self, user_id, **kwargs):
        """Get user by ID."""
        return self.get(f"user/{user_id}", **kwargs)

    def get_current_user(self, **kwargs):
        """Get current user."""
        return self.get("user/current", **kwargs)

    # Group Management
    def get_groups(self, **kwargs):
        """Get all groups."""
        return self.get("group", **kwargs)

    def get_group(self, group_id, **kwargs):
        """Get group by ID."""
        return self.get(f"group/{group_id}", **kwargs)

    def get_group_members(self, group_id, **kwargs):
        """Get group members."""
        return self.get(f"group/{group_id}/member", **kwargs)

    # Label Management
    def get_labels(self, **kwargs):
        """Get all labels."""
        return self.get("label", **kwargs)

    def get_content_labels(self, content_id, **kwargs):
        """Get content labels."""
        return self.get(f"content/{content_id}/label", **kwargs)

    def add_content_labels(self, content_id, data, **kwargs):
        """Add labels to content."""
        return self.post(f"content/{content_id}/label", data=data, **kwargs)

    def remove_content_label(self, content_id, label_id, **kwargs):
        """Remove label from content."""
        return self.delete(f"content/{content_id}/label/{label_id}", **kwargs)

    # Attachment Management
    def get_attachments(self, content_id, **kwargs):
        """Get content attachments."""
        return self.get(f"content/{content_id}/child/attachment", **kwargs)

    def get_attachment(self, attachment_id, **kwargs):
        """Get attachment by ID."""
        return self.get(f"content/{attachment_id}", **kwargs)

    def create_attachment(self, content_id, data, **kwargs):
        """Create new attachment."""
        return self.post(f"content/{content_id}/child/attachment", data=data, **kwargs)

    def update_attachment(self, attachment_id, data, **kwargs):
        """Update existing attachment."""
        return self.put(f"content/{attachment_id}", data=data, **kwargs)

    def delete_attachment(self, attachment_id, **kwargs):
        """Delete attachment."""
        return self.delete(f"content/{attachment_id}", **kwargs)

    # Comment Management
    def get_comments(self, content_id, **kwargs):
        """Get content comments."""
        return self.get(f"content/{content_id}/child/comment", **kwargs)

    def get_comment(self, comment_id, **kwargs):
        """Get comment by ID."""
        return self.get(f"content/{comment_id}", **kwargs)

    def create_comment(self, content_id, data, **kwargs):
        """Create new comment."""
        return self.post(f"content/{content_id}/child/comment", data=data, **kwargs)

    def update_comment(self, comment_id, data, **kwargs):
        """Update existing comment."""
        return self.put(f"content/{comment_id}", data=data, **kwargs)

    def delete_comment(self, comment_id, **kwargs):
        """Delete comment."""
        return self.delete(f"content/{comment_id}", **kwargs)

    # Search
    def search_content(self, query, **kwargs):
        """Search content."""
        return self.get("content/search", params={"cql": query, **kwargs})

    def search_spaces(self, query, **kwargs):
        """Search spaces."""
        return self.get("space/search", params={"query": query, **kwargs})

    # Page Properties
    def get_content_properties(self, content_id, **kwargs):
        """Get content properties."""
        return self.get(f"content/{content_id}/property", **kwargs)

    def get_content_property(self, content_id, property_key, **kwargs):
        """Get content property by key."""
        return self.get(f"content/{content_id}/property/{property_key}", **kwargs)

    def create_content_property(self, content_id, data, **kwargs):
        """Create new content property."""
        return self.post(f"content/{content_id}/property", data=data, **kwargs)

    def update_content_property(self, content_id, property_key, data, **kwargs):
        """Update existing content property."""
        return self.put(f"content/{content_id}/property/{property_key}", data=data, **kwargs)

    def delete_content_property(self, content_id, property_key, **kwargs):
        """Delete content property."""
        return self.delete(f"content/{content_id}/property/{property_key}", **kwargs)

    # Templates
    def get_templates(self, **kwargs):
        """Get all templates."""
        return self.get("template", **kwargs)

    def get_template(self, template_id, **kwargs):
        """Get template by ID."""
        return self.get(f"template/{template_id}", **kwargs)

    # Analytics
    def get_content_analytics(self, content_id, **kwargs):
        """Get content analytics."""
        return self.get(f"content/{content_id}/analytics", **kwargs)

    def get_space_analytics(self, space_id, **kwargs):
        """Get space analytics."""
        return self.get(f"space/{space_id}/analytics", **kwargs)

    # Export
    def export_content(self, content_id, **kwargs):
        """Export content."""
        return self.get(f"content/{content_id}/export", **kwargs)

    def export_space(self, space_id, **kwargs):
        """Export space."""
        return self.get(f"space/{space_id}/export", **kwargs)

    # Utility Methods
    def get_metadata(self, **kwargs):
        """Get API metadata."""
        return self.get("metadata", **kwargs)

    def get_health(self, **kwargs):
        """Get API health status."""
        return self.get("health", **kwargs)
