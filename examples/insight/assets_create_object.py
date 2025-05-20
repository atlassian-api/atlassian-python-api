from atlassian import Assets

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    assets = Assets(url="http://localhost:8080/", username="jira-administrator", password="admin")

    object_type_id = 3520  # Contract

    assets.create_object(
        object_type_id=object_type_id,
        attributes=[
            {"objectTypeAttributeId": 38, "objectAttributeValues": [{"value": "Expenses"}]},  # Contract Name
            {"objectTypeAttributeId": 46, "objectAttributeValues": [{"value": "OPEX"}]},  # Contract Type
            {"objectTypeAttributeId": 48, "objectAttributeValues": [{"value": "Expired"}]},  # Contract Status
        ],
    )
