from atlassian import Jira

jira_cloud = Jira(url="<url>", username="username", password="password")
jira_dc = Jira(url="url", token="<token>>")
path = "/Users/<username>>/PycharmProjects/atlassian-python-api/attachments"
# JIRA DC using custom directory path
jira_dc.download_attachments_from_issue("TEST-1", path=path, cloud=False)
# Jira cloud. Attachments will be saved to same director where script is being executed.
jira_cloud.get_attachments_ids_from_page("SC-1", cloud=True)
