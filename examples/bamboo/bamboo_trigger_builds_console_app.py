# coding=utf-8
import argparse
import logging
from os import environ

from atlassian import Bamboo

"""
To set up variables, use:
export BAMBOO_URL=https://your-url BAMBOO_PASSWORD=your_pass BAMBOO_USERNAME=your_username
You also can use .env files, check the awesome python-dotenv module:
https://github.com/theskumar/python-dotenv
"""
bamboo = Bamboo(
    url=environ.get("BAMBOO_URL"),
    username=environ.get("BAMBOO_USERNAME"),
    password=environ.get("BAMBOO_PASSWORD"),
    advanced_mode=True,  # In this app I use an advanced_mode flag to handle responses.
)


def execute_build(build_key, params):
    """
    build_key: str
    params: dict
    """
    started_build = bamboo.execute_build(build_key, **params)
    logging.info(f"Build execution status: {started_build.status_code}")
    if started_build.status_code == 200:
        logging.info(f"Build key: {started_build.json().get('buildResultKey')}")
        logging.info(started_build.json().get("link", {}).get("href"))
    else:
        logging.error("Execution failed!")
        logging.error(started_build.json().get("message"))


if __name__ == "__main__":
    """
    This part of code only executes if we run this module directly.
    You can still import the execute_build function and use it separately in the different module.
    """
    # Setting the logging level. INFO|ERROR|DEBUG are the most common.
    logging.basicConfig(level=logging.INFO)
    # Initialize argparse module with some program name and additional information
    parser = argparse.ArgumentParser(
        prog="bamboo_trigger",
        usage="%(prog)s BUILD-KEY --arguments [KEY VALUE]",
        description="Simple execution of the bamboo plan with provided key-value arguments",
    )
    # Adding the build key as the first argument
    parser.add_argument("build", type=str, help="Build key")
    # Adding key=value parameters after the --arguments key
    parser.add_argument("--arguments", nargs="*")
    # Getting arguments
    args = parser.parse_args()
    # Make a dictionary from the command arguments
    build_arguments = {args.arguments[i]: args.arguments[i + 1] for i in range(0, len(args.arguments or []), 2)}
    # Pass build key and arguments to the function
    execute_build(args.build, build_arguments)
