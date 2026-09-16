# coding=utf-8
"""Jira Cloud Plans (Advanced Roadmaps) example.

Atlassian shipped the first official Plans REST API in December 2024
(https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-plans/).
The JiraCloud client exposes it as ordinary methods: ``get_plans``,
``create_plan``, ``get_plan``, ``update_plan``, ``duplicate_plan``,
``archive_plan``, and ``trash_plan``.

Note: managing plan *views* (list/add/delete) is not part of the official
API yet; vote on https://jira.atlassian.com/browse/JSWCLOUD-20360.
"""

from atlassian.jira import JiraCloud

jira = JiraCloud(
    url="https://example.atlassian.net",
    username="admin@example.com",
    password="api-token",
)

# List plans (paginated; cursor comes back in the response)
plans = jira.get_plans(include_trashed=False, include_archived=False)
for plan in plans.get("plans", []):
    print(plan["id"], plan["name"], plan.get("status"))

# Create a plan from a board issue source
new_plan = jira.create_plan(
    data={
        "name": "Q3 Delivery Plan",
        "leadAccountId": "5b10a2844c20165700ede21g",
        "issueSources": [{"sourceType": "BOARD", "id": "42"}],
        "scheduling": {"schedulingMethod": "MANUAL"},
        "customFields": [{"customFieldId": 10071}],
    }
)
print("Created plan:", new_plan["id"])

# Add another custom field to an existing plan (JSON Patch "Update plan")
jira.add_custom_field_to_plan(plan_id=new_plan["id"], custom_field_id=10102, filter=True)

# Inspect the plan (issue sources, custom fields, scheduling, permissions)
plan = jira.get_plan(new_plan["id"])
print("Custom fields:", plan.get("customFields"))

# Remove a custom field again through the generic JSON Patch surface
jira.update_plan(
    new_plan["id"],
    data=[{"op": "remove", "path": "/customFields/0"}],
)

# Duplicate, archive, and trash
copy = jira.duplicate_plan(new_plan["id"], data={"name": "Q3 Delivery Plan (copy)"})
jira.archive_plan(copy["id"])
jira.trash_plan(new_plan["id"])
