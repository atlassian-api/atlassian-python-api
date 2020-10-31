# coding=utf-8
from atlassian import Confluence

"""This example shows how to export pages """

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")


def save_file(content, title):
    file_pdf = open(title + ".pdf", "w")
    file_pdf.write(content)
    file_pdf.close()
    print("Completed")


if __name__ == "__main__":
    label = "super-important"
    pages = confluence.get_all_pages_by_label(label=label, start=0, limit=10)
    for page in pages:
        response = confluence.get_page_as_pdf(page["id"])
        save_file(content=response, title=page["title"])
