"""Read a file and list a directory with the Bitbucket Cloud OO client."""

import os

from atlassian.bitbucket import Cloud


bitbucket = Cloud(
    username=os.environ["ATLASSIAN_EMAIL"],
    password=os.environ["BITBUCKET_API_TOKEN"],
)
repository = bitbucket.workspaces.get(os.environ["BITBUCKET_WORKSPACE"]).repositories.get(
    os.environ["BITBUCKET_REPOSITORY"]
)

# A revision is required: it may be a branch, tag, or commit SHA.
contents = repository.get_source_file("main", "README.md")
print(contents.decode("utf-8"))

directory = repository.get_source_directory("main", "src")
for entry in directory["values"]:
    print(entry["path"])
