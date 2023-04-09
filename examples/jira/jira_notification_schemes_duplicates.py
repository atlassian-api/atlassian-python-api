from atlassian import Jira

jira = Jira(url="http://localhost:8090", username="admin", password="admin")


def compare_dicts(dict1, dict2, print_diffs=False):
    count = 0
    hint = []
    if len(dict1) != len(dict2) and len(dict1) != len(dict2) + 1 and len(dict2) != len(dict1) + 1:
        return False

    for key in dict1:
        if dict1[key] != dict2.get(key):
            count += 1
            hint.append(key)
            if count > 1:
                return False
    line = None
    if len(dict1) != len(dict2):
        line = "Different size"
    if count == 1:
        line = "Different: " + hint[0]
    if line and print_diffs:
        print(line)
    return True


def review():
    notification_scheme_dict = {}
    all_notification_schemes_dict = {}

    notification_schemes_ids = jira.get_notification_schemes()
    names = []

    for notification_schemes_id in notification_schemes_ids["values"]:
        notification_id = notification_schemes_id["id"]
        notification_schemes = jira.get_notification_scheme(notification_id, "all")
        names.append(notification_schemes["name"])
        notification_scheme_dict = {}
        for scheme in notification_schemes["notificationSchemeEvents"]:
            notification_types = []
            for notificationType in scheme["notifications"]:
                notification_types.append(notificationType["notificationType"])
                notification_scheme_dict[scheme["event"]["name"]] = notification_types
        all_notification_schemes_dict[notification_schemes["name"]] = notification_scheme_dict

    show_diffs = False
    for i in range(len(names)):
        for j in range(len(names)):
            if names and i < j:
                if compare_dicts(
                    all_notification_schemes_dict[names[i]],
                    all_notification_schemes_dict[names[j]],
                    print_diffs=show_diffs,
                ):
                    print("| same |", names[i], " | ", names[j], "|")


if __name__ == "__main__":
    review()
