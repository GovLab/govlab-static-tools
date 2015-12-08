import os
import urllib
import socket
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import posixpath
import threading

from colorama import Style

# http://stackoverflow.com/a/18858817
class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET,
                               socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


def build_request_handler(root_dir):
    class MySimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
        # This has been taken from Python 2.7.3's SimpleHTTPServer.py and
        # modified to work with a root directory instead of os.getcwd().
        def translate_path(self, path):
            """Translate a /-separated PATH to the local filename syntax.
            Components that mean special things to the local file system
            (e.g. drive or directory names) are ignored.  (XXX They should
            probably be diagnosed.)
            """
            # abandon query parameters
            path = path.split('?',1)[0]
            path = path.split('#',1)[0]
            path = posixpath.normpath(urllib.unquote(path))
            words = path.split('/')
            words = filter(None, words)
            path = root_dir
            for word in words:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir): continue
                path = os.path.join(path, word)
            return path

    return MySimpleHTTPRequestHandler


def run(root_dir, port):
    httpd = MyTCPServer(("", port), build_request_handler(root_dir))

    print Style.BRIGHT + \
          ("Starting HTTP server at port %d." % port) + \
          Style.RESET_ALL
    httpd.serve_forever()


def start(root_dir, port):
    thread = threading.Thread(target=run, kwargs=dict(
        root_dir=root_dir,
        port=port
    ))
    thread.daemon = True
    thread.start()
