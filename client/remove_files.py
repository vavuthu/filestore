"""
Remove files from server
"""

import requests


def remove_files(files, location):
    """
    List files in server

    Args:
        files (list): List of files to upload
        location (str): URL of http server

    """
    params = {"files_to_delete": files}
    r = requests.delete(location, params=params)
    print(r.text)
