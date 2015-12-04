import sys
import os
import subprocess
import threading
import atexit
import colorama

from colorama import Style, Fore

from . import webserver

def start_web_server(root_dir, port=7000):
    thread = threading.Thread(target=webserver.run_server, kwargs=dict(
        root_dir=root_dir,
        port=port
    ))
    thread.daemon = True
    thread.start()


def start_sass(src_path, dest_path):
    print Style.BRIGHT + "Starting SASS." + Style.RESET_ALL

    try:
        process = subprocess.Popen(' '.join([
            'sass',
            '--watch',
            '%s:%s' % (src_path, dest_path)
        ]), shell=True)
        atexit.register(process.kill)
    except OSError, e:
        print Style.BRIGHT + Fore.RED
        print "SASS failure: %s" % e
        print "SASS files will not be built."
        print Style.RESET_ALL


def init():
    if sys.platform == 'win32':
        # Workaround for https://github.com/tartley/colorama/issues/48.
        if 'TERM' in os.environ:
            del os.environ['TERM']
    colorama.init()
