"""Confluence Cloud V2 database lifecycle operations.

The public API currently exposes database metadata only. Record, field, view,
and query operations are intentionally not provided because Atlassian does not
publish endpoints for them.
"""

from typing import Any, Dict, Optional

from ...confluence_base import ConfluenceBase


class DatabaseOperations(ConfluenceBase):
    """Base component implementing the supported Cloud database endpoints."""

    def create_database(
        self,
        space_id: str,
        title: str,
        parent_id: Optional[str] = None,
        private: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Create a database in a Confluence Cloud space.

        Requires the ``write:database:confluence`` scope for scoped tokens.
        """
        data: Dict[str, str] = {"spaceId": space_id, "title": title}
        if parent_id is not None:
            data["parentId"] = parent_id
        params = {"private": private} if private is not None else None
        return self.post(self.get_endpoint("database"), data=data, params=params)

    def get_database(
        self,
        database_id: str,
        include_collaborators: Optional[bool] = None,
        include_direct_children: Optional[bool] = None,
        include_operations: Optional[bool] = None,
        include_properties: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return database metadata by ID.

        Requires the ``read:database:confluence`` scope for scoped tokens.
        """
        optional_params = {
            "include-collaborators": include_collaborators,
            "include-direct-children": include_direct_children,
            "include-operations": include_operations,
            "include-properties": include_properties,
        }
        params = {key: value for key, value in optional_params.items() if value is not None}
        return self.get(self.get_endpoint("database_by_id", id=database_id), params=params)

    def delete_database(self, database_id: str) -> Optional[Dict[str, Any]]:
        """Move a database to the Confluence Cloud trash.

        Requires the ``delete:database:confluence`` scope for scoped tokens.
        """
        return self.delete(self.get_endpoint("database_by_id", id=database_id))
