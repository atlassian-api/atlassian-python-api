from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Union


@dataclass
class TextNode:
    text: str
    marks: list[dict[str, Any]] = field(default_factory=list)

    def bold(self) -> TextNode:
        self.marks.append({"type": "strong"})
        return self

    def italic(self) -> TextNode:
        self.marks.append({"type": "em"})
        return self

    def code(self) -> TextNode:
        self.marks.append({"type": "code"})
        return self

    def link(self, href: str) -> TextNode:
        self.marks.append({"type": "link", "attrs": {"href": href}})
        return self

    def strike(self) -> TextNode:
        self.marks.append({"type": "strike"})
        return self

    def to_dict(self) -> dict[str, Any]:
        node: dict[str, Any] = {"type": "text", "text": self.text}
        if self.marks:
            node["marks"] = [dict(m) for m in self.marks]
        return node


@dataclass(frozen=True)
class MentionNode:
    account_id: str
    display_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "mention",
            "attrs": {"id": self.account_id, "text": self.display_text},
        }


InlineNode = Union[TextNode, MentionNode]


class ADFBuilder:
    """Fluent builder that produces an Atlassian Document Format dict."""

    def __init__(self) -> None:
        """Initialize an empty ADF document builder."""
        self._content: list[dict[str, Any]] = []

    def paragraph(self, *nodes: InlineNode) -> ADFBuilder:
        self._content.append(
            {
                "type": "paragraph",
                "content": [n.to_dict() for n in nodes],
            }
        )
        return self

    def text_paragraph(self, text: str) -> ADFBuilder:
        return self.paragraph(TextNode(text))

    def heading(self, text: str, level: int = 1) -> ADFBuilder:
        if level not in range(1, 7):
            raise ValueError(f"Heading level must be 1-6, got {level}")
        self._content.append(
            {
                "type": "heading",
                "attrs": {"level": level},
                "content": [{"type": "text", "text": text}],
            }
        )
        return self

    def bullet_list(self, items: list[str]) -> ADFBuilder:
        list_items = [
            {
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": item}],
                    }
                ],
            }
            for item in items
        ]
        self._content.append({"type": "bulletList", "content": list_items})
        return self

    def ordered_list(self, items: list[str]) -> ADFBuilder:
        list_items = [
            {
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": item}],
                    }
                ],
            }
            for item in items
        ]
        self._content.append({"type": "orderedList", "content": list_items})
        return self

    def code_block(self, code: str, language: Optional[str] = None) -> ADFBuilder:
        node: dict[str, Any] = {
            "type": "codeBlock",
            "content": [{"type": "text", "text": code}],
        }
        if language:
            node["attrs"] = {"language": language}
        self._content.append(node)
        return self

    def rule(self) -> ADFBuilder:
        self._content.append({"type": "rule"})
        return self

    def blockquote(self, *nodes: InlineNode) -> ADFBuilder:
        self._content.append(
            {
                "type": "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [n.to_dict() for n in nodes],
                    }
                ],
            }
        )
        return self

    def table(self, headers: list[str], rows: list[list[str]]) -> ADFBuilder:
        header_row = {
            "type": "tableRow",
            "content": [
                {
                    "type": "tableHeader",
                    "content": [{"type": "paragraph", "content": [{"type": "text", "text": h}]}],
                }
                for h in headers
            ],
        }
        data_rows = [
            {
                "type": "tableRow",
                "content": [
                    {
                        "type": "tableCell",
                        "content": [{"type": "paragraph", "content": [{"type": "text", "text": cell}]}],
                    }
                    for cell in row
                ],
            }
            for row in rows
        ]
        self._content.append(
            {
                "type": "table",
                "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
                "content": [header_row] + data_rows,
            }
        )
        return self

    def raw_node(self, node: dict[str, Any]) -> ADFBuilder:
        """Escape hatch for ADF node types not covered by dedicated methods."""
        self._content.append(node)
        return self

    def build(self) -> dict[str, Any]:
        return {
            "version": 1,
            "type": "doc",
            "content": list(self._content),
        }
