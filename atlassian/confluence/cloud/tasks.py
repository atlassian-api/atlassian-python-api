"""Confluence Cloud V2 task operations."""

from typing import Any, Dict, List, Optional, Sequence

from ...confluence_base import ConfluenceBase


class TaskOperations(ConfluenceBase):
    """Operations for Confluence Cloud inline tasks."""

    def get_tasks(
        self,
        body_format: Optional[str] = None,
        include_blank_tasks: Optional[bool] = None,
        status: Optional[str] = None,
        task_ids: Optional[Sequence[int]] = None,
        space_ids: Optional[Sequence[int]] = None,
        page_ids: Optional[Sequence[int]] = None,
        blogpost_ids: Optional[Sequence[int]] = None,
        created_by: Optional[Sequence[str]] = None,
        assigned_to: Optional[Sequence[str]] = None,
        completed_by: Optional[Sequence[str]] = None,
        created_at_from: Optional[int] = None,
        created_at_to: Optional[int] = None,
        due_at_from: Optional[int] = None,
        due_at_to: Optional[int] = None,
        completed_at_from: Optional[int] = None,
        completed_at_to: Optional[int] = None,
        cursor: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return all visible Confluence Cloud tasks matching the supplied filters.

        Date filters are Unix epoch milliseconds.  The endpoint is cursor
        paginated; this method follows every result page, while ``limit``
        controls the number requested per page (1--250).
        """
        if body_format is not None and body_format not in ("storage", "atlas_doc_format", "view"):
            raise ValueError("body_format must be 'storage', 'atlas_doc_format', or 'view'")
        if status is not None and status not in ("complete", "incomplete"):
            raise ValueError("status must be 'complete' or 'incomplete'")
        if not 1 <= limit <= 250:
            raise ValueError("limit must be between 1 and 250")

        filters = {
            "body-format": body_format,
            "include-blank-tasks": include_blank_tasks,
            "status": status,
            "task-id": task_ids,
            "space-id": space_ids,
            "page-id": page_ids,
            "blogpost-id": blogpost_ids,
            "created-by": created_by,
            "assigned-to": assigned_to,
            "completed-by": completed_by,
            "created-at-from": created_at_from,
            "created-at-to": created_at_to,
            "due-at-from": due_at_from,
            "due-at-to": due_at_to,
            "completed-at-from": completed_at_from,
            "completed-at-to": completed_at_to,
            "cursor": cursor,
        }
        params = {key: value for key, value in filters.items() if value is not None}
        params["limit"] = limit
        return list(self._get_paged(self.get_endpoint("tasks"), params=params))

    def get_task(self, task_id: int, body_format: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Return a task by ID. Scoped tokens require ``read:task:confluence``."""
        if body_format is not None and body_format not in ("storage", "atlas_doc_format", "view"):
            raise ValueError("body_format must be 'storage', 'atlas_doc_format', or 'view'")
        params = {"body-format": body_format} if body_format is not None else None
        return self.get(self.get_endpoint("task_by_id", id=task_id), params=params)

    def update_task(self, task_id: int, status: str, body_format: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update a task's status to ``complete`` or ``incomplete``.

        Confluence currently supports updating only the status. Scoped tokens
        require ``write:task:confluence``.
        """
        if status not in ("complete", "incomplete"):
            raise ValueError("status must be 'complete' or 'incomplete'")
        if body_format is not None and body_format not in ("storage", "atlas_doc_format", "view"):
            raise ValueError("body_format must be 'storage', 'atlas_doc_format', or 'view'")
        params = {"body-format": body_format} if body_format is not None else None
        return self.put(self.get_endpoint("task_by_id", id=task_id), data={"status": status}, params=params)
