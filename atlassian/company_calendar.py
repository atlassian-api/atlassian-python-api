# coding=utf-8
"""Company Calendar for Jira REST API client.

See the vendor documentation:
https://brizoit.atlassian.net/wiki/spaces/CCJDOCS/pages/4018044966/REST+API
"""

import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class CompanyCalendar(AtlassianRestAPI):
    """Client for the Company Calendar for Jira REST API.

    Company Calendar for Jira exposes its REST API below
    ``rest/brizo-calendar/api/1``. Authentication is done through a Bearer
    API token that is generated and assigned to one or more calendars by an
    administrator.

    On Cloud the base URL is fixed to
    ``https://ccj.brizoit.com/ccj/rest/brizo-calendar``, while on Data Center
    it is ``<JIRA-URL>/rest/brizo-calendar``.

    Examples
    --------
    >>> calendar = CompanyCalendar(
    ...     "https://ccj.brizoit.com/ccj",
    ...     token="API-TOKEN",
    ... )
    >>> calendar.get_calendars()
    """

    def __init__(self, *args, **kwargs):
        kwargs["api_root"] = "rest/brizo-calendar"
        super(CompanyCalendar, self).__init__(*args, **kwargs)

    def _resource_url(self, resource):
        return self.url_joiner(self.api_root, f"api/1/{resource}")

    ################################################################################################
    # Calendars
    ################################################################################################

    def get_calendars(self):
        """
        Return a list of all calendars associated with the token.

        :return: list[dict] - Calendars.
        """
        return self.get(self._resource_url("calendar"))

    def get_calendar(self, calendar_id):
        """
        Return details for a specific calendar, including permissions.

        :param calendar_id: int/str - The calendar ID.
        :return: dict - Calendar details.
        """
        return self.get(self._resource_url(f"calendar/{calendar_id}"))

    def create_calendar(self, data):
        """
        Create a new calendar.

        :param data: dict - The calendar payload. See the Company Calendar REST API
            documentation for the ``publicCalendar``/``permCalendarView``/``value`` fields
            required for public and private calendars.
        :return: dict - The created calendar.
        """
        return self.post(self._resource_url("calendar"), data=data)

    def update_calendar(self, data):
        """
        Update an existing calendar.

        Important: when updating, the full ``value`` JSON object must be provided.
        Any property that is not included will be overwritten or removed.

        :param data: dict - The calendar payload, including its ``id``.
        :return: dict - The updated calendar.
        """
        return self.put(self._resource_url("calendar"), data=data)

    def delete_calendar(self, calendar_id):
        """
        Delete the specified calendar.

        Deleting a calendar is possible only when the token has permission to delete it.

        :param calendar_id: int/str - The calendar ID.
        :return: response
        """
        return self.delete(self._resource_url(f"calendar/{calendar_id}"))

    ################################################################################################
    # Event types
    ################################################################################################

    def get_event_types(self):
        """
        Return all system and custom event types.

        :return: list[dict] - Event types.
        """
        return self.get(self._resource_url("eventypes"))

    ################################################################################################
    # Sources
    ################################################################################################

    def get_source(self, source_id):
        """
        Return details for a specific source.

        :param source_id: int/str - The source ID.
        :return: dict - Source details.
        """
        return self.get(self._resource_url(f"source/{source_id}"))

    def create_source(self, data):
        """
        Create a new source for a calendar.

        :param data: dict - The source payload, e.g. ``eventTypeId``,
            ``calendarConfigurationId``, ``emailsEnabled`` and ``value``.
        :return: dict - The created source.
        """
        return self.post(self._resource_url("source"), data=data)

    def update_source(self, data):
        """
        Update an existing source.

        Important: always send the full ``value`` JSON object. Any omitted
        property will be overwritten or removed.

        :param data: dict - The source payload, including its ``id``.
        :return: dict - The updated source.
        """
        return self.put(self._resource_url("source"), data=data)

    def delete_source(self, source_id):
        """
        Delete a source.

        Deleting a source is possible only when the token has permission to delete it.

        :param source_id: int/str - The source ID.
        :return: response
        """
        return self.delete(self._resource_url(f"source/{source_id}"))

    ################################################################################################
    # Events
    ################################################################################################

    def create_event(self, data):
        """
        Create a new event (all-day, timed or recurring).

        :param data: dict - The event payload, e.g. ``{"event": {...}, "mode": "add"}``.
        :return: dict - The created event.
        """
        return self.post(self._resource_url("event"), data=data)

    def update_event(self, data):
        """
        Update an existing event (single or recurring).

        :param data: dict - The event payload, e.g. ``{"event": {...}, "mode": "edit"}``.
        :return: dict - The updated event.
        """
        return self.put(self._resource_url("event"), data=data)

    def delete_event(self, event_id):
        """
        Delete an event.

        :param event_id: int/str - The event ID.
        :return: response
        """
        return self.delete(self._resource_url(f"event/{event_id}"))

    def delete_recurring_event(self, event_id, data):
        """
        Delete a recurring event occurrence, exception, or the entire recurrence chain.

        Depending on ``data``, this can delete the full recurring series, a single
        occurrence, or exclude a specific instance from the recurrence by adding an
        exception date. See the Company Calendar REST API documentation for the
        required ``mode``, ``select`` and ``exdate`` fields.

        :param event_id: int/str - The event ID (occurrence or parent, depending on scenario).
        :param data: dict - The deletion payload.
        :return: response
        """
        return self.delete(self._resource_url(f"event/{event_id}/recur"), data=data)

    ################################################################################################
    # Search
    ################################################################################################

    def search_events(self, data):
        """
        Search for events within a date range, optionally scoped to a calendar or source.

        :param data: dict - The search payload. Accepts either Unix timestamps
            (``startDate``/``endDate``) or ISO dates (``startDateIso``/``endDateIso``),
            combined with an optional ``calendarId`` or ``sourceId``.
        :return: dict - Paginated search results.
        """
        return self.post(self._resource_url("event/search"), data=data)
