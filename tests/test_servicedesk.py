# coding: utf8
import sys

import pytest

from atlassian import ServiceDesk

SERVICEDESK = None
try:
    from .mockup import mockup_server

    SERVICEDESK = ServiceDesk(
        "{}/servicedesk".format(mockup_server()), username="username", password="password", cloud=True
    )
except ImportError:
    pass


@pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
class TestBasic:
    def test_create_customer(self):
        result = SERVICEDESK.create_customer("{displayName}", "{emailAddress}")["emailAddress"]
        assert result == "{emailAddress}", "Result of [create_customer()]"

    def test_get_organisations(self):
        result = [x["name"] for x in SERVICEDESK.get_organisations()["values"]]
        assert result == ["Charlie Cakes Franchises"], "Result of [get_organisations()]"

    def test_get_organizations(self):
        result = [x["name"] for x in SERVICEDESK.get_organizations()["values"]]
        assert result == ["Charlie Cakes Franchises"], "Result of [get_organizations()]"

    def test_get_organisations_servicedesk_id(self):
        result = [x["name"] for x in SERVICEDESK.get_organisations(service_desk_id="{serviceDeskId}")["values"]]
        assert result == [
            "Charlie Cakes Franchises",
            "Atlas Coffee Co",
            "The Adjustment Bureau",
        ], "Result of [get_organisations(service_desk_id)]"

    def test_get_organizations_servicedesk_id(self):
        result = [x["name"] for x in SERVICEDESK.get_organizations(service_desk_id="{serviceDeskId}")["values"]]
        assert result == [
            "Charlie Cakes Franchises",
            "Atlas Coffee Co",
            "The Adjustment Bureau",
        ], "Result of [get_organizations(service_desk_id)]"

    def test_get_organization(self):
        result = SERVICEDESK.get_organization("{organizationId}")
        assert result["name"] == "Charlie Cakes Franchises", "Result of [test_get_organization(...)]"

    def test_get_users_in_organization(self):
        result = [x["emailAddress"] for x in SERVICEDESK.get_users_in_organization("{organizationId}")["values"]]
        assert result == ["fred@example.com", "bob@example.com"], "Result of [get_users_in_organization(...)]"

    def test_create_organization(self):
        result = SERVICEDESK.create_organization("Charlie Chocolate Franchises")
        assert result["id"] == "2", "Result of [create_organization(...)]"

    def test_add_organization(self):
        result = SERVICEDESK.add_organization("{serviceDeskId}", "{organizationId}")
        assert result is None, "Result of [add_organization(...)]"

    def test_remove_organization(self):
        result = SERVICEDESK.remove_organization("{serviceDeskId}", "{organizationId}")
        assert result is None, "Result of [remove_organization(...)]"

    def test_delete_organization(self):
        result = SERVICEDESK.delete_organization("{organizationId}")
        assert result is None, "Result of [delete_organization(...)]"

    def test_add_users_to_organization(self):
        result = SERVICEDESK.add_users_to_organization(
            "{organizationId}", account_list=["{accountId1}", "{accountId2}"]
        )
        assert result is None, "Result of [add_users_to_organization(...)]"

    def test_remove_users_from_organization(self):
        result = SERVICEDESK.remove_users_from_organization(
            "{organizationId}", account_list=["{accountId1}", "{accountId2}"]
        )
        assert result is None, "Result of [remove_users_from_organization(...)]"

    def test_get_customers(self):
        result = [x["emailAddress"] for x in SERVICEDESK.get_customers("{serviceDeskId}", query=None)["values"]]
        assert result == ["fred@example.com"], "Result of [remove_users_from_organization(...)]"

    def test_add_customers(self):
        result = SERVICEDESK.add_customers("{serviceDeskId}", list_of_accountids=["{accountId1}", "{accountId2}"])
        assert result is None, "Result of [remove_users_from_organization(...)]"

    def test_remove_customers(self):
        result = SERVICEDESK.remove_customers("{serviceDeskId}", list_of_accountids=["{accountId1}", "{accountId2}"])
        assert result is None, "Result of [remove_users_from_organization(...)]"
