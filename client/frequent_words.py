"""
Most frequently used words in all the files in server
"""

import ast
import requests

from collections import Counter


def frequent_words(location, limit, order):
    """
    Most frequently used words in all the files

    Args:
        location (str): URL of http server
        limit (int): number of words to return
        order (str): Either acs ( ascending) or dsc ( descending)

    """
    params = {"frequent_words": True}
    try:
        response = requests.get(location, params=params)
    except requests.exceptions.HTTPError as err_http:
        print(f"Http Error: {err_http}")
    except requests.exceptions.Timeout as err_timeout:
        print(f"Timeout Error: {err_timeout}")
    except requests.exceptions.ConnectionError as err_connection:
        print(f"Network Connection Error: {err_connection}")
    except requests.exceptions.RequestException as err:
        print(f"Unexpected Error: {err}")

    # convert string representation of dictionary to dictionary
    words_mapping = ast.literal_eval(response.text)

    # sort the dictionary
    sorted_words_mapping = Counter(words_mapping)

    if order == "dsc":
        frequent_words_list = sorted_words_mapping.most_common()[:limit]
    else:
        frequent_words_list = sorted_words_mapping.most_common()[::-1][:limit]

    for each in frequent_words_list:
        print(f"{each[0]} : {each[1]}")
