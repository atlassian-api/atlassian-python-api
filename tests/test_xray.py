from unittest.mock import patch

from atlassian import Xray


def test_v2_test_steps_use_plural_route_and_test_version():
    xray = Xray("https://jira.example.com", api_version="2.0")

    with patch.object(xray, "get", return_value=[]) as get:
        xray.get_test_steps("TEST-1", test_version="1")

    get.assert_called_once_with(
        "rest/raven/2.0/api/test/TEST-1/steps",
        params={"testVersion": "1"},
    )


def test_v2_update_test_run_iteration_step_status_forwards_status_query():
    xray = Xray("https://jira.example.com", api_version="2.0")

    with patch.object(xray, "put", return_value=None) as put:
        xray.update_test_run_iteration_step_status(12, 3, 4, "PASS")

    put.assert_called_once_with(
        "rest/raven/2.0/api/testrun/12/iteration/3/step/4/status",
        params={"status": "PASS"},
    )


def test_v2_dataset_export_forwards_supported_filters_as_binary_response():
    xray = Xray("https://jira.example.com", api_version="2.0")

    with patch.object(xray, "get", return_value=b"csv") as get:
        result = xray.export_dataset(testIssueKey="TEST-1", resolved=True)

    assert result == b"csv"
    get.assert_called_once_with(
        "rest/raven/2.0/api/dataset/export",
        params={"testIssueKey": "TEST-1", "resolved": True},
        not_json_response=True,
    )


def test_v2_import_execution_multipart_forwards_files():
    xray = Xray("https://jira.example.com", api_version="2.0")
    files = {"file": ("results.json", b"{}", "application/json")}

    with patch.object(xray, "post", return_value={"key": "EXEC-1"}) as post:
        result = xray.import_test_execution_multipart(files=files)

    assert result == {"key": "EXEC-1"}
    post.assert_called_once_with(
        "rest/raven/2.0/api/import/execution/multipart",
        data=None,
        files=files,
    )
