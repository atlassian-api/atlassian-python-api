from unittest.mock import call, patch

import pytest

from atlassian import ServiceDesk


def test_create_customer_request_sends_json_with_standard_headers():
    service_desk = ServiceDesk("https://example.atlassian.net")
    values = {"summary": "A request", "description": "Details", "priority": "low"}

    with patch.object(service_desk, "post", return_value={"issueKey": "HELP-1"}) as post:
        result = service_desk.create_customer_request("10", "25", values)

    assert result == {"issueKey": "HELP-1"}
    post.assert_called_once_with(
        "rest/servicedeskapi/request",
        json={
            "serviceDeskId": "10",
            "requestTypeId": "25",
            "requestFieldValues": values,
        },
        headers=service_desk.default_headers,
    )


def test_create_customer_request_rejects_non_json_field_values():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with pytest.raises(TypeError, match="values_dict must be"):
        service_desk.create_customer_request("10", "25", ["summary"])


def test_get_queue_settings_uses_admin_route():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "get", return_value={"queues": []}) as get:
        service_desk.get_queue_settings("PROJ")

    get.assert_called_once_with(
        "rest/servicedeskapi/admin/queues/PROJ",
        headers=service_desk.experimental_headers,
    )


def test_get_queue_includes_count_param():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "get", return_value={"id": "1"}) as get:
        service_desk.get_queue("10", "1", include_count=True)

    get.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/queue/1",
        headers=service_desk.experimental_headers,
        params={"includeCount": "true"},
    )


def test_create_queue_sends_dto():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "post", return_value={"id": "1"}) as post:
        service_desk.create_queue("10", "My queue", jql="project = PROJ", fields=["summary"])

    post.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/queue",
        headers=service_desk.experimental_headers,
        data={"name": "My queue", "jql": "project = PROJ", "fields": ["summary"]},
    )


def test_update_queue_posts_to_queue_id():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "post", return_value={"id": "1"}) as post:
        service_desk.update_queue("10", "1", name="Renamed")

    post.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/queue/1",
        headers=service_desk.experimental_headers,
        data={"name": "Renamed"},
    )


def test_delete_queue_deletes_queue_id():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "delete", return_value=None) as delete:
        service_desk.delete_queue("10", "1")

    delete.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/queue/1",
        headers=service_desk.experimental_headers,
    )


def test_reorder_queues_sends_comma_joined_order():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "post", return_value=None) as post:
        service_desk.reorder_queues("10", [3, 1, 2])

    post.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/queue/reorder",
        headers=service_desk.experimental_headers,
        data="3,1,2",
    )


def test_admin_queue_boolean_settings_send_raw_boolean():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "put", return_value=None) as put:
        service_desk.set_should_queues_use_count_cache_globally(True)
        service_desk.set_should_queues_include_count_globally(False)
        service_desk.set_should_queues_use_count_cache_on_project("PROJ", True)
        service_desk.set_should_queues_include_count_on_project("PROJ", False)

    assert put.call_args_list[0] == call(
        "rest/servicedeskapi/admin/queues/cache-count",
        headers=service_desk.experimental_headers,
        data=True,
    )
    assert put.call_args_list[1] == call(
        "rest/servicedeskapi/admin/queues/include-count",
        headers=service_desk.experimental_headers,
        data=False,
    )
    assert put.call_args_list[2] == call(
        "rest/servicedeskapi/admin/queues/PROJ/cache-count",
        headers=service_desk.experimental_headers,
        data=True,
    )
    assert put.call_args_list[3] == call(
        "rest/servicedeskapi/admin/queues/PROJ/include-count",
        headers=service_desk.experimental_headers,
        data=False,
    )


def test_update_request_type_sends_dto():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "put", return_value={"id": "5"}) as put:
        service_desk.update_request_type("10", "5", request_name="New name", request_description="New description")

    put.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/requesttype",
        headers=service_desk.experimental_headers,
        data={"requestTypeId": "5", "name": "New name", "description": "New description"},
    )


def test_delete_request_type_deletes_request_type_id():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "delete", return_value=None) as delete:
        service_desk.delete_request_type("10", "5")

    delete.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/requesttype/5",
        headers=service_desk.experimental_headers,
    )


def test_get_request_type_permission_uses_request_type_route():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "get", return_value={"allowlist": []}) as get:
        service_desk.get_request_type_permission("10", "5")

    get.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/requesttype/5/permission",
        headers=service_desk.experimental_headers,
    )


def test_upsert_request_type_permission_sends_allowlist():
    service_desk = ServiceDesk("https://example.atlassian.net")
    allowlist = [{"entityType": "GROUP", "entityId": "jira-users"}]

    with patch.object(service_desk, "put", return_value=None) as put:
        service_desk.upsert_request_type_permission("10", "5", allowlist)

    put.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/requesttype/5/permission",
        headers=service_desk.experimental_headers,
        data={"allowlist": allowlist},
    )


def test_get_request_type_groups_uses_request_type_group_route():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "get", return_value={"values": []}) as get:
        service_desk.get_request_type_groups("10", start=0, limit=25)

    get.assert_called_once_with(
        "rest/servicedeskapi/servicedesk/10/requesttypegroup",
        headers=service_desk.experimental_headers,
        params={"start": 0, "limit": 25},
    )


def test_get_approval_comment_config_uses_config_route():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "get", return_value={"required": True}) as get:
        service_desk.get_approval_comment_config("HELP-1", "2")

    get.assert_called_once_with(
        "rest/servicedeskapi/request/HELP-1/approval/2/config",
        headers=service_desk.experimental_headers,
    )


def test_get_portals_uses_portals_route():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "get", return_value={"values": []}) as get:
        service_desk.get_portals(start=0, limit=25)

    get.assert_called_once_with(
        "rest/servicedeskapi/portals",
        headers=service_desk.experimental_headers,
        params={"start": 0, "limit": 25},
    )


def test_get_portal_and_portal_by_project():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "get", return_value={"id": "1"}) as get:
        service_desk.get_portal("1")
        service_desk.get_portal_by_project("PROJ")

    assert get.call_args_list[0] == call(
        "rest/servicedeskapi/portals/1",
        headers=service_desk.experimental_headers,
    )
    assert get.call_args_list[1] == call(
        "rest/servicedeskapi/portals/project/PROJ",
        headers=service_desk.experimental_headers,
    )


def test_organization_cleanup_preview_and_cleanup_send_flags():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "get", return_value={"values": []}) as get, patch.object(
        service_desk, "delete", return_value=None
    ) as delete:
        service_desk.preview_organization_cleanup(delete_detached_organizations=True)
        service_desk.cleanup_organizations(delete_organizations_with_inactive_users=True)

    get.assert_called_once_with(
        "rest/servicedeskapi/organization/cleanup",
        headers=service_desk.experimental_headers,
        params={"deleteDetachedOrganizations": "true"},
    )
    delete.assert_called_once_with(
        "rest/servicedeskapi/organization/cleanup",
        headers=service_desk.experimental_headers,
        params={"deleteOrganizationsWithInactiveUsers": "true"},
    )
