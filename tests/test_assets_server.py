from unittest.mock import patch

from atlassian import AssetsDataCenter, AssetsServer
from atlassian.assets.assets_server import AssetsServer as ModuleAssetsServer


def test_assets_datacenter_uses_assets_rest_root():
    assets = AssetsDataCenter("https://jira.example.com")

    assert assets.api_root == "rest/assets/1.0"
    assert AssetsServer is AssetsDataCenter
    assert ModuleAssetsServer is AssetsServer

    with patch.object(assets, "get", return_value={}) as get:
        assets.get_aql_objects(query='objectType = "Server"', page=1)

    get.assert_called_once_with(
        "rest/assets/1.0/aql/objects",
        params={"qlQuery": 'objectType = "Server"', "page": 1},
    )


def test_assets_datacenter_supports_object_type_attribute_operations():
    assets = AssetsDataCenter("https://jira.example.com")
    payload = {"name": "Owner"}

    with patch.object(assets, "post", return_value={}) as post:
        assets.create_object_type_attribute("10001", payload)

    post.assert_called_once_with("rest/assets/1.0/objecttypeattribute/10001", data=payload)
