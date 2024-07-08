# coding: utf8
from jira import JIRA as Jira
import requests
from requests.auth import HTTPBasicAuth
import json
import time

#Constants
# I'm also making 3 API calls (potentially) per loop so maybe need to only call 100 times per minute to be on the safe side
MAX_TEMPO_API_HITS_PER_MINUTE = 300
NUM_API_HITS_IN_LOOP = 3

#Globals
#I am concerned about limit throttling in Jira when we do every issue so adding some code in handle this
# Store the time when the requests are made
request_times = []
my_username = "andrew.dobbing@ezurio.com" 
from secrets import my_api_token, my_tempo_token
jira = Jira(server="https://rfpros.atlassian.net", basic_auth=(my_username, my_api_token))
#keep track of how many issues are missing the FPC
missingFPC = 0 

# Define the tempo account values that should be mapped to 'New Feature Development'
#define the tempo_account_category
tempo_to_task_category = {
    'Billable': 'Billable',
    'Capitalized New Product Development': 'New Product Development',
    'New Product Development': 'New Product Development',
    'Capitalized Feature Development': 'New Feature Development',
    'Feature Development': 'New Feature Development',
    'Overhead': 'Overhead',
    'PTO': 'PTO',    
    'Sustaining': 'Sustaining'
}



#Function Definitions

#function to retrieve available options from custom field
def get_tempo_accounts():
    
    url = "https://api.us.tempo.io/4/accounts"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {my_tempo_token}"
    }

    offset = 0
    limit = 50
    all_results = {}

    while True:

        response = requests.get(
            url,
            headers=headers,
            params={'offset': offset, 'limit': limit}
        )

        results = json.loads(response.text)['results']
        all_results.update({result['name']: result['id'] for result in results})

        # If the number of results is less than the limit, we've got all the accounts
        if len(results) < limit:
            break

        offset += limit

    return all_results

#{'self': 'https://api.tempo.io/4/accounts/176', 'key': 'L131D024', 'id': 176, 'name': 'L131D024: RM126x', 'status': 'OPEN', 'global': False, 'lead': {'self': 'https://rfpros.atlassian.net/rest/api/2/user?accountId=5cbdf7dac4966f0ffe44afcf', 'accountId': '5cbdf7dac4966f0ffe44afcf'}, 'category': {'self': 'https://api.tempo.io/4/account-categories/CAP', 'key': 'CAP', 'id': 9, 'name': 'Capitalized', 'type': {...}}, 'links': {'self': 'https://api.tempo.io/4/accounts/L131D024/links'}}


def link_tempo_account(account_key, project_id=10277):
    url = "https://api.tempo.io/4/account-links"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {my_tempo_token}"
    }

    payload = {
        "accountKey": account_key,
        "scopeId": project_id,
        "scopeType": "PROJECT"
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        json=payload
    )

    response.raise_for_status()
    return json.loads(response.text)

def add_tempo_accounts(account_key, account_name, account_lead='5cbdf7dac4966f0ffe44afcf'):
    url = "https://api.us.tempo.io/4/accounts"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {my_tempo_token}"
    }

    payload = {
        "leadAccountId": account_lead,
        "key": account_key,
        "name": account_name,
        "status": "OPEN"
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        json=payload
    )

    response.raise_for_status()
    link_tempo_account(account_key)
    return json.loads(response.text)

#function to retrieve available options from custom field
# def get_custom_field_options(field_id):
#     #url = "https://rfpros.atlassian.net/rest/api/3/field/10142/context?isAnyIssueType=true"
#     url = "https://api.us.tempo.io/4/accounts/"

#     #auth = HTTPBasicAuth(my_username, my_api_token)
    
#     headers = {
#     "Accept": "application/json",
#     "Authorization": f"Bearer {my_tempo_token}"
#     }

#     response = requests.request(
#     "GET",
#     url,
#     headers=headers
#     )    

#     print(response.text)

#     return json.loads(response.text)


# Get the  'Finance Project Code' custom field values
# `finance_project_code_options` = get_custom_field_options('customfield_10540')


#if the Parent or Child FPC field is empty then we should flag that and move on. There are probably over 1000 issues so we need to handle this
def addToLabel(new_label):

    # Retrieve current labels
    current_labels = issue.fields.labels
    
    # Check if the new label is not already in the current labels list to avoid duplicates
    if new_label not in current_labels:
        current_labels.append(new_label)
    
    # Update the issue with the new list of labels
    issue.update(fields={"labels": current_labels}, notify=False)

# Example implementation of get_task_category_id (you need to adjust it to your context)
def get_task_category_id(task_category_value):
    
    # Endpoint URL to fetch the options for theTask Category field
    #strange API - need the field ID and the screen context ID
    endpoint_url = f"https://rfpros.atlassian.net/rest/api/3/field/customfield_10889/context/11138/option"

    # Make the GET request
    response = requests.get(endpoint_url, auth=HTTPBasicAuth(my_username, my_api_token))

    # Check if the request was successful
    if response.status_code == 200:
        options = response.json()
        
        for option in options['values']:
            if option['value'] == task_category_value:
                print(f"ID: {option['id']}, Value: {option['value']}")
                return option['id'] # Return the ID of the option identified by the value
    
        print(f"No field options match: {task_category_value}.")
    else:
        print(f"Failed to fetch Task Category field options: {response.status_code}.")
        return None 
    

    # Fetch all options for customfield_10889
    # This is a placeholder; you need to implement the actual API call to fetch options
    options = [{'id': '123', 'value': 'ExampleCategory'}]  # Placeholder options
    for option in options:
        if option['value'] == task_category_value:
            return option['id']
    return None

# Define a function to handle the update logic
def update_task_category_field(current_issue, value):
    # Get the task category value from the mapping, defaulting to the original value if not found
    task_category_value = tempo_to_task_category.get(value, value)

    # Assuming you have a function to fetch the correct ID for a given task category value
    task_category_id = get_task_category_id(task_category_value) 

    if task_category_id:

        # Update the issue with the valid option ID or name
        issue.update(fields={'customfield_10889': {'id': task_category_id}}, notify=False)
    else:
        # Handle cases where no valid mapping is found
        print(f"No valid option found for {task_category_value}")



#start of the entry point

# Can only return up to 100 issues at a time so need to loop through all issues

issues = []
startAt = 0
maxResults = 100 #looks like the maximum the API will return is 100 and not 1000
#Get all issues in the project
# we could rate limit but inreality there are only about 12000 issue in the project so we will call <130 times
# in total so we should be fine
if True:
    jql_query = 'project = "PROD" AND issuetype NOT IN ("Test", "Test Execution", "Test Plan", "Test Set", "Sub Test Execution")'
    while True:
        chunk = jira.search_issues(jql_query, startAt=startAt, maxResults=maxResults)
        if len(chunk) == 0:
            # If no more issues are returned, we're done.
            break
        issues.extend(chunk)
        startAt += maxResults
        print(f"Gathering issues from {startAt}")

else:
    #While testing we will use one issue
    issues = jira.search_issues('key = "PROD-8932"')

#get all the account currrently in place - get them again if we add one - cuts don calls to the API. 

all_Current_accounts = get_tempo_accounts()
issues_processed = 0

for issue in issues:
    issues_processed += 1
    print(f"Processing issue number {issues_processed} : {issue.key}")

    # If there are more than 300 requests in the last 60 seconds
    if len(request_times) >= MAX_TEMPO_API_HITS_PER_MINUTE/NUM_API_HITS_IN_LOOP:
        # Get the time of the first request
        first_request_time = request_times[0]

        # Calculate how much time has passed since the first request
        time_since_first_request = time.time() - first_request_time

        # If less than 60 seconds have passed
        if time_since_first_request < 60:
            # Sleep until 60 seconds have passed
            time.sleep(60 - time_since_first_request)

        # Remove the first request time from the list
        request_times.pop(0)

    #before I bother about FPC I should copy the Account field into the Task Category field
    # Get the value of the 'Tempo Account' field
    tempo_account = issue.fields.customfield_10142
    #put that value into the Task Category field
    #if the tempo_account is Capitalized Feature or Feature Development then it should be New Feature Development
    # Check if the tempo account is not None
    if tempo_account is None:
        print(f"Issue {issue.key} missing 'Tempo Account'")
        addToLabel("MissingTempoAccount")
        continue

    if tempo_account is not None and tempo_account.value in tempo_to_task_category:
        # Call the function with the tempo account value
        update_task_category_field(issue, tempo_account.value)
    else:
        print(f"Tempo Account field already updated {issue.key}")
        
    #now move onto the FPC
    # Get the value of the 'Finance Project Code' field
    finance_project_code = issue.fields.customfield_10540

    if finance_project_code is None:
        print(f"Issue {issue.key} missing 'Finance Project Code'")
        missingFPC += 1
        # Update issue label with this new information 
        addToLabel("MissingFPCParent")
        continue

    # get parent value
    parent_value = finance_project_code.value
    
    try:
        #attempt to get the child value
       child_value = finance_project_code.child.value
    except:
        print(f"Issue {issue.key} missing 'Child field of FPC'")
        # Update issue label with this new information
        addToLabel("MissingFPCChild")
        continue

    # Combine parent and child values into a single string, or handle as needed
    #parent_value = parent_value.strip()
    #child_code = child_value.split(':')[0].strip()
    #child_string = child_value.split(':')[1].strip()
    #combined_value = f"{parent_value}{child_code}: {child_string}" 

    parent_value = parent_value.strip()
    parts = child_value.split(':', 1)
    child_code = parts[0].strip()  # Everything before the first colon
    child_string = parts[1].strip() if len(parts) > 1 else ''  # Everything after the first colon, including any additional colons
    combined_value = f"{parent_value}{child_code}: {child_string}"

    # Remove the first character if it is duplicated
    if combined_value[0:2] in ['RR', 'CC']:
        combined_value=combined_value[1:]
    elif combined_value[0:3] in ['000']:
        combined_value="000: Overhead & Admin" #fix the overhead and admin parsing

    combined_value = combined_value.strip()

    #print(f"The FPC is '{combined_value}'")

    # Get the options of the 'Tempo Account' field
    #tempo_account_field = get_custom_field_options('customfield_10142')

    # Get the Tempo Account ID for the combined value - the original code called the get_tempo_accounts() function to check 
    # andfor the existence of the account and then againget the key ID. Changed it to make one call to limit the 
    # number of API calls we are making.   
    # we could do this at the start but its possible a new account will get added during the call 
    # to all the issues, so it is safer to grab the current tempo accounts every tome we access an issue
    #all_Current_accounts = get_tempo_accounts()
    if not combined_value in all_Current_accounts:
        print(f"Adding tempo Account: {combined_value}")
        account_key = combined_value.split(':')[0]
        account_key = account_key.strip()
        add_tempo_accounts(account_key, combined_value)
        #get accounts again now this  new ID has been added
        all_Current_accounts = get_tempo_accounts()
        key_id = all_Current_accounts[combined_value]
    else:
        key_id = all_Current_accounts[combined_value]

    # Set the value of the 'Tempo Account' field to the combined value 
    issue.update(fields={'customfield_10142': key_id}, notify=False)
    # jira.update_issue_field(issue["key"], {'customfield_10142': {'value': key_id}})

        # Add the current request time to the list
    request_times.append(time.time())

print(f"Number of issues missing the FPC: {missingFPC}" )