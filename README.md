# Filestore

Filestore is a simple file store service that stores plain-text files (HTTP server and a command line client)

## Prerequisites

1. Python version >= 3.8

## Getting Started

It is recommended that you use a python virtual environment to install the
necessary dependencies in both client and server. Do below steps on both server and cient

1. Clone filestore repository from
    [https://github.com/vavuthu/filestore](https://github.com/vavuthu/filestore)
    via cmd  
    `git clone https://github.com/vavuthu/filestore.git` or  
    `git clone git@github.com:vavuthu/filestore.git`.
2. Go to filestore folder `cd filestore`.
3. Setup a python 3.8 virtual environment.
    * `python3.8 -m venv <path/to/venv>`
    * `source <path/to/venv>/bin/activate`
4. Install requirements with `pip install -r requirements.txt`

Note: Follow above steps in both client and server

## start httpd on server

1. Once virtual environment is activated and installed requirements.txt from above steps,
go to any directory which we would like to act as file store and start the httpd server
using below command. By default it will run on port 8000
     * `run-server`

## client side

Edit the .env file in filestore repository and add the server URL. Incase you are running httpd
server locally, no need to edit the file.
example: If httpd server is running on 10.x.xxx.xxx, .env looks like below

```console
$ cat .env 
URL=http://10.x.xxx.xxx:8000/
```

Once virtual environment is activated and installed requirements.txt from above steps,
use `store` command to perform file operations like ls, add, etc. Few example are below for reference

### add
Uploads multiple files to server.

1. add multiples files to server
```console
$ store --add file1 file2
file1 uploaded successfully
file2 uploaded successfully
```

2. add multiples files with few files already existed in server (skips the upload of existing files)
```console
$ store --add file1 file3 file4
file1 exists in server. skipping upload...

file3 uploaded successfully
file4 uploaded successfully
```

3. add files having same content present in server ( create files in server without sending contents to server)
```console
$ store --add dup
dup is duplicate of file3 in server
created dup without sending contents over network
```

### ls
List all the files in server

```console
$ store --ls
file1
file2
file3
file4
dup
```

### rm
Remove files from server

1. remove multiple files from server
```console
$ store --rm file1 file2
```

2. remove a file which doesn't exist on server
```console
$ store --rm file1
Error: file1 - No such file or directory
```

### update
Updates file on server, if file doesn't exist it will create new file

```console
$ store --update updatefile1 
updatefile1 updated successfully
```

### wc
Count the number of words on all files in file store

```console
$ store --wc
Total number of words in all files are 8
```

### freq_words
List the most frequent words in all the files combined. We can list by either limit (default limit is 10)
and order (dsc or asc, default value is dsc(descending))

1. List most frequent words by default values
```console
$ store --freq_words
data : 19
openshift : 14
and : 13
foundation : 11
the : 10
red : 9
hat : 9
for : 9
cluster : 7
to : 7
```

2. List most frequent words by limit
```console
$ store --freq_words --limit 3
data : 19
openshift : 14
and : 13
````

3. List most frequent words by order
```console
$ store --freq_words --limit 3 --order asc
rhacm : 1
requirements, : 1
detailed : 1
```





