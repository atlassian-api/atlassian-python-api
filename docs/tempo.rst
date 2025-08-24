Tempo API
=========

The Tempo API client provides access to both Tempo Cloud and Tempo Server APIs
within Atlassian instances.

Overview
--------

This implementation provides two main client types:

- **TempoCloud**: For Tempo Cloud instances (hosted by Atlassian)
- **TempoServer**: For Tempo Server instances (self-hosted)

The Tempo Cloud client is based on the official OpenAPI specification,
while the Tempo Server client provides access to various server-side API
modules.

Installation
------------

The Tempo clients are included with the main atlassian-python-api package:

.. code-block:: python

    from atlassian import TempoCloud, TempoServer

Tempo Cloud
-----------

The Tempo Cloud client provides access to Tempo's cloud-based time tracking
and project management capabilities.

Basic Usage
-----------
Initialize the Tempo Cloud client:

.. code-block:: python

    tempo = TempoCloud(
        url="https://your-domain.atlassian.net",
        token="your-tempo-api-token",
        cloud=True
    )

### Authentication

Tempo Cloud uses API tokens for authentication. Generate a token from your
Tempo Cloud settings:

1. Go to your Tempo Cloud instance
2. Navigate to **Settings** → **Integrations** → **API Keys**
3. Create a new API key
4. Use the generated token in your client initialization

### API Endpoints

The Tempo Cloud client provides access to the following endpoints:

#### Account Management

.. code-block:: python

    # Get all accounts
    accounts = tempo.get_accounts()

    # Get specific account
    account = tempo.get_account(account_id)

    # Create new account
    new_account = tempo.create_account({
        "name": "Client Project",
        "key": "CLIENT",
        "status": "ACTIVE"
    })

    # Update account
    updated_account = tempo.update_account(account_id, {
        "name": "Updated Project Name"
    })

    # Delete account
    tempo.delete_account(account_id)

Worklog Management
------------------
.. code-block:: python

    # Get all worklogs
    worklogs = tempo.get_worklogs()

    # Get specific worklog
    worklog = tempo.get_worklog(worklog_id)

    # Create new worklog
    new_worklog = tempo.create_worklog({
        "issueKey": "PROJ-123",
        "timeSpentSeconds": 3600,  # 1 hour
        "dateCreated": "2024-01-15",
        "description": "Development work"
    })

    # Update worklog
    updated_worklog = tempo.update_worklog(worklog_id, {
        "timeSpentSeconds": 7200  # 2 hours
    })

    # Delete worklog
    tempo.delete_worklog(worklog_id)

Schedule Management
-------------------
.. code-block:: python

    # Get all schedules
    schedules = tempo.get_schedules()

    # Get specific schedule
    schedule = tempo.get_schedule(schedule_id)

    # Create new schedule
    new_schedule = tempo.create_schedule({
        "name": "Flexible Schedule",
        "type": "FLEXIBLE"
    })

    # Update schedule
    updated_schedule = tempo.update_schedule(schedule_id, {
        "name": "Updated Schedule Name"
    })

    # Delete schedule
    tempo.delete_schedule(schedule_id)

User Management
---------------
.. code-block:: python

    # Get all users
    users = tempo.get_users()

    # Get specific user
    user = tempo.get_user(user_id)

    # Get user's schedule
    user_schedule = tempo.get_user_schedule(user_id)

    # Get user's worklogs
    user_worklogs = tempo.get_user_worklogs(user_id)

Team Management
---------------
.. code-block:: python

    # Get all teams
    teams = tempo.get_teams()

    # Get specific team
    team = tempo.get_team(team_id)

    # Create new team
    new_team = tempo.create_team({
        "name": "Development Team",
        "description": "Software development team"
    })

    # Update team
    updated_team = tempo.update_team(team_id, {
        "name": "Updated Team Name"
    })

    # Delete team
    tempo.delete_team(team_id)

    # Get team members
    team_members = tempo.get_team_members(team_id)

    # Add member to team
    tempo.add_team_member(team_id, user_id)

    # Remove member from team
    tempo.remove_team_member(team_id, user_id)

Project Management
------------------
.. code-block:: python

    # Get all projects
    projects = tempo.get_projects()

    # Get specific project
    project = tempo.get_project(project_id)

    # Get project worklogs
    project_worklogs = tempo.get_project_worklogs(project_id)

Activity Management
-------------------
.. code-block:: python

    # Get all activities
    activities = tempo.get_activities()

    # Get specific activity
    activity = tempo.get_activity(activity_id)

    # Create new activity
    new_activity = tempo.create_activity({
        "name": "Code Review",
        "description": "Reviewing code changes and providing feedback"
    })

    # Update activity
    updated_activity = tempo.update_activity(activity_id, {
        "name": "Updated Activity Name"
    })

    # Delete activity
    tempo.delete_activity(activity_id)

Customer Management
-------------------
.. code-block:: python

    # Get all customers
    customers = tempo.get_customers()

    # Get specific customer
    customer = tempo.get_customer(customer_id)

    # Create new customer
    new_customer = tempo.create_customer({
        "name": "Acme Corporation",
        "description": "Enterprise software client"
    })

    # Update customer
    updated_customer = tempo.update_customer(customer_id, {
        "name": "Updated Customer Name"
    })

    # Delete customer
    tempo.delete_customer(customer_id)

Holiday Management
------------------
.. code-block:: python

    # Get all holidays
    holidays = tempo.get_holidays()

    # Get specific holiday
    holiday = tempo.get_holiday(holiday_id)

    # Create new holiday
    new_holiday = tempo.create_holiday({
        "name": "Christmas Day",
        "date": "2024-12-25",
        "description": "Company holiday"
    })

    # Update holiday
    updated_holiday = tempo.update_holiday(holiday_id, {
        "name": "Updated Holiday Name"
    })

    # Delete holiday
    tempo.delete_holiday(holiday_id)

Report Generation
-----------------
.. code-block:: python

    # Generate report
    report = tempo.generate_report("timesheet", {
        "dateFrom": "2024-01-01",
        "dateTo": "2024-01-31"
    })

    # Check report status
    status = tempo.get_report_status(report_id)

    # Download report
    report_data = tempo.download_report(report_id)

Utility Methods
---------------
.. code-block:: python

    # Get API metadata
    metadata = tempo.get_metadata()

    # Check API health
    health = tempo.get_health()

Tempo Server
------------

The Tempo Server client provides access to various server-side API modules
for self-hosted Tempo instances.

Basic Usage
-----------
Initialize the base Tempo Server client:

.. code-block:: python

    tempo = TempoServer(
        url="https://your-tempo-server.com",
        token="your-tempo-api-token",
        cloud=False
    )

Specialized Client Classes
---------------------------
For specific functionality, use the specialized client classes:

Accounts API
------------
.. code-block:: python

    from atlassian.tempo import TempoServerAccounts

    accounts_client = TempoServerAccounts(
        url="https://your-tempo-server.com",
        token="your-tempo-api-token"
    )

    # Get all accounts
    accounts = accounts_client.get_accounts()

    # Create new account
    new_account = accounts_client.create_account({
        "name": "New Account",
        "key": "NEW"
    })

Teams API
---------
.. code-block:: python

    from atlassian.tempo import TempoServerTeams

    teams_client = TempoServerTeams(
        url="https://your-tempo-server.com",
        token="your-tempo-api-token"
    )

    # Get all teams
    teams = teams_client.get_teams()

    # Create new team
    new_team = teams_client.create_team({
        "name": "New Team",
        "description": "Team description"
    })

    # Add member to team
    teams_client.add_team_member(team_id, user_id)

Planner API
-----------
.. code-block:: python

    from atlassian.tempo import TempoServerPlanner

    planner_client = TempoServerPlanner(
        url="https://your-tempo-server.com",
        token="your-tempo-api-token"
    )

    # Get all plans
    plans = planner_client.get_plans()

    # Create new plan
    new_plan = planner_client.create_plan({
        "name": "New Plan",
        "description": "Plan description"
    })

    # Get plan assignments
    assignments = planner_client.get_plan_assignments(plan_id)

Budgets API
-----------
.. code-block:: python

    from atlassian.tempo import TempoServerBudgets

    budgets_client = TempoServerBudgets(
        url="https://your-tempo-server.com",
        token="your-tempo-api-token"
    )

    # Get all budgets
    budgets = budgets_client.get_budgets()

    # Create new budget
    new_budget = budgets_client.create_budget({
        "name": "New Budget",
        "amount": 10000
    })

    # Get budget allocations
    allocations = budgets_client.get_budget_allocations(budget_id)

Timesheets API
--------------
.. code-block:: python

    from atlassian.tempo import TempoServerTimesheets

    timesheets_client = TempoServerTimesheets(
        url="https://your-tempo-server.com",
        token="your-tempo-api-token"
    )

    # Get all timesheets
    timesheets = timesheets_client.get_timesheets()

    # Create new timesheet
    new_timesheet = timesheets_client.create_timesheet({
        "name": "New Timesheet",
        "userId": 1
    })

    # Submit timesheet for approval
    timesheets_client.submit_timesheet(timesheet_id)

    # Approve timesheet
    timesheets_client.approve_timesheet(timesheet_id)

    # Reject timesheet
    timesheets_client.reject_timesheet(timesheet_id, "Invalid entries")

Servlet API
-----------
.. code-block:: python

    from atlassian.tempo import TempoServerServlet

    servlet_client = TempoServerServlet(
        url="https://your-tempo-server.com",
        token="your-tempo-api-token"
    )

    # Get all worklogs
    worklogs = servlet_client.get_worklogs()

    # Create new worklog
    new_worklog = servlet_client.create_worklog({
        "issueKey": "TEST-1",
        "timeSpentSeconds": 3600
    })

    # Get worklog attributes
    attributes = servlet_client.get_worklog_attributes(worklog_id)

    # Update worklog attributes
    servlet_client.update_worklog_attributes(worklog_id, {
        "attribute1": "value1"
    })

Events API
----------
.. code-block:: python

    from atlassian.tempo import TempoServerEvents

    events_client = TempoServerEvents(
        url="https://your-tempo-server.com",
        token="your-tempo-api-token"
    )

    # Get all events
    events = events_client.get_events()

    # Create new event
    new_event = events_client.create_event({
        "type": "worklog_created",
        "data": {"worklogId": 1}
    })

    # Get event subscriptions
    subscriptions = events_client.get_event_subscriptions()

    # Create event subscription
    new_subscription = events_client.create_event_subscription({
        "eventType": "worklog_created",
        "url": "https://webhook.url"
    })

API Configuration
-----------------
Both Cloud and Server clients support various configuration options:

.. code-block:: python

    tempo = TempoCloud(
        url="https://your-domain.atlassian.net",
        token="your-tempo-api-token",
        cloud=True,
        timeout=75,
        verify_ssl=True,
        proxies={"http": "http://proxy:8080"},
        backoff_and_retry=True,
        max_backoff_retries=1000
    )

Regional Endpoints
------------------
For Tempo Cloud, you can use regional endpoints:

- **Europe**: `https://api.eu.tempo.io`
- **Americas**: `https://api.us.tempo.io`
- **Global**: `https://api.tempo.io`

.. code-block:: python

    # For European clients
    tempo_eu = TempoCloud(
        url="https://api.eu.tempo.io",
        token="your-tempo-api-token"
    )

    # For American clients
    tempo_us = TempoCloud(
        url="https://api.us.tempo.io",
        token="your-tempo-api-token"
    )

Error Handling
--------------
Both clients include proper error handling for common HTTP status codes:

.. code-block:: python

    try:
        accounts = tempo.get_accounts()
    except Exception as e:
        if "401" in str(e):
            print("Authentication failed. Check your API token.")
        elif "403" in str(e):
            print("Access denied. Check your permissions.")
        elif "404" in str(e):
            print("Resource not found.")
        elif "429" in str(e):
            print("Rate limited. Wait before retrying.")
        else:
            print(f"Unexpected error: {e}")

Rate Limiting
-------------
Both Tempo Cloud and Server APIs have rate limiting. The clients automatically
handle retries for rate-limited requests (status code 429).

Examples
--------

See the `examples/tempo/` directory for complete working examples:

- `tempo_cloud_example.py` - Cloud API usage
- `tempo_server_example.py` - Server API usage
- `tempo_integration_example.py` - Combined usage

API Reference
-------------

For detailed API documentation, visit:

- **Tempo Cloud**: `Tempo Cloud API Documentation <https://apidocs.tempo.io/>`_
- **Tempo Server**: `Tempo Server API Documentation <https://www.tempo.io/server-api-documentation>`_

Class Reference
---------------

.. autoclass:: atlassian.tempo.TempoCloud
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: atlassian.tempo.TempoServer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: atlassian.tempo.TempoServerAccounts
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: atlassian.tempo.TempoServerTeams
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: atlassian.tempo.TempoServerPlanner
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: atlassian.tempo.TempoServerBudgets
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: atlassian.tempo.TempoServerTimesheets
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: atlassian.tempo.TempoServerServlet
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: atlassian.tempo.TempoServerEvents
   :members:
   :undoc-members:
   :show-inheritance:
