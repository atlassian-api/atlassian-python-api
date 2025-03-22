import logging
from datetime import datetime
from datetime import timedelta

from atlassian import Bamboo

"""
Example shows how to clean up expired build results for specific label.
Feel free to modify OLDER_DAYS and LABEL parameters.
You can remove, after changing value for DRY_RUN variable
"""

logging.basicConfig(level=logging.ERROR)
BAMBOO_LOGIN = "admin"
BAMBOO_PASSWORD = "password"
BAMBOO_URL = "https://bamboo.example.com"

DRY_RUN = True
LABEL = "cores_found"
OLDER_DAYS = 60


def get_all_projects():
    return [x["key"] for x in bamboo.projects(max_results=10000)]


def get_plans_from_project(project_key):
    return [x["key"] for x in bamboo.project_plans(project_key, max_results=1000)]


if __name__ == "__main__":
    bamboo = Bamboo(url=BAMBOO_URL, username=BAMBOO_LOGIN, password=BAMBOO_PASSWORD, timeout=180)
    projects = get_all_projects()
    print((f"Start analyzing the {len(projects)} projects"))
    for project in projects:
        print((f"Inspecting {project} project"))
        plans = get_plans_from_project(project)
        print((f"Start analyzing the {len(plans)} plans"))
        for plan in plans:
            print((f"Inspecting {plan} plan"))
            build_results = [
                x for x in bamboo.results(plan_key=plan, label=LABEL, max_results=100, include_all_states=True)
            ]
            for build in build_results:
                build_key = build.get("buildResultKey") or None
                print((f"Inspecting {build_key} build"))
                build_value = bamboo.build_result(build_key)
                build_complete_time = build_value.get("buildCompletedTime") or None
                if not build_complete_time:
                    continue
                datetimeObj = datetime.strptime(build_complete_time.split("+")[0] + "000", "%Y-%m-%dT%H:%M:%S.%f")
                if datetime.now() > datetimeObj + timedelta(days=OLDER_DAYS):
                    print(
                        (f"Build is old {build_key} as build complete date {build_complete_time.strftime('%Y-%m-%d')}")
                    )
                    if not DRY_RUN:
                        print((f"Removing {build_key} build"))
                        bamboo.delete_build_result(build_key)
