"""List and complete Confluence Cloud inline tasks with the V2 client."""

import os

from atlassian import ConfluenceV2


confluence = ConfluenceV2(
    url=os.environ["CONFLUENCE_URL"],
    username=os.environ["CONFLUENCE_EMAIL"],
    password=os.environ["CONFLUENCE_API_TOKEN"],
)

for task in confluence.get_tasks(status="incomplete", body_format="storage"):
    print(f"{task['id']}: {task.get('body', {})}")

# The task API currently supports status updates only.
# confluence.update_task(task_id=12345, status="complete")
