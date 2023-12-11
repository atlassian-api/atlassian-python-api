from atlassian import Insight

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    ins = Insight(url="http://localhost:8080/", username="jira-administrator", password="admin")

    # Get all contracts in schema with id 51
    contracts = ins.iql("objectType=Contract", 51)

    for contract in contracts["objectEntries"]:
        print(contract)
