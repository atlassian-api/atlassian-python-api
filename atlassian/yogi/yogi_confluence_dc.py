"""Requirement Yogi Data Center client for Confluence."""

from .base import YogiBase


class YogiConfluenceDC(YogiBase):
    """Concrete Requirement Yogi Confluence Data Center REST client."""

    def __init__(self, url, *args, **kwargs):
        """Create a Confluence Data Center client for a Confluence base URL."""
        kwargs.setdefault("cloud", False)
        super(YogiConfluenceDC, self).__init__(url, *args, **kwargs)

    def search_requirements(
        self,
        space_key,
        query=None,
        offset=None,
        limit=None,
        order=None,
        include_archived=None,
        expand=None,
        **request_kwargs,
    ):
        """Search requirements in a Confluence space."""
        params = {
            "q": query,
            "offset": offset,
            "limit": limit,
            "order": order,
            "includeArchived": include_archived,
            "expand": expand,
        }
        return self.get(
            f"rest/reqs/1/requirement2/{space_key}",
            params={key: value for key, value in params.items() if value is not None} or None,
            **request_kwargs,
        )

    def get_requirement(self, space_key, key, version=None, expand=None, **request_kwargs):
        """Retrieve one requirement from a Confluence space."""
        params = {"v": version, "expand": expand}
        return self.get(
            f"rest/reqs/1/requirement2/{space_key}/{key}",
            params={key: value for key, value in params.items() if value is not None} or None,
            **request_kwargs,
        )

    def get_baselines(self, space_key, expand=None, **request_kwargs):
        """List baselines for a Confluence space."""
        return self.get(
            f"rest/reqs/1/baseline/{space_key}",
            params={"expand": expand} if expand is not None else None,
            **request_kwargs,
        )

    def create_baseline(self, space_key, data, **request_kwargs):
        """Freeze a baseline attached to a Confluence page."""
        return self.post(f"rest/reqs/1/baseline/{space_key}/1/create", data=data, **request_kwargs)

    def create_instant_baseline(self, space_key, data, **request_kwargs):
        """Create and freeze a baseline without a parent page."""
        return self.post(f"rest/reqs/1/baseline/{space_key}/1/create-instant", data=data, **request_kwargs)

    def delete_baseline(self, space_key, baseline, **request_kwargs):
        """Delete a baseline from a Confluence space."""
        return self.delete(f"rest/reqs/1/baseline/{space_key}/{baseline}", **request_kwargs)

    def update_baseline_label(self, space_key, baseline, label, **request_kwargs):
        """Update a baseline label using a plain-text request body."""
        headers = dict(self.default_headers)
        headers["Content-Type"] = "text/plain"
        return self.put(
            f"rest/reqs/1/baseline/{space_key}/{baseline}/label", data=label, headers=headers, **request_kwargs
        )

    def get_baseline_pages(self, space_key, baseline, **request_kwargs):
        """List pages represented by a baseline."""
        return self.get(f"rest/reqs/1/baseline/{space_key}/{baseline}/pages", **request_kwargs)

    def reindex_content(self, content_id, **request_kwargs):
        """Mark a Confluence page for Requirement Yogi reindexing."""
        return self.post(f"rest/reqs/1/helpers/reindex/{content_id}", **request_kwargs)

    def get_integrations(self, **request_kwargs):
        """List Requirement Yogi application-link integrations."""
        return self.get("rest/reqs/1/integration", **request_kwargs)

    def get_integration(self, service_id, **request_kwargs):
        """Retrieve one Requirement Yogi application-link integration."""
        return self.get(f"rest/reqs/1/integration/{service_id}", **request_kwargs)


ConfluenceDC = YogiConfluenceDC
