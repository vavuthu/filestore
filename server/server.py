"""
server side implementation for uploading data
"""

import cgi
import json
import os
import re
import ring

from collections import Counter
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import BytesIO
from shutil import copyfile
from utility.utility import get_md5sum


class ServerHandler(SimpleHTTPRequestHandler):
    """
    HTTP request handler with GET commands.

    ServerHandler serves files from the current directory
    and its subdirectories.

    """

    def do_GET(self):
        """
        Serves a GET request.

        Default GET method returns the html page which contains the files
        and directories. Implement the customized GET suitable for the
        file store service.

        """
        response_msg = " "
        path = f"{self.translate_path(self.path)}"
        files_list = [file for file in os.listdir(path) if os.path.isfile(file)]

        if "count_words" in self.requestline:
            word_count = self.count_words(files_list)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                f"Total number of words in all files are {word_count}".encode(
                    encoding="utf_8"
                )
            )
            return

        if "frequent_words" in self.requestline:
            words_mapping = self.frequent_words(files_list)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(words_mapping).encode(encoding="utf_8"))
            return

        # calculate md5sum if header contains md5sum
        if self.headers.get("md5sum"):
            md5sum_mapping = {}
            for each_file in files_list:
                if os.path.isfile(each_file):
                    md5sum_mapping[each_file] = get_md5sum(each_file)
            response_msg += json.dumps(md5sum_mapping)
        else:
            response_msg += response_msg.join(files_list)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response_msg.encode(encoding="utf_8"))

    def frequent_words(self, files_list):
        """
        Most frequently used words in given list of files
        """
        # create empty counter
        words_mapping = Counter()

        for each_file in files_list:
            words_mapping += Counter(frequent_words_in_file(each_file))
        return dict(words_mapping)

    def count_words(self, files_list):
        """
        Count the words in given list of files
        """
        count = 0
        for each_file in files_list:
            count += count_words_in_file(each_file)
        return count

    def do_POST(self):
        """
        Serves a POST request.
        """
        # check in headers whether POST request file is duplicate in server
        duplicate_file = self.headers.get("duplicate_file")
        if duplicate_file:
            self.filecopy(duplicate_file)
            return
        else:
            response = BytesIO()
            result, message = self.upload_data()
            if result:
                self.send_response(200)
            else:
                self.send_response(500)
            response.write(message.encode("utf-8"))

        self.end_headers()
        self.wfile.write(response.getvalue())

    def upload_data(self):
        """
        writes file data to server.
        """
        response_msg = ""
        content_type, _ = cgi.parse_header(self.headers["Content-Type"])

        if content_type == "multipart/form-data":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"],
                },
            )
            if isinstance(form["file"], list):
                for record in form["file"]:
                    try:
                        open(record.filename, "wb").write(record.file.read())
                        response_msg += f"{record.filename} uploaded successfully\n"
                    except IOError:
                        return (
                            False,
                            "Upload failed, please check permissions on file store",
                        )
                    except Exception as err:
                        return False, err
            else:
                try:
                    open(form["file"].filename, "wb").write(form["file"].file.read())
                    response_msg += f"{form['file'].filename} uploaded successfully\n"
                except IOError:
                    return (
                        False,
                        "Upload failed, please check permissions on file store",
                    )
                except Exception as err:
                    return False, err

        return True, f"{response_msg}"

    def do_DELETE(self):
        """
        Serves a DELETE request
        """
        response_msg = ""
        # requestline: 'DELETE /?files_to_delete=f5&files_to_delete=f6 HTTP/1.1'
        files_to_delete = re.findall(r"=(\w+)", self.requestline)
        is_delete_failed = False
        for file in files_to_delete:
            try:
                os.remove(file)
                # delete the entry from cache
                get_md5sum.delete(file)
                count_words_in_file.delete(file)
                frequent_words_in_file.delete(file)
            except OSError as e:
                is_delete_failed = True
                response_msg += f"Error: {e.filename} - {e.strerror}\n"

        if is_delete_failed:
            self.send_response(404)
        else:
            self.send_response(200)
        print(response_msg)
        self.end_headers()
        self.wfile.write(response_msg.encode("utf-8"))

    def do_PUT(self):
        """
        Serves a PUT request
        """
        duplicate_file = self.headers.get("duplicate_file")
        if duplicate_file:
            self.filecopy(duplicate_file)
            return

        response_msg = ""
        response = BytesIO()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "PUT",
                "CONTENT_TYPE": self.headers["Content-Type"],
            },
        )
        if isinstance(form["file"], list):
            for record in form["file"]:
                try:
                    open(record.filename, "wb").write(record.file.read())
                    response_msg += f"{record.filename} updated successfully\n"
                    # delete the entry from cache, since PUT request changes the content of file
                    # which in turn changes the md5sum of a file
                    get_md5sum.delete(record.filename)
                    count_words_in_file.delete(record.filename)
                    frequent_words_in_file.delete(record.filename)
                except IOError:
                    self.send_response(500)
                    self.end_headers()
                    return
        else:
            try:
                open(form["file"].filename, "wb").write(form["file"].file.read())
                response_msg += f"{form['file'].filename} updated successfully\n"
                # delete the entry from cache, since PUT request changes the content of file
                # which in turn changes the md5sum of a file
                get_md5sum.delete(form["file"].filename)
                count_words_in_file.delete(form["file"].filename)
                frequent_words_in_file.delete(form["file"].filename)
            except IOError:
                self.send_response(500)
                self.end_headers()
                return

        response.write(response_msg.encode("utf-8"))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.getvalue())

    def filecopy(self, duplicate_file):
        """
        Copy the file
        """
        response = BytesIO()
        # For update request, there is a chance of filename and content are same, in that
        # case, update metadata for file
        if duplicate_file == self.headers["file_name"]:
            epoch_time = datetime.now().timestamp()
            os.utime(self.headers["file_name"], (epoch_time, epoch_time))
            message = f"updated metadata for {self.headers['file_name']} since filename and content are same"
        else:
            copyfile(duplicate_file, self.headers["file_name"])
            message = f"updated {self.headers['file_name']} without sending contents over network"

        response.write(message.encode("utf-8"))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.getvalue())


@ring.lru()
def count_words_in_file(filename):
    """
    Count the words in a file
    """
    with open(filename, "r") as fd:
        return len(fd.read().split())


@ring.lru()
def frequent_words_in_file(filename):
    """
    Most frequently used words in a file
    """
    words_mapping_file = {}

    with open(filename, "r") as fd:
        words = fd.read().lower().split()
        for word in words:
            if words_mapping_file.get(word):
                current_count = words_mapping_file[word] + 1
            else:
                current_count = 1
            words_mapping_file[word] = current_count
    return words_mapping_file


def run_server(server_class=HTTPServer, handler_class=ServerHandler):
    server_address = ("", 8000)
    httpd = server_class(server_address, handler_class)
    print(f"starting httpd at {server_address}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Stopping httpd...\n")
