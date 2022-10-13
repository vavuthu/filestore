"""
Remove files from server
"""

import requests


def update_files(files, location):
    """
    List files in server

    Args:
        files (list): List of files to upload
        location (str): URL of http server

    """
    files_to_update = []
    for each_file in files:
        with open(each_file, "rb") as data:
            files_to_update.append(("file", (each_file, data.read())))
    try:
        r = requests.put(location, files=files_to_update)
        print(r.text)
    except requests.exceptions.HTTPError as err_http:
        print(f"Http Error: {err_http}")
    except requests.exceptions.Timeout as err_timeout:
        print(f"Timeout Error: {err_timeout}")
    except requests.exceptions.ConnectionError as err_connection:
        print(f"Network Connection Error: {err_connection}")
    except requests.exceptions.RequestException as err:
        print(f"Unexpected Error: {err}")
