from atlassian import Confluence
import logging

confluence = Confluence(
    url="<instance_url>",
    username="<user_enamil>",
    password="api_key",
)
page_id = 393464
logging.basicConfig(level=logging.INFO)
# Page_id is the page id of the page you want to get the tables from.

result = confluence.get_tables_from_page(page_id)
print(result)
# Let's say page has two table, each one has 3 columns and 2 rows'
# Method should return following output: {"page_id": 393464, "number_of_tables_in_page": 2, "tables_content": [[["header1", "header2", "header3"], ["h1r1", "h2r1", "h3r1"], ["h1r2", "h2r2", "h3r2"]], [["table2 header1", "table2 header2", "table2 header3"], ["h1r1", "h2r1", "h3r1"], ["h1r2", "h2r2", "h3r2"]]]}
# tables_content is a list of lists of lists. Each nested list represents a table. Each nested list inside a table represents a row.
