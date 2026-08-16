from unittest.mock import patch

from atlassian import Compass


def test_compass_uses_gateway_api_root_and_sends_metric():
    compass = Compass("https://example.atlassian.net")
    assert compass.api_root == "gateway/api"
    with patch.object(compass, "post", return_value={}) as post:
        compass.send_metric({"metric": "latency", "value": 12})
    post.assert_called_once_with("gateway/api/compass/v1/metrics", data={"metric": "latency", "value": 12})


def test_compass_attachment_routes_and_binary_response():
    compass = Compass("https://example.atlassian.net")
    with patch.object(compass, "get", return_value=b"data") as get:
        assert compass.get_forge_app_attachment("c1", "app1", "logo") == b"data"
    get.assert_called_once_with(
        "gateway/api/compass/v1/component/c1/app/app1/attachment/logo",
        not_json_response=True,
    )


def test_compass_upload_uses_file_mapping(tmp_path):
    compass = Compass("https://example.atlassian.net")
    filename = tmp_path / "openapi.yaml"
    filename.write_text("openapi: 3.0.0")
    with patch.object(compass, "put", return_value={}) as put:
        compass.upload_component_api_spec("c1", filename=str(filename))
    put.assert_called_once()
    assert put.call_args.args[0] == "gateway/api/compass/v1/component/c1/api_specs"
    assert "file" in put.call_args.kwargs["files"]
