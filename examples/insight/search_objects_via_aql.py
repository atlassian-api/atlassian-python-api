from atlassian import Insight


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    ins = Insight(
        url="https://sitename.atlassian.net/",
        username="email@email.com",
        password="api_key",
        cloud=True,
    )

    # Get all object in object schema Test
    insight_objects = ins.aql("objectSchema=Test")

    for insight_object in insight_objects["values"]:
        print(insight_object)
