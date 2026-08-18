from unittest.mock import patch

from atlassian import CompanyCalendar


def test_company_calendar_uses_brizo_calendar_api_root():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    assert calendar.api_root == "rest/brizo-calendar"


def test_get_calendars():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    with patch.object(calendar, "get", return_value=[]) as get:
        assert calendar.get_calendars() == []
    get.assert_called_once_with("rest/brizo-calendar/api/1/calendar")


def test_get_calendar():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    with patch.object(calendar, "get", return_value={"id": 1959}) as get:
        assert calendar.get_calendar(1959) == {"id": 1959}
    get.assert_called_once_with("rest/brizo-calendar/api/1/calendar/1959")


def test_create_calendar():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    payload = {"publicCalendar": True, "value": "{}", "user": "userID"}
    with patch.object(calendar, "post", return_value={"id": 1}) as post:
        assert calendar.create_calendar(payload) == {"id": 1}
    post.assert_called_once_with("rest/brizo-calendar/api/1/calendar", data=payload)


def test_update_calendar():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    payload = {"id": 1959, "value": "{}"}
    with patch.object(calendar, "put", return_value=payload) as put:
        assert calendar.update_calendar(payload) == payload
    put.assert_called_once_with("rest/brizo-calendar/api/1/calendar", data=payload)


def test_delete_calendar():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    with patch.object(calendar, "delete", return_value={}) as delete:
        assert calendar.delete_calendar(1959) == {}
    delete.assert_called_once_with("rest/brizo-calendar/api/1/calendar/1959")


def test_get_event_types():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    with patch.object(calendar, "get", return_value=[]) as get:
        assert calendar.get_event_types() == []
    get.assert_called_once_with("rest/brizo-calendar/api/1/eventypes")


def test_get_source():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    with patch.object(calendar, "get", return_value={"id": 5655}) as get:
        assert calendar.get_source(5655) == {"id": 5655}
    get.assert_called_once_with("rest/brizo-calendar/api/1/source/5655")


def test_create_source():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    payload = {"eventTypeId": 5, "calendarConfigurationId": 1959, "value": "{}"}
    with patch.object(calendar, "post", return_value={"id": 1}) as post:
        assert calendar.create_source(payload) == {"id": 1}
    post.assert_called_once_with("rest/brizo-calendar/api/1/source", data=payload)


def test_update_source():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    payload = {"id": 5655, "value": "{}"}
    with patch.object(calendar, "put", return_value=payload) as put:
        assert calendar.update_source(payload) == payload
    put.assert_called_once_with("rest/brizo-calendar/api/1/source", data=payload)


def test_delete_source():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    with patch.object(calendar, "delete", return_value={}) as delete:
        assert calendar.delete_source(5655) == {}
    delete.assert_called_once_with("rest/brizo-calendar/api/1/source/5655")


def test_create_event():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    payload = {"event": {"summary": "Test event"}, "mode": "add"}
    with patch.object(calendar, "post", return_value={"id": 1}) as post:
        assert calendar.create_event(payload) == {"id": 1}
    post.assert_called_once_with("rest/brizo-calendar/api/1/event", data=payload)


def test_update_event():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    payload = {"event": {"id": 1}, "mode": "edit"}
    with patch.object(calendar, "put", return_value=payload) as put:
        assert calendar.update_event(payload) == payload
    put.assert_called_once_with("rest/brizo-calendar/api/1/event", data=payload)


def test_delete_event():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    with patch.object(calendar, "delete", return_value={}) as delete:
        assert calendar.delete_event(60709) == {}
    delete.assert_called_once_with("rest/brizo-calendar/api/1/event/60709")


def test_delete_recurring_event():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    payload = {"event": {"eventTypeConfigId": 5655}, "select": "current", "exdate": "20240906"}
    with patch.object(calendar, "delete", return_value={}) as delete:
        assert calendar.delete_recurring_event(60707, payload) == {}
    delete.assert_called_once_with("rest/brizo-calendar/api/1/event/60707/recur", data=payload)


def test_search_events():
    calendar = CompanyCalendar("https://ccj.brizoit.com/ccj", token="API-TOKEN")
    payload = {"startDate": 1672531200000, "endDate": 1680307200000, "calendarId": 1959}
    with patch.object(calendar, "post", return_value={"total": 0, "values": []}) as post:
        assert calendar.search_events(payload) == {"total": 0, "values": []}
    post.assert_called_once_with("rest/brizo-calendar/api/1/event/search", data=payload)
