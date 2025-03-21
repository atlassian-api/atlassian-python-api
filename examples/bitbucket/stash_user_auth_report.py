import logging
from datetime import datetime

from atlassian import Bitbucket

"""
    That example shows how to make a report of bitbucket usage
"""

stash = Bitbucket(
    url="https://stash.example.com",
    username="admin",
    password="*************",
    timeout=60,
)


def report(limit=200, include_in_active=False):
    response = stash.get_users_info(stash, limit=limit)
    users = []
    if response:
        users = response.get("values") or []
    print("|Status|Display name| Email |Last Auth DateTime|")
    for user in users:
        auth_date = user.get("lastAuthenticationTimestamp") or None
        if auth_date:
            auth_date = int(auth_date / 1000)
            full_date = datetime.utcfromtimestamp(auth_date).strftime("%Y-%m-%d %H:%M:%S")
        else:
            full_date = None
        if include_in_active or user.get("active"):
            output = f"|{user.get('active')}|{user.get('displayName')}|{user.get('emailAddress')}|{full_date}|"
            print(output)


if __name__ == "__main__":
    """
    This part of code only executes if we run this module directly.
    You can still import the execute_build function and use it separately in the different module.
    """
    # Setting the logging level. INFO|ERROR|DEBUG are the most common.
    logging.basicConfig(level=logging.ERROR)
    report(limit=1000)
