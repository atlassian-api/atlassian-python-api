# coding=utf-8
from atlassian import Confluence

"""This example shows how to export pages"""

confluence = Confluence(
    url="https://test.atlassian.net/wiki",
    username="admin",
    password="api-key",
    api_version="cloud",
)

if __name__ == "__main__":
    space = "TEST"
    page_title = "Test"
    page_id = confluence.get_page_id(space, page_title)
    content = confluence.export_page(page_id)
    with open(page_title + ".pdf", "wb") as pdf_file:
        pdf_file.write(content)
        pdf_file.close()
        print("Completed")
