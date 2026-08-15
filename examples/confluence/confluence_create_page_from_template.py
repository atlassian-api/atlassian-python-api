# coding=utf-8
"""Create a Server/Data Center page from a content template."""

from atlassian import Confluence


confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")

page = confluence.create_page_from_template(
    space="DEMO",
    title="August report",
    template_id="123456",
    replacements={"{{REPORT_MONTH}}": "August", "{{OWNER}}": "Documentation team"},
)

print(page["id"])
