from pprint import pprint
from atlassian import Confluence


confluence = Confluence(
    url="http://localhost:8090",
    username="admin",
    password="admin")

status = confluence.create_page(space="~admin", title="This is the title", body="This is the body")

pprint(status.json())