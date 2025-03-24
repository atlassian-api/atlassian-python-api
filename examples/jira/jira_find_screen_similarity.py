import logging

from atlassian import Jira

"""
    That example shows how to find the same screen fields based on fields number or hash of orders.
    used python 3 string forms f'{variable}'
"""

logging.basicConfig(level=logging.ERROR)

jira = Jira(url="jira.example.com", username="username", password="********", timeout=10)


def extract_count(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(json["available_fields_count"])
    except KeyError:
        return 0


all_screens = jira.get_all_screens()
screens = list()
count_fields_per_screen = list()
hashes = list()
for screen in all_screens:
    screen_id = screen.get("id")
    available_screen_fields = jira.get_all_available_screen_fields(screen_id=screen_id)
    field_ids = [x.get("id") for x in available_screen_fields]
    number_fields = len(available_screen_fields)
    hash_field = hash(tuple(field_ids))
    hashes.append(hash_field)
    screens.append(
        {
            "screen_id": screen_id,
            "available_fields_count": number_fields,
            "available_fields_hash": hash_field,
            "available_fields": field_ids,
        }
    )
    count_fields_per_screen.append(number_fields)
    print(f"Number of available screen fields {number_fields} for screen with name  {screen.get('name')}")

screens.sort(key=extract_count, reverse=True)
flipped_fields = {}

print("The same screen of fields based on the count")
for x in screens:
    if count_fields_per_screen.count(x["available_fields_count"]) > 1:
        print(f"Please, check {jira.url}/secure/admin/ConfigureFieldScreen.jspa?id={x['screen_id']}")

print(("=" * 12))
print("The same field screens based on the hash")
for x in screens:
    if hashes.count(x["available_fields_hash"]) > 1:
        print(f"Please, check {jira.url}/secure/admin/ConfigureFieldScreen.jspa?id={x['screen_id']}")
