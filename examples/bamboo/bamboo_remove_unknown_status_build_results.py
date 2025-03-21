import logging

from atlassian import Bamboo

"""
That example shows how to clean up Bamboo incomplete or Unknown build results
"""

logging.basicConfig(level=logging.ERROR)

REMOVE = True
STATUS_CLEANED_RESULTS = ["Incomplete", "Unknown"]
EXCLUDED_PROJECTS = ["EXCLUDE_PROJECT"]
BAMBOO_LOGIN = "admin"
BAMBOO_PASS = "password"
BAMBOO_URL = "https://bamboo.example.com"


def get_all_projects():
    return [x["key"] for x in bamboo.projects(max_results=1000)]


def get_plans_from_project(proj):
    return [x["key"] for x in bamboo.project_plans(proj)]


def get_branches_from_plan(plan_key):
    return [x["id"] for x in bamboo.search_branches(plan_key, max_results=1000, start=0)]


def get_results_from_branch(plan_key):
    return [x for x in bamboo.results(plan_key, expand="results.result", max_results=100, include_all_states=True)]


def remove_build_result(build_key, status):
    result = bamboo.build_result(build_key=build_key)
    if result.get("buildState") == status:
        print(f"Removing build result - {build_key}")
        if REMOVE:
            bamboo.delete_build_result(build_key=build_key)


def project_review(plans):
    for plan in plans:
        print((f"Inspecting {plan} plan"))
        branches = get_branches_from_plan(plan)
        for branch in branches:
            build_results = get_results_from_branch(branch)
            for build in build_results:
                build_key = build.get("buildResultKey") or None
                print(f"Inspecting build - {build_key}")
                if build_key:
                    for status in STATUS_CLEANED_RESULTS:
                        remove_build_result(build_key=build_key, status=status)


if __name__ == "__main__":
    bamboo = Bamboo(url=BAMBOO_URL, username=BAMBOO_LOGIN, password=BAMBOO_PASS, timeout=180)
    projects = get_all_projects()
    for project in projects:
        if project in EXCLUDED_PROJECTS:
            continue
        print(f"Inspecting project - {project}")
        results = []
        all_plans_of_project = get_plans_from_project(project)
        project_review(plans=all_plans_of_project)
