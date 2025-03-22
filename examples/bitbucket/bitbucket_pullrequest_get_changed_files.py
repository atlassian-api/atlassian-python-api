from atlassian import Bitbucket

url = "http://localhost:7990"
username = "admin"
password = "admin"

proj = "PROJ"
repo = "test-repo"
pr_id = 123

bitbucket = Bitbucket(url=url, username=username, password=password, advanced_mode=True)

diff = bitbucket.get_pull_requests_changes(proj, repo, pr_id).json()
for item in diff.get("values", []):
    print((item.get("path", {}).get("toString")))
