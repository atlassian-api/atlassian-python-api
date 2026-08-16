from unittest.mock import patch

import pytest

from atlassian.bitbucket.cloud.repositories import Repository


@pytest.fixture
def repository():
    return Repository(
        {
            "type": "repository",
            "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/workspace/repository"}},
        }
    )


@patch.object(Repository, "get", return_value=b"# README\n")
def test_get_source_file_returns_raw_bytes_and_quotes_path(mock_get, repository):
    assert repository.get_source_file("main", "docs/My file.md") == b"# README\n"
    mock_get.assert_called_once_with("src/main/docs/My%20file.md", not_json_response=True)


@patch.object(Repository, "get", return_value={"values": []})
def test_get_source_directory_returns_json_listing(mock_get, repository):
    assert repository.get_source_directory("v1.0", "src") == {"values": []}
    mock_get.assert_called_once_with("src/v1.0/src")


def test_get_source_file_requires_a_path(repository):
    with pytest.raises(ValueError, match="path must identify a file"):
        repository.get_source_file("main", "/")
