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
    r = requests.put(location, files=files_to_update)
    print(r.text)
