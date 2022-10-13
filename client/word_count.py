"""
Count the words in all the files in server
"""

import requests


def word_count(location):
    """
    Count words in all the files

    Args:
        location (str): URL of http server

    """
    params = {"count_words": True}
    try:
        response = requests.get(location, params=params)
        print(response.text)
    except requests.exceptions.HTTPError as err_http:
        print(f"Http Error: {err_http}")
    except requests.exceptions.Timeout as err_timeout:
        print(f"Timeout Error: {err_timeout}")
    except requests.exceptions.ConnectionError as err_connection:
        print(f"Network Connection Error: {err_connection}")
    except requests.exceptions.RequestException as err:
        print(f"Unexpected Error: {err}")
