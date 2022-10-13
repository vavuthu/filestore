"""
Upload files to http server
"""

import json
import requests

from utility.utility import get_md5sum


def add_files(files, location):
    """
    Upload files to server

    Args:
        files (list): List of files to upload
        location (str): URL of http server

    """
    # get the md5sum of files in server
    headers = {"md5sum": "True"}
    response = requests.get(location, headers=headers)
    # convert string representation of dictionary to dictionary
    md5sum_mapping_server = json.loads(response.text)

    files_to_upload = []
    for each_file in files:
        is_duplicate_found = False
        # check whether file exists in server or not here since checking on
        # server side needs sending data over network
        if each_file in md5sum_mapping_server.keys():
            is_duplicate_found = True
            print(f"{each_file} exists in server. skipping upload...\n")
            continue

        # check the duplicate content exists or not
        md5sum = get_md5sum(each_file)
        for key, value in md5sum_mapping_server.items():
            if md5sum == value:
                is_duplicate_found = True
                print(f"{each_file} is duplicate of {key} in server")
                headers = {"file_name": each_file, "duplicate_file": key}
                r = requests.post(location, headers=headers)
                print(r.text)
                break

        if not is_duplicate_found:
            with open(each_file, "rb") as data:
                files_to_upload.append(("file", (each_file, data.read())))

    if files_to_upload:
        try:
            r = requests.post(location, files=files_to_upload)
            print(r.text)
        except requests.exceptions.HTTPError as err_http:
            print(f"Http Error: {err_http}")
        except requests.exceptions.Timeout as err_timeout:
            print(f"Timeout Error: {err_timeout}")
        except requests.exceptions.ConnectionError as err_connection:
            print(f"Network Connection Error: {err_connection}")
        except requests.exceptions.RequestException as err:
            print(f"Unexpected Error: {err}")
