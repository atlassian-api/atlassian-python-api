# coding: utf8
from atlassian import Confluence

confluence = Confluence(
    url='http://localhost:8090',
    username='admin',
    password='admin')
# this example related get all user from group e.g. group_name
group_name = 'confluence-users'
flag = True
i = 0
limit = 50
result = []
while flag:
    response = confluence.get_group_members(group_name=group_name, start=i * limit, limit=limit)
    if response and len(response):
        i += 1
        result.append(response)
    else:
        flag = False
print(result)
