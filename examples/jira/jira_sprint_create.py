from atlassian import Jira

sprint_name = "Sprint 2"
origin_board_id = 1000
start_datetime = "2021-05-30T14:42:23.643068"
end_datetime = "2021-06-30T14:42:23.643068"
goal = "And we're out of beta, we're releasing on time."

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

# name and board_id are mandatory only
# Necessary for user to have `Manage Sprint` permission for the board
resp = jira.create_sprint(
    name=sprint_name,
    board_id=origin_board_id,
    start_date=start_datetime,
    end_date=end_datetime,
    goal=goal,
)
