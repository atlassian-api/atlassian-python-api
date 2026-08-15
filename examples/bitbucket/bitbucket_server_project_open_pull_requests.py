"""Print every open pull request in a Bitbucket Server/Data Center project."""

import os

from atlassian import Bitbucket


bitbucket = Bitbucket(
    url=os.environ["BITBUCKET_URL"],
    username=os.environ["BITBUCKET_USERNAME"],
    password=os.environ["BITBUCKET_PASSWORD"],
)
project_key = os.environ["BITBUCKET_PROJECT_KEY"]

# repo_all_list() and get_pull_requests() are generators. Iterating them fetches
# further result pages only when needed.
for repository in bitbucket.repo_all_list(project_key):
    for pull_request in bitbucket.get_pull_requests(project_key, repository["slug"], state="OPEN"):
        print(f"{repository['slug']}: {pull_request['title']}")
