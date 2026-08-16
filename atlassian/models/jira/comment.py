from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Union


@dataclass(frozen=True)
class Visibility:
    """Comment visibility restriction."""

    type: str
    value: str

    def __post_init__(self) -> None:
        """Validate visibility type and value."""
        if self.type not in ("role", "group"):
            raise ValueError(f"Visibility type must be 'role' or 'group', got '{self.type}'")
        if not self.value:
            raise ValueError("Visibility requires a 'value'")

    def to_dict(self) -> dict[str, str]:
        return {"type": self.type, "value": self.value}


@dataclass
class Comment:
    """Represents a Jira issue comment.

    Used with Jira.issue_add_comment(issue_key, comment, visibility=...).
    Supports both plain text and ADF body.
    """

    body: Union[str, dict[str, Any]]
    visibility: Optional[Visibility] = None

    def __post_init__(self) -> None:
        """Validate comment body is not empty."""
        if not self.body:
            raise ValueError("Comment requires a 'body'")

    def as_args(self) -> dict[str, Any]:
        """Return keyword arguments for Jira.issue_add_comment().

        Usage::

            c = Comment("Fixed in PR #42", visibility=Visibility("role", "Developers"))
            jira.issue_add_comment("PLAT-123", **c.as_args())
        """
        args: dict[str, Any] = {"comment": self.body}
        if self.visibility:
            args["visibility"] = self.visibility.to_dict()
        return args
