"""Confluence Cloud V2 whiteboard operations."""

from typing import Any, Dict, List, Optional

from ...confluence_base import ConfluenceBase


class WhiteboardOperations(ConfluenceBase):
    """Base component implementing Confluence Cloud whiteboard endpoints."""

    def create_whiteboard(
        self,
        space_id: str,
        title: Optional[str] = None,
        parent_id: Optional[str] = None,
        template_key: Optional[str] = None,
        locale: Optional[str] = None,
        private: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Create a whiteboard in a Confluence Cloud space.

        Scoped tokens require ``write:whiteboard:confluence``. ``private`` is
        sent as the API query parameter; the remaining optional values are
        fields in the request body.
        """
        data: Dict[str, str] = {"spaceId": space_id}
        if title is not None:
            data["title"] = title
        if parent_id is not None:
            data["parentId"] = parent_id
        if template_key is not None:
            data["templateKey"] = template_key
        if locale is not None:
            data["locale"] = locale
        if private is None:
            return self.post(self.get_endpoint("whiteboard"), data=data)
        return self.post(self.get_endpoint("whiteboard"), data=data, params={"private": private})

    def get_whiteboard(
        self,
        whiteboard_id: str,
        include_collaborators: Optional[bool] = None,
        include_direct_children: Optional[bool] = None,
        include_operations: Optional[bool] = None,
        include_properties: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return a whiteboard by ID.

        Scoped tokens require ``read:whiteboard:confluence``.
        """
        optional_params = {
            "include-collaborators": include_collaborators,
            "include-direct-children": include_direct_children,
            "include-operations": include_operations,
            "include-properties": include_properties,
        }
        params = {key: value for key, value in optional_params.items() if value is not None}
        endpoint = self.get_endpoint("whiteboard_by_id", id=whiteboard_id)
        if not params:
            return self.get(endpoint)
        return self.get(endpoint, params=params)

    def get_whiteboard_by_id(self, whiteboard_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Backward-compatible alias for :meth:`get_whiteboard`."""
        return self.get_whiteboard(whiteboard_id, **kwargs)

    def delete_whiteboard(self, whiteboard_id: str) -> Optional[Dict[str, Any]]:
        """Move a whiteboard to the Confluence Cloud trash.

        Scoped tokens require ``delete:whiteboard:confluence``.
        """
        return self.delete(self.get_endpoint("whiteboard_by_id", id=whiteboard_id))

    def get_whiteboard_children(
        self, whiteboard_id: str, cursor: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Return every child of a whiteboard, following pagination."""
        params = {key: value for key, value in {"cursor": cursor, "limit": limit}.items() if value is not None}
        return list(self._get_paged(self.get_endpoint("whiteboard_children", id=whiteboard_id), params=params))

    def get_whiteboard_ancestors(self, whiteboard_id: str) -> List[Dict[str, Any]]:
        """Return the ancestors of a whiteboard."""
        response = self.get(self.get_endpoint("whiteboard_ancestors", id=whiteboard_id))
        if response is None:
            return []
        return response.get("results", [])

    def get_space_whiteboards(
        self, space_id: str, cursor: Optional[str] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Return every whiteboard in a space, following pagination."""
        params: Dict[str, Any] = {"spaceId": space_id, "limit": limit}
        if cursor is not None:
            params["cursor"] = cursor
        return list(self._get_paged(self.get_endpoint("whiteboard"), params=params))
