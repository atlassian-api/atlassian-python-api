# coding=utf-8
from atlassian import Confluence

"""This example shows how to export pages"""

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")

# Set page property
data = {"key": "newprp", "value": {"anything": "goes"}}
print("SET")
print((confluence.set_page_property(242793586, data)))

# # Get page property
print("GET")
print((confluence.get_page_property(242793586, "newprp")))

# Update page property
data = {
    "key": "newprp",
    "value": {"anything": "goes around"},
    "version": {"number": 2, "minorEdit": False, "hidden": False},
}
print("UPDATE")
print((confluence.update_page_property(242793586, data)))

# Delete page property
print("DELETE")
print((confluence.delete_page_property(242793586, "newprp")))
