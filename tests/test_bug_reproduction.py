import pytest

from atlassian.bitbucket.cloud.repositories.commits import Commit


def test_commit_date_parsing_raises_value_error():
    """Ensure Commit.date handles timestamps like '...+00:00Z'."""

    data = {"type": "commit", "date": "2025-09-18T21:26:38+00:00Z"}

    commit = Commit(data)

    result = commit.date
    assert result is not None
