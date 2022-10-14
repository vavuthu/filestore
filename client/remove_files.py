"""
Remove files from server
"""

import requests


def remove_files(files, location):
    """
    List files in server

    Args:
        files (list): List of files to delete
        location (str): URL of http server

    """
    params = {"files_to_delete": files}
    try:
        r = requests.delete(location, params=params)
        print(r.text)
    except requests.exceptions.HTTPError as err_http:
        print(f"Http Error: {err_http}")
    except requests.exceptions.Timeout as err_timeout:
        print(f"Timeout Error: {err_timeout}")
    except requests.exceptions.ConnectionError as err_connection:
        print(f"Network Connection Error: {err_connection}")
    except requests.exceptions.RequestException as err:
        print(f"Unexpected Error: {err}")
