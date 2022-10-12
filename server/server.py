"""
server side implementation for uploading data
"""

import cgi
import json
import os

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
        files_list = os.listdir(path)

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

    def do_POST(self):
        """
        Serves a POST request.
        """
        # check in headers whether POST request file is duplicate in server
        duplicate_file = self.headers.get("duplicate_file")
        if duplicate_file:
            copyfile(duplicate_file, self.headers["file_name"])
            response = BytesIO()
            message = f"created {self.headers['file_name']} without sending contents over network"
            response.write(message.encode("utf-8"))
        else:
            result, message = self.upload_data()
            response = BytesIO()
            if result:
                response.write(message.encode("utf-8"))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.getvalue())

    def upload_data(self):
        """
        writes file data to server.
        """
        response_msg = ""
        content_type, _ = cgi.parse_header(self.headers["Content-Type"])
        # pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        # pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])

        if content_type == "multipart/form-data":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"],
                },
            )
            try:
                if isinstance(form["file"], list):
                    for record in form["file"]:
                        # check if file already exists before writing
                        if not self.is_file_exist(record.filename):
                            open(record.filename, "wb").write(record.file.read())
                            response_msg += f"{record.filename} uploaded successfully\n"
                        else:
                            response_msg += f"{record.filename} exists in server. skipping upload...\n"
                else:
                    if not self.is_file_exist(form["file"].filename):
                        open(form["file"].filename, "wb").write(
                            form["file"].file.read()
                        )
                        response_msg += (
                            f"{form['file'].filename} uploaded successfully\n"
                        )
                    else:
                        response_msg += f"{form['file'].filename} exists in server. skipping upload...\n"
            except IOError:
                return False, "Upload failed, please check permissions on file store"

        return True, f"{response_msg}"

    def is_file_exist(self, filename):
        """
        Check whether file exists or not.
        """
        if os.path.isfile(filename):
            return True


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
