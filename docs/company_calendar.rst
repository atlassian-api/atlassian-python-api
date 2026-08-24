Company Calendar for Jira
==========================

The ``CompanyCalendar`` client wraps the Company Calendar for Jira REST API
at ``rest/brizo-calendar/api/1``. See the vendor documentation for the full
reference:
https://brizoit.atlassian.net/wiki/spaces/CCJDOCS/pages/4018044966/REST+API

Authentication is done with a Bearer API token generated and assigned to one
or more calendars by an administrator.

.. code-block:: python

    from atlassian import CompanyCalendar

    # Cloud
    calendar = CompanyCalendar(
        "https://ccj.brizoit.com/ccj",
        token="API-TOKEN",
    )

    # Data Center
    calendar = CompanyCalendar(
        "https://your-jira-instance.company.com",
        token="API-TOKEN",
    )

    calendars = calendar.get_calendars()
    calendar_details = calendar.get_calendar(calendars[0]["id"])

Calendars, sources, and events can be created, updated, and deleted:

.. code-block:: python

    calendar.create_calendar(
        {
            "publicCalendar": True,
            "calendarEditable": True,
            "eventsEditable": True,
            "value": '{"name":"New public calendar","usersFromEvents":true}',
            "user": "userID",
        }
    )

    calendar.create_source(
        {
            "eventTypeId": 5,
            "calendarConfigurationId": 1959,
            "emailsEnabled": False,
            "value": '{"color":"#0fff04","name":"New source"}',
        }
    )

    calendar.create_event(
        {
            "event": {
                "summary": "All-day Rest API event",
                "eventTypeConfigId": "sourceId",
                "userKeys": ["account-id"],
                "allDayStart": "2024-09-29",
                "allDayEnd": "2024-09-29",
            },
            "mode": "add",
        }
    )

Events can be searched by date range, optionally scoped to a calendar or a
source:

.. code-block:: python

    calendar.search_events(
        {
            "startDate": 1672531200000,
            "endDate": 1680307200000,
            "calendarId": 1959,
        }
    )
