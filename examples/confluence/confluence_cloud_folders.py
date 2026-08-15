"""Create and inspect a Confluence Cloud folder using the v2 API."""

import os

from atlassian import ConfluenceV2


confluence = ConfluenceV2(
    url=os.environ["CONFLUENCE_URL"],
    username=os.environ["CONFLUENCE_USERNAME"],
    password=os.environ["CONFLUENCE_API_TOKEN"],
)

folder = confluence.create_folder(
    space_id=os.environ["CONFLUENCE_SPACE_ID"],
    title="API-created folder",
    parent_id=os.environ.get("CONFLUENCE_PARENT_ID"),
)
print(confluence.get_folder(folder["id"], include_direct_children=True))

# This moves the folder to trash. Uncomment only when cleanup is intended.
# confluence.delete_folder(folder["id"])
