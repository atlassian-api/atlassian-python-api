"""Confluence Cloud V2 folder operations."""

from typing import Any, Dict, Optional

from ...confluence_base import ConfluenceBase


class FolderOperations(ConfluenceBase):
    """Base component implementing the supported Cloud folder endpoints."""

    def create_folder(self, space_id: str, title: str, parent_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a folder in a Confluence Cloud space.

        ``parent_id`` can identify a page or folder. Scoped tokens require the
        ``write:folder:confluence`` scope.
        """
        data: Dict[str, str] = {"spaceId": space_id, "title": title}
        if parent_id is not None:
            data["parentId"] = parent_id
        return self.post(self.get_endpoint("folder"), data=data)

    def get_folder(
        self,
        folder_id: str,
        include_collaborators: Optional[bool] = None,
        include_direct_children: Optional[bool] = None,
        include_operations: Optional[bool] = None,
        include_properties: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return a Confluence Cloud folder by ID.

        Scoped tokens require the ``read:folder:confluence`` scope.
        """
        optional_params = {
            "include-collaborators": include_collaborators,
            "include-direct-children": include_direct_children,
            "include-operations": include_operations,
            "include-properties": include_properties,
        }
        params = {key: value for key, value in optional_params.items() if value is not None}
        return self.get(self.get_endpoint("folder_by_id", id=folder_id), params=params)

    def delete_folder(self, folder_id: str) -> Optional[Dict[str, Any]]:
        """Move a Confluence Cloud folder to the trash.

        Scoped tokens require the ``delete:folder:confluence`` scope.
        """
        return self.delete(self.get_endpoint("folder_by_id", id=folder_id))
