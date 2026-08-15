"""List merged pull requests associated with commits between two refs.

This example targets Bitbucket Server/Data Center. It is intentionally based on
the changelog between refs rather than a date range, so release tags and commit
hashes can be used directly.
"""

import os

from atlassian import Bitbucket


def merged_pull_requests_between_refs(bitbucket, project_key, repository_slug, ref_from, ref_to):
    """Return each merged PR associated with a commit in the requested range."""
    pull_requests = {}
    for commit in bitbucket.get_changelog(project_key, repository_slug, ref_from, ref_to):
        for pull_request in bitbucket.get_pull_requests_contain_commit(project_key, repository_slug, commit["id"]):
            if pull_request["state"] == "MERGED":
                pull_requests[pull_request["id"]] = pull_request
    return pull_requests.values()


if __name__ == "__main__":
    bitbucket = Bitbucket(
        url=os.environ["BITBUCKET_URL"],
        username=os.environ["BITBUCKET_USERNAME"],
        password=os.environ["BITBUCKET_PASSWORD"],
    )
    project = os.environ["BITBUCKET_PROJECT_KEY"]
    repository = os.environ["BITBUCKET_REPOSITORY"]

    for pull_request in merged_pull_requests_between_refs(
        bitbucket,
        project,
        repository,
        ref_from="refs/tags/v1.0.0",
        ref_to="refs/tags/v1.1.0",
    ):
        print(f"#{pull_request['id']}: {pull_request['title']}")
