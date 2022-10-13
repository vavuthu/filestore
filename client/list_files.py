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
    try:
        response = requests.get(location)
        if not response.ok:
            print("Unable to list files")
        # list files
        for file in response.text.split():
            print(file)
    except requests.exceptions.HTTPError as err_http:
        print(f"Http Error: {err_http}")
    except requests.exceptions.Timeout as err_timeout:
        print(f"Timeout Error: {err_timeout}")
    except requests.exceptions.ConnectionError as err_connection:
        print(f"Network Connection Error: {err_connection}")
    except requests.exceptions.RequestException as err:
        print(f"Unexpected Error: {err}")
