"""Small Xray REST API v2 example.

Set XRAY_URL, XRAY_USERNAME, XRAY_PASSWORD and XRAY_TEST_KEY before running.
"""

import os

from atlassian import Xray


def main():
    xray = Xray(
        url=os.environ["XRAY_URL"],
        username=os.environ["XRAY_USERNAME"],
        password=os.environ["XRAY_PASSWORD"],
        api_version="2.0",
    )
    test_key = os.environ["XRAY_TEST_KEY"]
    for step in xray.get_test_steps(test_key, test_version="1"):
        print(step)

    # Xray accepts the JSON import schema of the installed release unchanged.
    xray.import_test_execution({"testExecutionKey": os.environ["XRAY_EXECUTION_KEY"], "tests": []})


if __name__ == "__main__":
    main()
