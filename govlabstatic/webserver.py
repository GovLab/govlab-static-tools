import os
import urllib
import urllib2
import socket
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import posixpath
import threading
import time
import traceback

from colorama import Style

class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        # http://stackoverflow.com/a/18858817
        self.socket.setsockopt(socket.SOL_SOCKET,
                               socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def handle_error(self, request, client_address):
        # Suppress spurious errors raised when we spider the site
        # and prematurely abort requests, etc.
        tb = traceback.format_exc()
        spurious_errors = [
            # Windows
            'An established connection was aborted',
            'An existing connection was forcibly closed',
            # Unix
            'Broken pipe',
        ]
        for error in spurious_errors:
            if error in tb:
                return
        SocketServer.TCPServer.handle_error(self, request, client_address)


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

        def log_message(self, format, *args):
            # Suppress logging.
            pass

    return MySimpleHTTPRequestHandler


def run(root_dir, port):
    httpd = MyTCPServer(("", port), build_request_handler(root_dir))

    print Style.BRIGHT + \
          ("Starting HTTP server at port %d." % port) + \
          Style.RESET_ALL
    httpd.serve_forever()


def wait_for_server_to_be_up(port, max_attempts, attempt_interval):
    attempts = 0
    server_is_up = False
    while not server_is_up:
        try:
            urllib2.urlopen('http://127.0.0.1:%d' % port)
            server_is_up = True
        except urllib2.URLError:
            attempts += 1
            if attempts >= max_attempts:
                raise
            time.sleep(attempt_interval)


def start(root_dir, port):
    thread = threading.Thread(target=run, kwargs=dict(
        root_dir=root_dir,
        port=port
    ))
    thread.daemon = True
    thread.start()
    wait_for_server_to_be_up(port, max_attempts=5, attempt_interval=0.25)
