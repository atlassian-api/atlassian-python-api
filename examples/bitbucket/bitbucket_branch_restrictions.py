# coding=utf-8
from atlassian import Bitbucket

"""
For all possible arguments and values please visit:
https://docs.atlassian.com/bitbucket-server/rest/latest/bitbucket-ref-restriction-rest.html
"""
bitbucket = Bitbucket(
    url="http://localhost:7990", username="admin", password="admin", advanced_mode=True
)  # For more simple response handling

single_permission = bitbucket.set_branches_permissions(
    "PROJECT_KEY",
    matcher_type="branch",  # lowercase matcher type
    matcher_value="master",
    permission_type="no-deletes",
    repository_slug="repository_name",
    except_users=["user1", "user2"],
)
print(single_permission)
pid = single_permission.json().get("id")

single_permission = bitbucket.get_branch_permission("PROJECT_KEY", pid)
print(single_permission)

deleted_permission = bitbucket.delete_branch_permission("PROJECT_KEY", pid)
print(deleted_permission)

multiple_permissions_payload = [
    {
        "type": "read-only",
        "matcher": {
            "id": "master",
            "displayId": "master",
            "type": {"id": "BRANCH", "name": "Branch"},
            "active": True,
        },
        "users": [
            "user1",
        ],
        "groups": [],
        "accessKeys": [],
    },
    {
        "type": "pull-request-only",
        "matcher": {
            "id": "refs/tags/**",
            "displayId": "refs/tags/**",
            "type": {"id": "PATTERN", "name": "Pattern"},
            "active": True,
        },
        "users": ["user2"],
        "groups": [],
        "accessKeys": [],
    },
]
multiple_permissions = bitbucket.set_branches_permissions(
    "PROJECT_KEY",
    multiple_permissions=multiple_permissions_payload,
    matcher_type="branch",
    matcher_value="master",
    permission_type="no-deletes",
    repository_slug="repository_name",
    except_users=["user1", "user2"],
)
print(multiple_permissions)
