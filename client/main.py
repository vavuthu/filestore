import argparse
import os

from client.add_files import add_files
from client.frequent_words import frequent_words
from client.list_files import list_files
from client.remove_files import remove_files
from client.update_files import update_files
from client.word_count import word_count
from dotenv import load_dotenv


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
        "--rm",
        action="store",
        nargs="+",
        required=False,
        help="delete files from http server",
    )
    parser.add_argument(
        "--update",
        action="store",
        nargs="+",
        required=False,
        help="delete files from http server",
    )
    parser.add_argument(
        "--wc",
        action="store_true",
        required=False,
        default=False,
        help="word count on all the files from http server",
    )
    parser.add_argument(
        "--freq_words",
        action="store_true",
        required=False,
        default=False,
        help="most frequently used words on all the files from http server",
    )
    parser.add_argument(
        "--limit",
        action="store",
        default=10,
        type=int,
        help="number of frequently used words to return from http server",
    )
    parser.add_argument(
        "--order",
        action="store",
        default="dsc",
        type=str,
        choices=["dsc", "asc"],
        help="frequently used words order by ascending(asc) or descending(dsc)",
    )
    return parser.parse_args()


def main():
    """
    Main function
    """
    load_dotenv()
    parser = arg_parser()
    store_add = parser.add
    store_ls = parser.ls
    store_rm = parser.rm
    store_update = parser.update
    store_wc = parser.wc
    store_freq_words = parser.freq_words
    store_location = os.environ.get("URL")

    if not (
        store_add
        or store_ls
        or store_rm
        or store_update
        or store_wc
        or store_freq_words
    ):
        print("At least 1 operation is required")

    if store_add:
        add_files(store_add, store_location)

    if store_ls:
        list_files(store_location)

    if store_rm:
        remove_files(store_rm, store_location)

    if store_update:
        update_files(store_update, store_location)

    if store_wc:
        word_count(store_location)

    if store_freq_words:
        frequent_words(store_location, parser.limit, parser.order)
