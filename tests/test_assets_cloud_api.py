from unittest.mock import patch

from atlassian import AssetsCloud


def test_assets_import_source_mapping_supports_put_and_patch():
    assets = AssetsCloud("https://example.atlassian.net")
    payload = {"mapping": []}

    with patch.object(assets, "put", return_value={}) as put:
        assets.update_import_source_mapping("source-1", payload)
    put.assert_called_once_with("rest/assets/1.0/importsource/source-1/mapping", data=payload)

    with patch.object(assets, "patch", return_value={}) as patch_request:
        assets.update_import_source_mapping("source-1", payload, partial=True)
    patch_request.assert_called_once_with("rest/assets/1.0/importsource/source-1/mapping", data=payload)


def test_assets_object_type_and_schedule_routes():
    assets = AssetsCloud("https://example.atlassian.net")

    with patch.object(assets, "post", return_value={}) as post:
        assets.create_object_type_attribute("type-1", {"name": "Owner"})
        assets.create_import_schedule("source-1", {"cron": "0 0 * * *"})

    assert [call.args for call in post.call_args_list] == [
        ("rest/assets/1.0/objecttypeattribute/type-1",),
        ("rest/assets/1.0/importsource/source-1/importschedule",),
    ]


def test_assets_export_dataset_returns_binary_content():
    assets = AssetsCloud("https://example.atlassian.net")

    with patch.object(assets, "get", return_value=b"csv") as get:
        result = assets.export_dataset(testIssueKey="TEST-1", resolved=False)

    assert result == b"csv"
    get.assert_called_once_with(
        "rest/assets/1.0/dataset/export",
        params={"testIssueKey": "TEST-1", "resolved": False},
        not_json_response=True,
    )


def test_assets_aql_and_iql_collection_endpoints_forward_query_parameters():
    assets = AssetsCloud("https://example.atlassian.net")

    with patch.object(assets, "get", return_value={}) as get:
        assets.get_iql_objects("objectType = Server", page=2, result_per_page=50)

    get.assert_called_once_with(
        "rest/assets/1.0/iql/objects",
        params={"iql": "objectType = Server", "page": 2, "resultPerPage": 50},
    )
