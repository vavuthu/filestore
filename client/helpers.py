import json
import requests


def get_md5sum_mapping_server(location):
    """
    Gets the MD5sum for all files in server

    Args:
        location (url): URL of httpd server

    Returns:
        dict: Dictionary of md5sums with key as filename and value as md5sum
           e.g:{
               "f1": "d41d8cd98f00b204e9800998ecf8427e",
               "f2": "d41d8cd98f00b204e9800998ecf8427e",
               "f3": "d41d8cd98f00b204e9800998ecf8427e"
               }

    """
    # get the md5sum of files in server
    # since cache is implemented in server, overhead will be very minimal
    headers = {"md5sum": "True"}
    response = requests.get(location, headers=headers)
    # convert string representation of dictionary to dictionary
    md5sum_mapping_server = json.loads(response.text)
    return md5sum_mapping_server
