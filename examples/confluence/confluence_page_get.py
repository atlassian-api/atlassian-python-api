# coding=utf-8
from atlassian import Confluence

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")

# If you know Space and Title
content1 = confluence.get_page_by_title(space="SPACE", title="page title")

print(content1)

# If you know page_id of the page
content2 = confluence.get_page_by_id(page_id=1123123123)

print(content2)
