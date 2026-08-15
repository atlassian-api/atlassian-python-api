"""Append a Confluence storage-format table to an existing page.

This example works with the backwards-compatible ``Confluence`` client for
both Confluence Cloud and Server/Data Center.  Set CONFLUENCE_CLOUD=true for
Cloud, then supply the page ID and credentials as environment variables.
"""

import os
from html import escape

from atlassian import Confluence


def storage_table(headers, rows):
    """Return a Confluence storage-format table, escaping cell contents."""
    header_cells = "".join(f"<th>{escape(str(value))}</th>" for value in headers)
    body_rows = "".join(
        "<tr>{}</tr>".format("".join(f"<td>{escape(str(value))}</td>" for value in row)) for row in rows
    )
    return f"<table><tbody><tr>{header_cells}</tr>{body_rows}</tbody></table>"


def append_table(confluence, page_id, headers, rows):
    """Read a page's storage body, append a table, and write a new version."""
    page = confluence.get_page_by_id(page_id, expand="body.storage")
    page_body = page["body"]["storage"]["value"]
    updated_body = f"{page_body}{storage_table(headers, rows)}"

    # update_page obtains and increments the current page version for both
    # Cloud's compatibility API and Server/Data Center.
    return confluence.update_page(
        page_id=page_id,
        title=page["title"],
        body=updated_body,
        representation="storage",
    )


if __name__ == "__main__":
    cloud = os.getenv("CONFLUENCE_CLOUD", "false").lower() == "true"
    confluence = Confluence(
        url=os.environ["CONFLUENCE_URL"],
        username=os.environ["CONFLUENCE_USERNAME"],
        password=os.environ["CONFLUENCE_TOKEN"],
        cloud=cloud,
    )
    result = append_table(
        confluence,
        page_id=os.environ["CONFLUENCE_PAGE_ID"],
        headers=["Service", "Status"],
        rows=[["API", "Healthy"], ["Worker", "Healthy"]],
    )
    print(f"Updated page {result['id']}")
