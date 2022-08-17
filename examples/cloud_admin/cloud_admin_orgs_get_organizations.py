# coding=utf-8
from atlassian import CloudAdminOrgs

# How to get organizations

cloud_admin_orgs = CloudAdminOrgs(admin_api_key="admin_api_key")

cloud_admin_orgs.get_organizations()
