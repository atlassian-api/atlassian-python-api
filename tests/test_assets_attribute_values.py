from unittest.mock import patch

from atlassian import AssetsCloud, AssetsServer


def test_get_object_attribute_value_returns_first_value_from_cloud_response():
    assets = AssetsCloud("https://example.atlassian.net")
    response = [
        {
            "objectTypeAttributeId": 42,
            "objectAttributeValues": [{"value": "owner@example.com"}],
        }
    ]
    with patch.object(assets, "get_object_attributes", return_value=response):
        assert assets.get_object_attribute_value("10001", 42) == "owner@example.com"


def test_get_object_attribute_value_supports_server_response_and_default():
    assets = AssetsServer("https://jira.example.com")
    response = {"objectAttributeBeans": [{"objectTypeAttribute": {"id": 7}, "values": [{"value": "Production"}]}]}
    with patch.object(assets, "get_object_attributes", return_value=response):
        assert assets.get_object_attribute_value("10001", 7) == "Production"
        assert assets.get_object_attribute_value("10001", 8, default="missing") == "missing"
