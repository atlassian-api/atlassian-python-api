# coding=utf-8
import logging
from datetime import datetime

from atlassian import Confluence

confluence = Confluence(
    url="http://localhost:8090",
    username="admin",
    password="admin",
)

logging.basicConfig(level=logging.DEBUG)

filename = "test_file.txt"
with open(filename, "w") as f:
    f.write(str(datetime.utcnow()))

confluence.attach_file(filename, page_id="123456789")

link = f"""<p>
  <ac:link>
    <ri:attachment ri:filename="{filename}"/>
  </ac:link>
</p>"""

confluence.append_page(123456789, "Page Title", link)
