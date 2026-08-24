from unittest.mock import patch

from atlassian import JiraServiceManagement, ServiceDesk


def test_legacy_service_desk_get_sla_metrics_uses_agent_endpoint():
    service_desk = ServiceDesk("https://example.atlassian.net")

    with patch.object(service_desk, "get", return_value={"metrics": []}) as get:
        result = service_desk.get_sla_metrics("10", start=0, limit=25)

    assert result == {"metrics": []}
    get.assert_called_once_with(
        "rest/servicedesk/1/servicedesk/agent/10/sla/metrics",
        params={"start": 0, "limit": 25},
        headers=service_desk.experimental_headers,
    )


def test_jsm_cloud_get_sla_metrics_uses_agent_endpoint():
    service_management = JiraServiceManagement("https://example.atlassian.net")

    with patch.object(service_management, "get", return_value={"metrics": []}) as get:
        service_management.get_sla_metrics("10")

    get.assert_called_once_with("rest/servicedesk/1/servicedesk/agent/10/sla/metrics", params=None)


def test_legacy_service_desk_update_sla_metric_uses_agent_endpoint():
    service_desk = ServiceDesk("https://example.atlassian.net")
    payload = {"id": 42, "name": "Time to resolution", "config": {"goals": []}}

    with patch.object(service_desk, "put", return_value=payload) as put:
        result = service_desk.update_sla_metric("10", "42", payload)

    assert result == payload
    put.assert_called_once_with(
        "rest/servicedesk/1/servicedesk/agent/10/sla/metrics/42",
        data=payload,
        headers=service_desk.experimental_headers,
    )


def test_jsm_cloud_update_sla_metric_uses_agent_endpoint():
    service_management = JiraServiceManagement("https://example.atlassian.net")
    payload = {"id": 42, "config": {"goals": []}}

    with patch.object(service_management, "put", return_value=payload) as put:
        result = service_management.update_sla_metric("10", "42", payload)

    assert result == payload
    put.assert_called_once_with(
        "rest/servicedesk/1/servicedesk/agent/10/sla/metrics/42",
        data=payload,
    )
