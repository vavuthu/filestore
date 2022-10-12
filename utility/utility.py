"""
Common functions which is used for both client and server
"""

import hashlib


def get_md5sum(filename):
    """
    Calculate md5sum of file

    Args:
        filename (str): Name of file

    Returns:
        str: md5sum of file

    """
    with open(filename, "rb") as fd:
        bytes = fd.read()
        md5sum = hashlib.md5(bytes).hexdigest()
        return md5sum
