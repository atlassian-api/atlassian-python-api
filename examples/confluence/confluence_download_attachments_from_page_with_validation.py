from atlassian import Confluence
import os

confluence_datacenter = Confluence(url="confl_server_url", token="<api_token>")


def download_attachments_test(api_wrapper_object, page_id, directory_path):
    api_wrapper_object.download_attachments_from_page(page_id=page_id, path=directory_path)


def check_file_size(directory):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            print(f"File: {filename}, Size: {os.path.getsize(os.path.join(directory, filename))} bytes")


download_attachments_test(confluence_datacenter, 393464, "~/Downloads/confluence_attachments")
check_file_size("~/Downloads/confluence_attachments")
