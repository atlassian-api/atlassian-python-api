# coding=utf-8
from atlassian import CloudAdminUsers

# How to get user profile

cloud_admin_users = CloudAdminUsers(admin_api_key="admin_api_key")

cloud_admin_users.get_organizations(account_id="account_id")
