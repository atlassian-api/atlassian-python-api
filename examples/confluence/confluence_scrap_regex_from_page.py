from atlassian import Confluence


confluence = Confluence(
    url="<instance_url>",
    username="<user_enamil>",
    password="api_key",
)
page_id = 393464
ipv4_regex = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
confluence.scrap_regex_from_page(
    page_id, ipv4_regex
)  # method returns list of matches of ipv4 addresses from page content.
