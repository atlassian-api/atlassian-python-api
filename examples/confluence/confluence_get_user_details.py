# coding=utf-8
from atlassian import Confluence

""" This example related get user details and his status"""

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")

result = confluence.get_user_details_by_username(username="gonchik.tsymzhitov", expand="status")
print(result)
