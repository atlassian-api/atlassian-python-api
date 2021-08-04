import argparse
import logging

from atlassian import Jira

logging.basicConfig(level=logging.ERROR)

"""
    This is example for to generate the weekly report in one button
    You can adjust the days based on the field self.days.
    user.txt better to prepare one by line:
            user3
            user2
            user1
    as result you can give a csv file
"""


class ReportGenerator:
    def __init__(self, jira):
        print("Init configs")
        self.jira = jira
        self.cases = []
        self.users = []
        self.days = 7

    def __fetch_user_activity(self, user):
        flag = True
        limit = 10
        step = 0
        jql = "((assignee was in ({})) OR assignee in ({})) AND updated > -{}d ".format(user, user, self.days)
        print("Start fetching info jql = {}".format(jql))
        while flag:
            values = []
            try:
                response = self.jira.jql(
                    jql,
                    fields=["created", "summary", "status"],
                    expand="changelog",
                    limit=limit,
                    start=step * limit,
                )
                values = response.get("issues") or []
            except ValueError:
                values = []
            if values:
                step += 1
                for value in values:
                    value["actor"] = self.jira.user(user).get("displayName")
                    self.cases.append(value)
            else:
                flag = False

    def __get_changes_of_cases(self, histories):
        from datetime import datetime, timezone

        today = datetime.now(timezone.utc)
        output = ""
        for history in histories:
            change_date = datetime.strptime(history.get("created"), "%Y-%m-%dT%H:%M:%S.%f%z")
            difference = today - change_date
            if difference.days > self.days:
                continue
            output = [
                history.get("author").get("name"),
                change_date.format("%Y-%m-%d"),
            ]  # person who did the change
            changes = ["Listing all items that changed:"]
            for item in history.get("items"):
                changes.append(
                    "{} - {}- {}".format(
                        item["field"],
                        item["fromString"],
                        item["toString"],
                    )
                )
            output.append("\t".join(changes))
        return " - ".join(output)

    def fetching(self):
        for user in self.users:
            self.__fetch_user_activity(user=user)
        pass

    def console_output(self, delimiter="|", console=True):
        """
        Print values to check
        :return:
        """
        number = 1
        data = []
        for case in self.cases:
            print("Processing case #{}".format(number))
            output = [
                case.get("actor"),
                case.get("key"),
                case.get("fields").get("summary"),
                case.get("fields").get("status").get("name"),
            ]
            histories = (case.get("changelog") or {}).get("histories") or []
            output.append('"' + self.__get_changes_of_cases(histories) + '"')
            line = delimiter.join(output)
            if console:
                print(line)
            data.append(line)
            number += 1
        return "\n".join(data)

    def export(self, filename, delimiter=";"):
        """
        Prepare a csv file
        :return:
        """

        write_file = open(filename, "w")
        write_file.write(self.console_output(delimiter=delimiter, console=False))
        write_file.close()

    def load_users(self, filename):
        users = []
        with open(filename, "r") as f:
            for line in f:
                users.append(line.strip())
        self.users = users
        pass


def main():
    parser = argparse.ArgumentParser(description="Just wrapper to make arguments")
    parser.add_argument("--url", type=str, action="store")
    parser.add_argument("--user", type=str, action="store")
    parser.add_argument("--password", type=str, action="store")
    parser.add_argument(
        "--user_file",
        type=str,
        action="store",
        description="user.txt with username in each line",
    )
    args = parser.parse_args()
    # validate jql method
    jira = Jira(url=args.url, username=args.user, password=args.password)
    report = ReportGenerator(jira=jira)
    report.load_users(args.user_file)
    report.fetching()
    # report.print()
    report.export("export.csv")


if __name__ == "__main__":
    main()
