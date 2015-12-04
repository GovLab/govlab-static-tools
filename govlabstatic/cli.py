import sys
import os
import argparse

import colorama

import staticjinja

from . import sass, webserver
from .script.manager import Manager, App
from .script.commands import Command

def init_colors():
    if sys.platform == 'win32':
        # Workaround for https://github.com/tartley/colorama/issues/48.
        if 'TERM' in os.environ:
            del os.environ['TERM']
    colorama.init()

class GovLabApp(App):
    def __init__(self, **kwargs):
        App.__init__(self)
        self.__dict__.update(kwargs)

class GovLabManager(Manager):
    def __init__(self, site_name, usage=None, help=None, **kwargs):
        app = GovLabApp(site_name=site_name, **kwargs)
        Manager.__init__(
            self,
            app,
            usage=usage,
            help=help,
            description='Static site generator for %s' % site_name
        )
        self.add_command('runserver', WatchBuildServe())

    def run(self, commands=None, default_command=None):
        init_colors()
        Manager.run(self, commands, default_command)

class WatchBuildServe(Command):
    def run(self):
        if not os.path.exists(self.app.site['outpath']):
            os.makedirs(self.app.site['outpath'])
        sass.start_watch(src_path=self.app.sass_src_path,
                         dest_path=self.app.sass_dest_path)
        webserver.start(root_dir=self.app.site['outpath'])
        staticjinja.make_site(**self.app.site).render(use_reloader=True)

def run(sass_src_path, sass_dest_path, site, name):
    manager = GovLabManager(
        site_name=name,
        sass_src_path=sass_src_path,
        sass_dest_path=sass_dest_path,
        site=site
    )
    manager.run(default_command='runserver')
