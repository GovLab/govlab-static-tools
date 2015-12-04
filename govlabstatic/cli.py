import sys
import os
import argparse

import colorama

import staticjinja

from . import sass, webserver

def init_colors():
    if sys.platform == 'win32':
        # Workaround for https://github.com/tartley/colorama/issues/48.
        if 'TERM' in os.environ:
            del os.environ['TERM']
    colorama.init()

def run(sass_src_path, sass_dest_path, site, name):
    init_colors()

    parser = argparse.ArgumentParser(
        description='Static site generator for %s' % name,
    )

    args = parser.parse_args()

    sass.start_watch(src_path=sass_src_path, dest_path=sass_dest_path)
    webserver.start(root_dir=site['outpath'])
    staticjinja.make_site(**site).render(use_reloader=True)
