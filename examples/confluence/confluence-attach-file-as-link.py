# coding=utf-8
from atlassian import Confluence
from datetime import datetime
import logging


confluence = Confluence(
    url='http://localhost:8090',
    username='admin',
    password='admin',
)

logging.basicConfig(level=logging.DEBUG)

filename = "test_file.txt"
with open(filename, "w") as f:
    f.write(str(datetime.utcnow()))

confluence.attach_file(filename, page_id="123456789")

link = """<p>
  <ac:link>
    <ri:attachment ri:filename="{}"/>
  </ac:link>
</p>""".format(filename)

confluence.append_page(123456789, "Page Title", link)
