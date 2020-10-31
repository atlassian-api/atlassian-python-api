# coding=utf-8
from atlassian import Bitbucket

bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")

# Get all tasks for a pull-request by pull_request_id
data = bitbucket.get_tasks("project_name", "repository_name", "pull_request_id")
print(data)

# Get information about task by task_id
data = bitbucket.get_task("task_id")
print(data)

# Add task to the comment by comment_ID in pull-request
data = bitbucket.add_task("comment_ID", "task_text")
print(data)

# Update task by task_ID with new state (OPEN, RESOLVED) or/and text.
data = bitbucket.update_task("task_ID", text="text", state="OPEN")
print(data)

# Delete task by task_ID. RESOLVED tasks can't be deleted
data = bitbucket.delete_task("task_ID")
print(data)
