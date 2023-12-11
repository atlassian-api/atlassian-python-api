from atlassian.bitbucket import Cloud

bitbucket = Cloud(url="https://api.bitbucket.org/", token="random_string_token")

pr_id = 1

if __name__ == "__main__":
    data = bitbucket.repositories.get(workspace="workspace1", repo_slug="repository1")
    pr = data.pullrequests.get(pr_id)
    print(f"For Pull Request ID = {pr.id}")
    for pr_commit in pr.commits:
        print(f"Commit Id={pr_commit.hash}, Message={pr_commit.message}")
