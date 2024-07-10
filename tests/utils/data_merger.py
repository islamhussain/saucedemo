import os
import json


def merge_test_data(directory=None, file_path=None):
    merged_data = {"tests": []}

    if directory:
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                full_path = os.path.join(directory, filename)
                with open(full_path, "r") as file:
                    data = json.load(file)
                    merged_data["tests"].extend(data["tests"])
    elif file_path:
        with open(file_path, "r") as file:
            data = json.load(file)
            merged_data["tests"].extend(data["tests"])
    else:
        raise ValueError("Either directory or file_path must be provided")

    return merged_data
