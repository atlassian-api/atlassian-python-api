# coding=utf-8

from .base import ConfluenceServerBase


class Server(ConfluenceServerBase):
    """
    Confluence Server REST API wrapper
    """

    def __init__(self, url, *args, **kwargs):
        # Set default values only if not provided
        if "cloud" not in kwargs:
            kwargs["cloud"] = False
        if "api_version" not in kwargs:
            kwargs["api_version"] = "1.0"
        if "api_root" not in kwargs:
            kwargs["api_root"] = "rest/api"
        url = url.strip("/") + f"/{kwargs['api_root']}/{kwargs['api_version']}"
        super(Server, self).__init__(url, *args, **kwargs)

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
        return self.get(f"content/{content_id}/child", **kwargs)

    def get_content_descendants(self, content_id, **kwargs):
        """Get descendant content."""
        return self.get(f"content/{content_id}/descendant", **kwargs)

    def get_content_ancestors(self, content_id, **kwargs):
        """Get ancestor content."""
        return self.get(f"content/{content_id}/ancestor", **kwargs)

    def get_content_by_title(self, space_key, title, **kwargs):
        """Get content by title and space key."""
        return self.get("content", params={"spaceKey": space_key, "title": title, **kwargs})

    def get_content_by_id(self, content_id, **kwargs):
        """Get content by ID with expand options."""
        return self.get(f"content/{content_id}", **kwargs)

    def get_all_pages_from_space(self, space_key, **kwargs):
        """Get all pages from space."""
        return self.get("content", params={"spaceKey": space_key, "type": "page", **kwargs})

    def get_all_blog_posts_from_space(self, space_key, **kwargs):
        """Get all blog posts from space."""
        return self.get("content", params={"spaceKey": space_key, "type": "blogpost", **kwargs})

    def get_page_by_title(self, space_key, title, **kwargs):
        """Get page by title and space key."""
        return self.get("content", params={"spaceKey": space_key, "title": title, "type": "page", **kwargs})

    def get_blog_post_by_title(self, space_key, title, **kwargs):
        """Get blog post by title and space key."""
        return self.get("content", params={"spaceKey": space_key, "title": title, "type": "blogpost", **kwargs})

    def page_exists(self, space_key, title, **kwargs):
        """Check if page exists."""
        result = self.get_page_by_title(space_key, title, **kwargs)
        return len(result.get("results", [])) > 0

    def blog_post_exists(self, space_key, title, **kwargs):
        """Check if blog post exists."""
        result = self.get_blog_post_by_title(space_key, title, **kwargs)
        return len(result.get("results", [])) > 0

    def get_content_id(self, space_key, title, content_type="page"):
        """Get content ID by title and space key."""
        if content_type == "page":
            result = self.get_page_by_title(space_key, title)
        elif content_type == "blogpost":
            result = self.get_blog_post_by_title(space_key, title)
        else:
            raise ValueError("content_type must be 'page' or 'blogpost'")

        results = result.get("results", [])
        if results:
            return results[0]["id"]
        return None

    def get_page_space(self, page_id):
        """Get space key from page ID."""
        page = self.get_content(page_id, expand="space")
        return page.get("space", {}).get("key")

    # Space Management
    def get_spaces(self, **kwargs):
        """Get all spaces."""
        return self.get("space", **kwargs)

    def get_space(self, space_key, **kwargs):
        """Get space by key."""
        return self.get(f"space/{space_key}", **kwargs)

    def create_space(self, data, **kwargs):
        """Create new space."""
        return self.post("space", data=data, **kwargs)

    def update_space(self, space_key, data, **kwargs):
        """Update existing space."""
        return self.put(f"space/{space_key}", data=data, **kwargs)

    def delete_space(self, space_key, **kwargs):
        """Delete space."""
        return self.delete(f"space/{space_key}", **kwargs)

    def get_space_content(self, space_key, **kwargs):
        """Get space content."""
        return self.get("content", params={"spaceKey": space_key, **kwargs})

    def get_space_permissions(self, space_key, **kwargs):
        """Get space permissions."""
        return self.get(f"space/{space_key}/permission", **kwargs)

    def get_space_settings(self, space_key, **kwargs):
        """Get space settings."""
        return self.get(f"space/{space_key}/settings", **kwargs)

    # User Management
    def get_users(self, **kwargs):
        """Get all users."""
        return self.get("user", **kwargs)

    def get_user(self, username, **kwargs):
        """Get user by username."""
        return self.get("user", params={"username": username, **kwargs})

    def get_current_user(self, **kwargs):
        """Get current user."""
        return self.get("user/current", **kwargs)

    def get_user_by_key(self, user_key, **kwargs):
        """Get user by key."""
        return self.get("user", params={"key": user_key, **kwargs})

    # Group Management
    def get_groups(self, **kwargs):
        """Get all groups."""
        return self.get("group", **kwargs)

    def get_group(self, group_name, **kwargs):
        """Get group by name."""
        return self.get("group", params={"groupname": group_name, **kwargs})

    def get_group_members(self, group_name, **kwargs):
        """Get group members."""
        return self.get(f"group/{group_name}/member", **kwargs)

    def add_user_to_group(self, group_name, username, **kwargs):
        """Add user to group."""
        return self.post(f"group/{group_name}/member", data={"name": username}, **kwargs)

    def remove_user_from_group(self, group_name, username, **kwargs):
        """Remove user from group."""
        return self.delete(f"group/{group_name}/member/{username}", **kwargs)

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

    def remove_content_label(self, content_id, label_name, **kwargs):
        """Remove label from content."""
        return self.delete(f"content/{content_id}/label/{label_name}", **kwargs)

    def get_all_pages_by_label(self, label, **kwargs):
        """Get all pages by label."""
        return self.get("content", params={"label": label, "type": "page", **kwargs})

    def get_all_blog_posts_by_label(self, label, **kwargs):
        """Get all blog posts by label."""
        return self.get("content", params={"label": label, "type": "blogpost", **kwargs})

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

    def download_attachment(self, attachment_id, **kwargs):
        """Download attachment."""
        return self.get(f"content/{attachment_id}/download", **kwargs)

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
        """Search content using CQL."""
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

    # Draft Management
    def get_draft_content(self, content_id, **kwargs):
        """Get draft content."""
        return self.get(f"content/{content_id}", params={"status": "draft", **kwargs})

    def get_all_draft_pages_from_space(self, space_key, **kwargs):
        """Get all draft pages from space."""
        return self.get("content", params={"spaceKey": space_key, "type": "page", "status": "draft", **kwargs})

    def get_all_draft_blog_posts_from_space(self, space_key, **kwargs):
        """Get all draft blog posts from space."""
        return self.get("content", params={"spaceKey": space_key, "type": "blogpost", "status": "draft", **kwargs})

    # Trash Management
    def get_trash_content(self, space_key, **kwargs):
        """Get trash content."""
        return self.get("content", params={"spaceKey": space_key, "status": "trashed", **kwargs})

    def get_all_pages_from_space_trash(self, space_key, **kwargs):
        """Get all pages from space trash."""
        return self.get("content", params={"spaceKey": space_key, "type": "page", "status": "trashed", **kwargs})

    def get_all_blog_posts_from_space_trash(self, space_key, **kwargs):
        """Get all blog posts from space trash."""
        return self.get("content", params={"spaceKey": space_key, "type": "blogpost", "status": "trashed", **kwargs})

    # Export
    def export_content(self, content_id, **kwargs):
        """Export content."""
        return self.get(f"content/{content_id}/export", **kwargs)

    def export_space(self, space_key, **kwargs):
        """Export space."""
        return self.get(f"space/{space_key}/export", **kwargs)

    # Utility Methods
    def get_metadata(self, **kwargs):
        """Get API metadata."""
        return self.get("metadata", **kwargs)

    def get_health(self, **kwargs):
        """Get API health status."""
        return self.get("health", **kwargs)

    def reindex(self, **kwargs):
        """Trigger reindex."""
        return self.post("reindex", **kwargs)

    def get_reindex_progress(self, **kwargs):
        """Get reindex progress."""
        return self.get("reindex", **kwargs)
