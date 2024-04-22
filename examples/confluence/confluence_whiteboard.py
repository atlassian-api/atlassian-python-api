from atlassian import Confluence

confluence = Confluence(
    url="<instance_url>",
    username="<atlassian_username>",
    password="api_key",
)
"""
This is example on how to use confluence whiteboard endponds
Currently only available on confluence cloud
"""
# create whiteboard. First parameter is a spaceID (not spacekey!),
# second param is a name of whiteboard (optional), third one  is a parent pageid (optional)
confluence.create_whiteboard("42342", "My whiteboard", "545463")

#  To delete of get whiteboard, use whiteboard id
# https://<instance_name>/wiki/spaces/<space_key>/whiteboard/<whiteboard_id>
# Deleting a whiteboard moves the whiteboard to the trash, where it can be restored later
confluence.delete_whiteboard("42342")
confluence.get_whiteboard("42342")
