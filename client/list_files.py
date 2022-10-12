"""
List all files in server
"""

import requests


def list_files(location):
    """
    List files in server

    Args:
        location (str): URL of http server

    """
    # get request to list files
    response = requests.get(location)
    if not response.ok:
        print("Unable to list files")

    # list files
    for file in response.text.split():
        print(file)
