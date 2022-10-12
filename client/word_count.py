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
    response = requests.get(location, params=params)
    print(response.text)
