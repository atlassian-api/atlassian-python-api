"""Confluence Cloud V2 content-property operations."""

from typing import Any, Dict, List, Optional

from ...confluence_base import ConfluenceBase


class ContentPropertyOperations(ConfluenceBase):
    """Reusable V2 content-property operations for every supported container."""

    _PROPERTY_RESOURCES = {
        "attachment": "attachments",
        "blogpost": "blogposts",
        "comment": "comments",
        "custom_content": "custom-content",
        "database": "databases",
        "embed": "embeds",
        "folder": "folders",
        "page": "pages",
        "whiteboard": "whiteboards",
    }

    @classmethod
    def _property_resource(cls, content_type: str) -> str:
        try:
            return cls._PROPERTY_RESOURCES[content_type]
        except KeyError as error:
            allowed = ", ".join(sorted(cls._PROPERTY_RESOURCES))
            raise ValueError(f"content_type must be one of: {allowed}") from error

    def _content_properties_url(self, content_type: str, content_id: str, property_id: Optional[str] = None) -> str:
        url = f"api/v2/{self._property_resource(content_type)}/{content_id}/properties"
        return f"{url}/{property_id}" if property_id is not None else url

    def get_v2_content_properties(
        self, content_type: str, content_id: str, cursor: Optional[str] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Return all V2 properties for one content item.

        ``content_type`` is one of ``attachment``, ``blogpost``, ``comment``,
        ``custom_content``, ``database``, ``embed``, ``folder``, ``page``, or
        ``whiteboard``. Pagination is followed automatically.
        """
        if not 1 <= limit <= 250:
            raise ValueError("limit must be between 1 and 250")
        params: Dict[str, Any] = {"limit": limit}
        if cursor is not None:
            params["cursor"] = cursor
        return list(self._get_paged(self._content_properties_url(content_type, content_id), params=params))

    def create_v2_content_property(
        self, content_type: str, content_id: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a V2 content property for one content item."""
        return self.post(self._content_properties_url(content_type, content_id), data=data)

    def get_v2_content_property(self, content_type: str, content_id: str, property_id: str) -> Optional[Dict[str, Any]]:
        """Return a V2 content property by its ID."""
        return self.get(self._content_properties_url(content_type, content_id, property_id))

    def update_v2_content_property(
        self, content_type: str, content_id: str, property_id: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update a V2 content property by its ID."""
        return self.put(self._content_properties_url(content_type, content_id, property_id), data=data)

    def delete_v2_content_property(
        self, content_type: str, content_id: str, property_id: str
    ) -> Optional[Dict[str, Any]]:
        """Delete a V2 content property by its ID."""
        return self.delete(self._content_properties_url(content_type, content_id, property_id))
