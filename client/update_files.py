"""
Remove files from server
"""

import requests

from utility.utility import get_md5sum
from client.helpers import get_md5sum_mapping_server


def update_files(files, location):
    """
    List files in server

    Args:
        files (list): List of files to update
        location (str): URL of http server

    """
    # get the md5sum of files in server
    md5sum_mapping_server = get_md5sum_mapping_server(location)

    files_to_update = []
    for each_file in files:
        is_duplicate_found = False
        # check the duplicate content exists or not
        md5sum = get_md5sum(each_file)
        for key, value in md5sum_mapping_server.items():
            if md5sum == value:
                is_duplicate_found = True
                print(f"{each_file} is duplicate of {key} in server")
                headers = {"file_name": each_file, "duplicate_file": key}
                r = requests.put(location, headers=headers)
                print(r.text)
                break
        if not is_duplicate_found:
            with open(each_file, "rb") as data:
                files_to_update.append(("file", (each_file, data.read())))

    if files_to_update:
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
