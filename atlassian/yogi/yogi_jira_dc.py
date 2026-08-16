"""Requirement Yogi Data Center client for Jira."""

from .base import YogiBase


class YogiJiraDC(YogiBase):
    """Concrete Requirement Yogi Jira Data Center REST client."""

    def __init__(self, url, *args, **kwargs):
        """Create a Jira Data Center client for a Jira base URL."""
        kwargs.setdefault("cloud", False)
        super(YogiJiraDC, self).__init__(url, *args, **kwargs)

    def get_api_info(self, applink_id=None, url=None, **request_kwargs):
        """Return Requirement Yogi API information for the current Jira user."""
        params = {"applinkId": applink_id, "url": url}
        return self.get(
            "rest/reqs/1/api",
            params={key: value for key, value in params.items() if value is not None} or None,
            **request_kwargs,
        )

    def post_api_messages(self, data, **request_kwargs):
        """Send Confluence-to-Jira synchronization messages."""
        return self.post("rest/reqs/1/api", data=data, **request_kwargs)

    def update_api_mode(self, applink_id, data, **request_kwargs):
        """Change the synchronization mode for an application link."""
        return self.put(f"rest/reqs/1/api/{applink_id}/mode", data=data, **request_kwargs)

    def update_api_version(self, applink_id, data, **request_kwargs):
        """Negotiate and update the API version for an application link."""
        return self.put(f"rest/reqs/1/api/{applink_id}/version", data=data, **request_kwargs)

    def get_issue_links(self, issue_key=None, relationship=None, **request_kwargs):
        """List Requirement Yogi links, optionally for one Jira issue."""
        path = "rest/reqs/1/issuelinks" if issue_key is None else f"rest/reqs/1/issuelinks/{issue_key}"
        return self.get(
            path, params={"relationship": relationship} if relationship is not None else None, **request_kwargs
        )

    def create_issue_links(self, issue_key, data, **request_kwargs):
        """Create Requirement Yogi links for a Jira issue."""
        return self.post(f"rest/reqs/1/issuelinks/{issue_key}", data=data, **request_kwargs)

    def replace_issue_links(self, issue_key, data, relationship=None, **request_kwargs):
        """Replace Requirement Yogi links for a Jira issue."""
        return self.put(
            f"rest/reqs/1/issuelinks/{issue_key}",
            data=data,
            params={"relationship": relationship} if relationship is not None else None,
            **request_kwargs,
        )

    def delete_issue_links(self, issue_key, data, **request_kwargs):
        """Delete the supplied Requirement Yogi links from a Jira issue."""
        return self.delete(f"rest/reqs/1/issuelinks/{issue_key}", data=data, **request_kwargs)

    def sync_issues(self, issues, **request_kwargs):
        """Request synchronization of the supplied Jira issue keys."""
        return self.put("rest/reqs/1/sync", params={"issues": issues}, **request_kwargs)


JiraDC = YogiJiraDC
