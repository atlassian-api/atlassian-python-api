from unittest.mock import patch

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
