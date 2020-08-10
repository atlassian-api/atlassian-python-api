from atlassian import Jira

jira = Jira(
    url='http://localhost:8090',
    username='admin',
    password='admin')


def compare_dicts(dict1, dict2):
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
    if len(dict1) != len(dict2):
        print('(Different size')
    if count == 1:
        print('(Different: ', hint[0])

    return True


notificationscheme_dict = {}
all_notificationschemes_dict = {}

notificationschemes_ids = jira.get_notification_schemes()
names = []

for notificationschemes_id in notificationschemes_ids['values']:

    id = notificationschemes_id['id']
    notificationschemes = jira.get_notification_scheme(id, 'all')
    names.append(notificationschemes['name'])
    notificationscheme_dict = {}

    for scheme in notificationschemes['notificationSchemeEvents']:
        notificationTypes = []

        for notificationType in scheme['notifications']:
            notificationTypes.append(notificationType['notificationType'])
            notificationscheme_dict[scheme['event']['name']] = notificationTypes
    all_notificationschemes_dict[notificationschemes['name']] = notificationscheme_dict

for i in range(len(names)):
    for j in range(len(names)):
        if names and i < j:
            if compare_dicts(all_notificationschemes_dict[names[i]], all_notificationschemes_dict[names[j]]):
                print(names[i], '/', names[j])
                print('same) \n -----------------------------------------------------------------')
