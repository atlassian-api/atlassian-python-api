# coding=utf-8

import logging
import re
import time
from urllib.parse import quote
from .base import ConfluenceCloudBase
import requests
from requests import HTTPError
from atlassian.errors import (
    ApiError,
    ApiNotFoundError,
)
from .cloud import ConfluenceCloud  # noqa: F401

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

    def _cloud_wiki_url(self, path):
        """Return an absolute Cloud URL under the site's ``/wiki`` context."""
        base_url = self.url.rstrip("/")
        if not base_url.endswith("/wiki"):
            base_url += "/wiki"
        return self.url_joiner(base_url, path)

    def create_or_update_template(
        self,
        name,
        body,
        template_type="page",
        template_id=None,
        description=None,
        labels=None,
        space=None,
    ):
        """Create or update a legacy Confluence Cloud content template.

        The template API remains a V1 endpoint in Confluence Cloud.  It is
        therefore addressed explicitly rather than through this client's V2
        root.  ``body`` must be the body object returned by
        :meth:`get_content_template`, or a storage body such as
        ``{"storage": {"value": "...", "representation": "storage"}}``.
        """
        data = {"name": name, "templateType": template_type, "body": body}
        if description:
            data["description"] = description
        if labels:
            data["labels"] = labels
        if space:
            data["space"] = {"key": space}

        endpoint = self._cloud_wiki_url("rest/api/template")
        if template_id:
            data["templateId"] = template_id
            return self.put(endpoint, data=data, absolute=True)
        return self.post(endpoint, json=data, absolute=True)

    def get_content_template(self, template_id):
        """Return a legacy Confluence Cloud content template by ID."""
        endpoint = self._cloud_wiki_url(f"rest/api/template/{template_id}")
        return self.get(endpoint, absolute=True)

    def get_pdf_download_url_for_confluence_cloud(self, url):
        """Start a Cloud PDF export and return its signed download URL.

        Confluence Cloud creates PDF exports asynchronously.  The legacy task
        endpoint was removed; the current task state is available from the V2
        ``pdfexporttask`` endpoint.
        """
        try:
            response = self.get(url, headers=self.form_token_headers, not_json_response=True, absolute=True)
            task_match = re.search(rb'name="ajs-taskId"\s+content="([^"]+)"', response)
            if not task_match:
                log.error("Could not find the PDF export task ID in the response")
                return None

            task_id = task_match.group(1).decode("utf-8", errors="ignore")
            poll_url = self._cloud_wiki_url(f"api/v2/pdfexporttask/progress/{task_id}")

            while True:
                log.info("Check if PDF export task has completed.")
                progress_response = self.get(poll_url, absolute=True) or {}
                task_state = progress_response.get("state")
                if task_state == "FAILED" or progress_response.get("status") == "failed":
                    log.error("PDF conversion was not successful.")
                    return None

                download_url = progress_response.get("result")
                if isinstance(download_url, str) and download_url:
                    return self._cloud_wiki_url(download_url) if download_url.startswith("/") else download_url

                percentage_complete = int(progress_response.get("progress", 0))
                log.info("%s%% - %s", percentage_complete, task_state)
                time.sleep(3)
        except (AttributeError, TypeError, ValueError) as error:
            log.error("Could not initiate or poll the PDF export: %s", error)
            return None

    def get_page_as_pdf(self, page_id):
        """Export a Cloud page as PDF using Confluence's asynchronous exporter."""
        export_url = self._cloud_wiki_url(f"spaces/flyingpdf/pdfpageexport.action?pageId={page_id}")
        download_url = self.get_pdf_download_url_for_confluence_cloud(export_url)
        if not download_url:
            raise ApiNotFoundError("Failed to export page as PDF", reason="Failed to get download PDF URL")
        response = requests.get(download_url, timeout=75)
        response.raise_for_status()
        if not response.content.startswith(b"%PDF-"):
            raise ApiError(
                "Confluence returned non-PDF content while exporting the page. "
                "Check the page permissions and authentication configuration."
            )
        return response.content

    def export_page(self, page_id):
        """Alias for :meth:`get_page_as_pdf`."""
        return self.get_page_as_pdf(page_id)

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
        """Check whether a page exists using the Cloud V2 page endpoint.

        The retired V1 content lookup accepted a space key directly. V2 page
        queries require a space ID, so resolve the key first and request only
        one matching page.
        """
        try:
            spaces = self.get("spaces", params={"keys": [space_key], "limit": 1})
        except HTTPError as error:
            if error.response is not None and error.response.status_code == 404:
                return False
            raise
        space_results = spaces.get("results", [])
        if not space_results:
            return False

        try:
            result = self.get(
                "pages",
                params={
                    "space-id": space_results[0]["id"],
                    "title": title,
                    "status": "current",
                    "body-format": "none",
                    "limit": 1,
                    **kwargs,
                },
            )
        except HTTPError as error:
            if error.response is not None and error.response.status_code == 404:
                return False
            raise
        return bool(result.get("results", []))

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

    def get_page_child_count(self, page_id, type="page"):
        """Return the number of direct children of ``type`` without listing them."""
        page = self.get_page_by_id(page_id, expand=f"children.{type}")
        collection = page.get("children", {}).get(type, {})
        size = collection.get("size")
        if size is not None:
            return int(size)
        return len(collection.get("results", []))

    def page_has_children(self, page_id, type="page"):
        """Return whether a page has at least one direct child of ``type``."""
        return self.get_page_child_count(page_id, type=type) > 0

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

    def get_space_names(self, **kwargs):
        """Return the names of every space without fetching page content."""
        return [space["name"] for space in self.get_all_spaces(**kwargs) if space.get("name")]

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
    def get_groups(self, start=0, limit=1000, **kwargs):
        """Get a page of Cloud groups from the supported V1 group API."""
        params = {"start": start, "limit": limit, **kwargs}
        return self.get(self._cloud_wiki_url("rest/api/group"), params=params, absolute=True)

    def get_group(self, group_id, **kwargs):
        """Get a Cloud group by its ID."""
        return self.get(
            self._cloud_wiki_url("rest/api/group/by-id"),
            params={"id": group_id, **kwargs},
            absolute=True,
        )

    def get_all_groups(self, start=0, limit=1000):
        """Return the groups from a Cloud group result page.

        This retains the legacy return shape while using the supported Cloud
        endpoint.  Use each group's ``id`` with :meth:`get_group_members`.
        """
        return self.get_groups(start=start, limit=limit).get("results", [])

    def get_group_members(self, group_id, start=None, limit=None, expand=None, **kwargs):
        """Get a paginated collection of members for a Cloud group ID."""
        params = dict(kwargs)
        if start is not None:
            params["start"] = start
        if limit is not None:
            params["limit"] = limit
        if expand is not None:
            params["expand"] = expand
        return self.get(
            self._cloud_wiki_url(f"rest/api/group/{quote(str(group_id), safe='')}/membersByGroupId"),
            params=params,
            absolute=True,
        )

    def get_all_members(self, group_id, expand=None):
        """Return all members of a Cloud group identified by its ID."""
        members = []
        start = 0
        limit = 1000
        while True:
            response = self.get_group_members(group_id, start=start, limit=limit, expand=expand)
            values = response.get("results", [])
            members.extend(values)
            if not values or len(values) < limit:
                return members
            start += len(values)

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

    def cql(self, cql, **kwargs):
        """Return one page of Cloud CQL search results."""
        return self.search_content(cql, **kwargs)

    def iter_cql(self, cql, **kwargs):
        """Yield every Cloud CQL result, following pagination links."""
        return self._get_paged("content/search", params={"cql": cql, **kwargs})

    def cql_all(self, cql, **kwargs):
        """Return all paginated Cloud CQL results as a list.

        Prefer :meth:`iter_cql` for large result sets.
        """
        return list(self.iter_cql(cql, **kwargs))

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
