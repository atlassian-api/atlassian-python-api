import pytest
from unittest.mock import patch

from atlassian.bitbucket import Bitbucket


def test_get_cluster_info_uses_latest_server_endpoint():
    bitbucket = Bitbucket("https://bitbucket.example.com")
    with patch.object(bitbucket, "get", return_value={"nodes": []}) as get:
        assert bitbucket.get_cluster_info() == {"nodes": []}
    get.assert_called_once_with("rest/api/latest/admin/cluster")


def test_get_cluster_info_is_not_available_on_cloud():
    bitbucket = Bitbucket("https://api.bitbucket.org", cloud=True)
    with pytest.raises(NotImplementedError, match="Server/Data Center"):
        bitbucket.get_cluster_info()
