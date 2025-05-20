from atlassian import Assets

try:
    import pandas as pd
except ImportError:
    print("Please install Flask library to run this example")
    exit(1)


def delete_object(ins, object_id):
    try:
        ins.delete_object(object_id)
        print(f"Object with ID {object_id} deleted successfully.")
    except Exception as e:
        print(f"Failed to delete object with ID {object_id}: {e}")


if __name__ == "__main__":
    ins = Assets(
        url="https://jira.example.com", username="admin", token="--------------------------------", cloud=False
    )

    df = pd.read_csv("diff.csv")
    df["Internal Object ID"].drop_duplicates().apply(lambda x: delete_object(ins, x))
