# coding=utf-8
from atlassian import Jira
from pprint import pprint

JIRA_NODE_URL = "JIRA_NODES_1"
JIRA_LOGIN = "admin"
JIRA_PASSWD = "admin"


class IndexFixer(Jira):
    def deindex_issue(self, issue_id):
        # own end point to deindex
        url = "deindexIssue.jsp"
        params = {"issueId": issue_id}
        return self.get(url, params=params)


s = IndexFixer(url=JIRA_NODE_URL, username=JIRA_LOGIN, password=JIRA_PASSWD)
response = s.index_checker()
print("-" * 20)
pprint(response)
print("-" * 20)
fixer = False
index_orphant_issues_count = response["indexOrphansCount"]
if index_orphant_issues_count > 0:
    index_orphant_issues = response["indexOrphans"]
    for ticket in index_orphant_issues:
        ticket_id = ticket["issueId"]
        print("Orphan index for ticket id = {}".format(ticket_id))
        if fixer:
            s.deindex_issue(ticket_id)
