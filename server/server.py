"""
server side implementation for uploading data
"""

import os

from http.server import HTTPServer, SimpleHTTPRequestHandler


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
        response_msg += response_msg.join(files_list)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response_msg.encode(encoding="utf_8"))


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
