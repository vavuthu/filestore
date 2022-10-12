# Filestore

Filestore is a simple file store service that stores plain-text files (HTTP server and a command line client)

## Prerequisites

1. Python version >= 3.8

## Getting Started

It is recommended that you use a python virtual environment to install the
necessary dependencies in both client and server.

1. Clone filestore repository from
    [https://github.com/vavuthu/filestore](https://github.com/vavuthu/filestore)
    via cmd `git clone git@github.com:vavuthu/filestore.git`.
2. Go to filestore folder `cd filestore`.
3. Setup a python 3.8 virtual environment.
    * `python3.8 -m venv <path/to/venv>`
    * `source <path/to/venv>/bin/activate`
4. Install requirements with `pip install -r requirements.txt`

Note: Follow above steps in both client and server

## start httpd on server

1. Once virtual environment is activated and installed requirements.txt from above steps,
go to any directory which we would like to act as file store and start the httpd server
using below command
     * `run-server`

## client side

Once virtual environment is activated and installed requirements.txt from above steps,
use `store` command to perform file operations like ls, add, etc
