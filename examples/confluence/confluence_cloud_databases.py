"""Create, inspect, and delete a Confluence Cloud database using the v2 API."""

import os

from atlassian import ConfluenceV2


confluence = ConfluenceV2(
    url=os.environ["CONFLUENCE_URL"],
    username=os.environ["CONFLUENCE_USERNAME"],
    password=os.environ["CONFLUENCE_API_TOKEN"],
)

database = confluence.create_database(
    space_id=os.environ["CONFLUENCE_SPACE_ID"],
    title="API-created database",
)
print(confluence.get_database(database["id"], include_properties=True))

# This moves the database to trash. Uncomment only when cleanup is intended.
# confluence.delete_database(database["id"])
