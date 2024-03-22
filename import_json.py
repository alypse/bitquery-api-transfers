import json


def load_json_data(file_path):
    """
    Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: JSON data as a Python dictionary.
    """
    with open(file_path) as f:
        data = json.load(f)
    return data
