from unittest import TestCase
from unittest.mock import patch

from atlassian import AssetsCloud


class TestAssetsObjectTypeAttributes(TestCase):
    def test_query_params_use_the_documented_api_names(self):
        assets = AssetsCloud("https://example.atlassian.net")

        with patch.object(assets, "get", return_value={}) as get:
            assets.get_object_type_attributes(
                "1",
                only_value_editable=True,
                order_by_name=True,
                query="name",
                include_values_exist=True,
                exclude_parent_attributes=True,
                include_children=True,
                order_by_required=True,
            )

        params = get.call_args.kwargs["params"]
        self.assertEqual(
            params,
            {
                "onlyValueEditable": True,
                "orderByName": True,
                "query": "name",
                "includeValuesExist": True,
                "excludeParentAttributes": True,
                "includeChildren": True,
                "orderByRequired": True,
            },
        )

    def test_unset_params_are_still_omitted(self):
        assets = AssetsCloud("https://example.atlassian.net")

        with patch.object(assets, "get", return_value={}) as get:
            assets.get_object_type_attributes("1", include_children=True)

        self.assertEqual(get.call_args.kwargs["params"], {"includeChildren": True})

    def test_type_id_is_not_sent_as_a_query_param(self):
        assets = AssetsCloud("https://example.atlassian.net")

        with patch.object(assets, "get", return_value={}) as get:
            assets.get_object_type_attributes("1")

        self.assertEqual(get.call_args.kwargs["params"], {})
        self.assertIn("objecttype/1/attributes", get.call_args.args[0])
