"""Confluence Cloud V2 data-classification operations."""

from typing import Any, Dict, List, Optional, cast

from ...confluence_base import ConfluenceBase


class ClassificationLevelOperations(ConfluenceBase):
    """Operations for Confluence Cloud data-classification levels.

    Classification levels are available only to Confluence Cloud sites with the
    corresponding Atlassian Guard entitlement.
    """

    _CONTENT_RESOURCES = {
        "blogpost": "blogposts",
        "database": "databases",
        "page": "pages",
        "whiteboard": "whiteboards",
    }

    @classmethod
    def _classification_resource(cls, content_type: str) -> str:
        try:
            return cls._CONTENT_RESOURCES[content_type]
        except KeyError as error:
            allowed = ", ".join(sorted(cls._CONTENT_RESOURCES))
            raise ValueError(f"content_type must be one of: {allowed}") from error

    def _classification_url(self, content_type: str, content_id: str) -> str:
        resource = self._classification_resource(content_type)
        return f"api/v2/{resource}/{content_id}/classification-level"

    def get_classification_levels(self) -> Optional[List[Dict[str, Any]]]:
        """Return the classification levels configured for the Confluence site."""
        # The V2 schema defines this endpoint's JSON response as an array,
        # while the base client's historical ``get`` annotation is a mapping.
        return cast(Optional[List[Dict[str, Any]]], self.get("api/v2/classification-levels"))

    def get_content_classification_level(
        self, content_type: str, content_id: str, status: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Return the classification level applied to a content item."""
        params = {"status": status} if status is not None else None
        return self.get(self._classification_url(content_type, content_id), params=params)

    def update_content_classification_level(
        self, content_type: str, content_id: str, classification_level_id: str, status: str = "current"
    ) -> Optional[Dict[str, Any]]:
        """Apply a classification level to a content item."""
        if status not in ("current", "draft"):
            raise ValueError("status must be 'current' or 'draft'")
        data = {"id": classification_level_id, "status": status}
        return self.put(self._classification_url(content_type, content_id), data=data)

    def reset_content_classification_level(
        self, content_type: str, content_id: str, status: str = "current"
    ) -> Optional[Dict[str, Any]]:
        """Reset a content item to its space's default classification level."""
        if status not in ("current", "draft"):
            raise ValueError("status must be 'current' or 'draft'")
        url = f"{self._classification_url(content_type, content_id)}/reset"
        return self.post(url, data={"status": status})

    def get_space_default_classification_level(self, space_id: str) -> Optional[Dict[str, Any]]:
        """Return a space's default classification level."""
        return self.get(f"api/v2/spaces/{space_id}/classification-level/default")

    def update_space_default_classification_level(
        self, space_id: str, classification_level_id: str
    ) -> Optional[Dict[str, Any]]:
        """Set a space's default classification level."""
        return self.put(f"api/v2/spaces/{space_id}/classification-level/default", data={"id": classification_level_id})

    def delete_space_default_classification_level(self, space_id: str) -> Optional[Dict[str, Any]]:
        """Remove a space's configured default classification level."""
        return self.delete(f"api/v2/spaces/{space_id}/classification-level/default")
