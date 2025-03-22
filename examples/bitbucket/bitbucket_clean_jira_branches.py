# coding=utf-8
import logging
import time

from atlassian import Jira
from atlassian import Stash

"""
Clean branches for closed issues
"""
PROJECT_KEY = "PROJ"
REPOS = ["repo1", "repo2"]
ACCEPTED_ISSUE_STATUSES = ["Closed", "Verified"]
EXCLUDE_REPO_RULES = ["refs/heads/release/", "refs/heads/master/", "development"]
LAST_COMMIT_CONDITION_IN_DAYS = 75
ATLASSIAN_USER = "gonchik.tsymzhitov"
ATLASSIAN_PASSWORD = "password"
JIRA_URL = "http://localhost:8080"
STASH_URL = "http://localhost:5999"

logging.basicConfig(level=logging.ERROR)
jira = Jira(url=JIRA_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

stash = Stash(url=STASH_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

flag = True
time_now = int(time.time()) * 1000
delta_for_time_ms = LAST_COMMIT_CONDITION_IN_DAYS * 24 * 60 * 60 * 1000
commit_info_key = "com.atlassian.bitbucket.server.bitbucket-branch:latest-commit-metadata"
out_going_pull_request = "com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata"
branch_related_issues = "com.atlassian.bitbucket.server.bitbucket-jira:branch-list-jira-issues"


def is_can_removed_branch(branch_candidate):
    branch_id_name = branch_candidate.get("id")
    # Just exclude exist mainstream branches
    if any(x in branch_id_name for x in EXCLUDE_REPO_RULES):
        print((branch.get("displayId") + " in exclusion list"))
        return False
    # skip default branch maybe DevOps made configs in ui
    if branch_candidate.get("isDefault"):
        print((branch.get("displayId") + " is default"))
        return False
    pull_request_info = (branch_candidate.get("metadata") or {}).get(out_going_pull_request) or {}
    if pull_request_info.get("pullRequest") is not None or (pull_request_info.get("open") or 0) > 0:
        print((branch.get("displayId") + " has open PR"))
        return False
    # skip branches without pull request info
    if pull_request_info is None or len(pull_request_info) == 0:
        print((branch.get("displayId") + " without pull request info"))
    #    return False

    author_time_stamp = branch_candidate.get("metadata").get(commit_info_key).get("authorTimestamp")
    # check latest commit info
    if time_now - author_time_stamp < delta_for_time_ms:
        print((branch.get("displayId") + " is too early to remove"))
        return False

    # check issues statuses
    issues_in_metadata = branch_candidate.get("metadata").get(branch_related_issues)
    for issue in issues_in_metadata:
        if jira.get_issue_status(issue.get("key")) not in ACCEPTED_ISSUE_STATUSES:
            print((branch.get("displayId") + " related issue has not Resolution "))
            return False
    # so branch can be removed
    return True


if __name__ == "__main__":
    DRY_RUN = False
    log = open("candidate_to_remove.csv", "w")
    log.write("'Branch name', 'Latest commit', 'Related issues has Resolution'\n")
    for repository in REPOS:
        step = 0
        limit = 10
        while flag:
            branches = stash.get_branches(
                PROJECT_KEY,
                repository,
                start=step * limit,
                limit=limit,
                order_by="ALPHABETICAL",
            )
            if len(branches) == 0:
                flag = False
                break
            for branch in branches:
                display_id = branch["displayId"]
                committer_time_stamp = branch.get("metadata").get(commit_info_key).get("committerTimestamp") / 1000
                last_date_commit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(committer_time_stamp))
                if is_can_removed_branch(branch):
                    if not DRY_RUN:
                        stash.delete_branch(
                            project_key=PROJECT_KEY,
                            repository_slug=repository,
                            name=display_id,
                            end_point=branch["latestCommit"],
                        )
                    log.write(f"{display_id},{last_date_commit},{True}\n")
            step += 1
    log.close()
    print("Done")
