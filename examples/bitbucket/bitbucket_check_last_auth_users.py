import argparse
import logging
from datetime import datetime

from atlassian import Bitbucket

"""
    That example shows how to make a report of bitbucket usage
"""

stash = Bitbucket(url="https://stash.example.com", username="admin", password="*********", timeout=60)


def report(all=False, non_auth=False, limit=20):
    response = stash.get_users_info(stash, limit=limit)
    users = []
    if response:
        users = response.get("values") or []
    for user in users:
        print(user)
        auth_date = user.get("lastAuthenticationTimestamp") or None
        if auth_date:
            auth_date = int(auth_date / 1000)
            full_date = datetime.utcfromtimestamp(auth_date).strftime("%Y-%m-%d %H:%M:%S")
        else:
            full_date = None
        if full_date:
            output = f"{user.get('displayName')} ({user.get('emailAddress')}) authenticated on {full_date}"
            if all:
                print(output)
        else:
            output = f"{user.get('displayName')} ({user.get('emailAddress')}) not authenticated yet"
            if non_auth or all:
                print(output)


if __name__ == "__main__":
    """
    This part of code only executes if we run this module directly.
    You can still import the execute_build function and use it separately in the different module.
    """
    # Setting the logging level. INFO|ERROR|DEBUG are the most common.
    logging.basicConfig(level=logging.ERROR)
    # Initialize argparse module with some program name and additional information
    parser = argparse.ArgumentParser(
        prog="bitbucker_auth_reviewer",
        usage="%(prog)s",
        description="Simple script to make a report of authenticated or non authenticated users",
    )
    # Adding the build key as the first argument
    parser.add_argument("--non-auth", help="Find non-auth users", dest="non_auth", action="store_true")
    parser.add_argument("--all", help="Review all users", dest="all", action="store_true")
    # Adding key=value parameters after the --arguments key
    # Getting arguments
    args = parser.parse_args()
    if args.all:
        report(all=True)
    if args.non_auth:
        report(non_auth=True)
    else:
        report(non_auth=False)
