# coding=utf-8

import logging
from .base import ConfluenceCloudBase
from requests import HTTPError
from atlassian.errors import (
    ApiError,
)

log = logging.getLogger(__name__)


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

    def get_all_pages_from_space(self, space_key, **kwargs):
        """Get all pages from space."""
        return self._get_paged("content", params={"spaceKey": space_key, "type": "page", **kwargs})

    def get_all_blog_posts_from_space(self, space_key, **kwargs):
        """Get all blog posts from space."""
        return self._get_paged("content", params={"spaceKey": space_key, "type": "blogpost", **kwargs})

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

    def get_child_pages(self, content_id, **kwargs):
        """Get child pages of a content item."""
        return self.get(f"content/{content_id}/child/page", **kwargs)

    def get_descendant_pages(self, content_id, **kwargs):
        """Get all descendant pages of a content item."""
        return self.get(f"content/{content_id}/descendant/page", **kwargs)

    def get_content_ancestors(self, content_id, **kwargs):
        """Get ancestor content."""
        return self.get(f"content/{content_id}/ancestors", **kwargs)

    def get_page_by_title(self, space_key, title, **kwargs):
        """Get page by title and space key."""
        return self.get("content", params={"spaceKey": space_key, "title": title, "type": "page", **kwargs})

    def get_blog_post_by_title(self, space_key, title, **kwargs):
        """Get blog post by title and space key."""
        return self.get("content", params={"spaceKey": space_key, "title": title, "type": "blogpost", **kwargs})

    def blog_post_exists(self, space_key, title, **kwargs):
        """Check if blog post exists."""
        result = self.get_blog_post_by_title(space_key, title, **kwargs)
        return len(result.get("results", [])) > 0
      
    def page_exists(self, space_key, title, **kwargs):
        """Check if page exists in Confluence Cloud."""
        result = self.get_page_by_title(space_key, title, **kwargs)
        return len(result.get("results", [])) > 0

    def get_page_child_by_type(self, page_id, type="page", start=None, limit=None, expand=None):
        """
        Provide content by type (page, blog, comment)
        :param page_id: A string containing the id of the type content container.
        :param type:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: how many items should be returned after the start index. Default: Site limit 200.
        :param expand: OPTIONAL: expand e.g. history
        :return:
        """
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)
        if expand is not None:
            params["expand"] = expand

        url = f"rest/api/content/{page_id}/child/{type}"
        log.info(url)

        try:
            if not self.advanced_mode and start is None and limit is None:
                return self._get_paged(url, params=params)
            else:
                response = self.get(url, params=params)
                if self.advanced_mode:
                    return response
                return response.get("results")
        except HTTPError as e:
            if e.response.status_code == 404:
                # Raise ApiError as the documented reason is ambiguous
                raise ApiError(
                    "There is no content with the given id, "
                    "or the calling user does not have permission to view the content",
                    reason=e,
                )

            raise

    def get_child_title_list(self, page_id, type="page", start=None, limit=None):
        """
        Find a list of Child title
        :param page_id: A string containing the id of the type content container.
        :param type:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: how many items should be returned after the start index. Default: Site limit 200.
        :return:
        """
        child_page = self.get_page_child_by_type(page_id, type, start, limit)
        child_title_list = [child["title"] for child in child_page]
        return child_title_list

    def get_child_id_list(self, page_id, type="page", start=None, limit=None):
        """
        Find a list of Child id
        :param page_id: A string containing the id of the type content container.
        :param type:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: how many items should be returned after the start index. Default: Site limit 200.
        :return:
        """
        child_page = self.get_page_child_by_type(page_id, type, start, limit)
        child_id_list = [child["id"] for child in child_page]
        return child_id_list

    # Space Management
    def get_spaces(self, **kwargs):
        """
        Get all spaces (single page).

        Calls the Confluence Cloud v2 endpoint ``/wiki/api/v2/spaces``.
        For paginated enumeration of every space, use :meth:`get_all_spaces`.
        """
        return self.get("spaces", **kwargs)

    def get_all_spaces(self, **kwargs):
        """
        Get all spaces with full pagination.

        Returns a generator yielding each space dict from the Confluence Cloud
        v2 endpoint ``/wiki/api/v2/spaces``. Replaces the legacy v1
        ``get_all_spaces`` (which hit ``/rest/api/space``) — that endpoint is
        not available on the OAuth API gateway and returns
        ``GoneException: This deprecated endpoint has been removed``.
        """
        return self._get_paged("spaces", params=kwargs)

    def get_space(self, space_id, **kwargs):
        """Get space by ID."""
        return self.get(f"spaces/{space_id}", **kwargs)

    def create_space(self, data, **kwargs):
        """Create new space."""
        return self.post("spaces", data=data, **kwargs)

    def update_space(self, space_id, data, **kwargs):
        """Update existing space."""
        return self.put(f"spaces/{space_id}", data=data, **kwargs)

    def delete_space(self, space_id, **kwargs):
        """Delete space."""
        return self.delete(f"spaces/{space_id}", **kwargs)

    def get_space_content(self, space_id, **kwargs):
        """Get space content."""
        return self.get(f"spaces/{space_id}/content", **kwargs)

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
