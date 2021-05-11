# coding=utf-8
from atlassian import Confluence

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")

status = confluence.create_page(space="DEMO", title="This is the title", body="This is the body")

print(status)
