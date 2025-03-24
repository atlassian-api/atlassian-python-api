# coding=utf-8
import argparse

from atlassian import Bamboo

"""
    How to create the plan branch
"""
bamboo = Bamboo(url="https://", username="", password="")


def create_plan_branch(plan, vcs_branch):
    bamboo_branch = vcs_branch.replace("/", "-")
    return bamboo.create_branch(plan, bamboo_branch, vcs_branch=vcs_branch, enabled=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan")
    parser.add_argument("--vcs_branch")
    args = parser.parse_args()

    branch = create_plan_branch(plan=args.plan, vcs_branch=args.vcs_branch)
    print((branch.get("key") or branch))


if __name__ == "__main__":
    main()
