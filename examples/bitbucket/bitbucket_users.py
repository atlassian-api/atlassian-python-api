# coding=utf-8
from atlassian import Bitbucket

bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")

data = bitbucket.get_users(user_filter="username")
print(data)
