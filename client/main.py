import argparse

from client.add_files import add_files
from client.list_files import list_files


def arg_parser():
    """
    Argument Parser

    Returns:
        object: Parsed arguments

    """
    parser = argparse.ArgumentParser(
        description="file store service that stores plain-text files",
    )
    parser.add_argument(
        "--add",
        action="store",
        nargs="+",
        required=False,
        help="upload files to http server",
    )
    parser.add_argument(
        "--ls",
        action="store_true",
        required=False,
        default=False,
        help="list files in http server",
    )
    parser.add_argument(
        "--url",
        action="store",
        required=False,
        type=str,
        default="http://0.0.0.0:8000/",
        help="list files in http server",
    )
    return parser.parse_args()


def main():
    """
    Main function
    """
    parser = arg_parser()
    store_add = parser.add
    store_ls = parser.ls
    store_location = parser.url

    if not (store_add or store_ls):
        print("At least 1 operation is required")

    if store_add:
        add_files(store_add, store_location)

    if store_ls:
        list_files(store_location)
