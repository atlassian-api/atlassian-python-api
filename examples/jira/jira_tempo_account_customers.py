# coding: utf8
from atlassian import Jira

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

results = jira.tempo_account_get_customers()
print(("Count of Customers  " + str(len(results))))

for result in results:
    print((result.get("key"), " ", result.get("name")))
