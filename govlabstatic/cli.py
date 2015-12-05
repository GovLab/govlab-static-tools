import sys
import os
import argparse
import inspect

import argh
import colorama
import staticjinja

from . import sass, webserver

def init_colors():
    if sys.platform == 'win32':
        # Workaround for https://github.com/tartley/colorama/issues/48.
        if 'TERM' in os.environ:
            del os.environ['TERM']
    colorama.init()

class Manager(object):
    def __init__(self, site_name, sass_src_path, sass_dest_path,
                 site, usage=None, help=None):
        self.site = site
        self.site_name = site_name
        self.sass_src_path = sass_src_path
        self.sass_dest_path = sass_dest_path
        self.parser = argparse.ArgumentParser(
            description='Static site generator for %s' % site_name
        )
        BuiltinCommands.add_to(self)

    def run(self):
        init_colors()
        if not os.path.exists(self.site['outpath']):
            os.makedirs(self.site['outpath'])
        argh.dispatch(self.parser)

def is_instance_method(obj):
    return inspect.ismethod(obj) and not inspect.isclass(obj.__self__)

class ManagerCommands(object):
    def __init__(self, manager):
        self.manager = manager

    @classmethod
    def add_to(cls, manager):
        commands = cls(manager)
        argh.add_commands(manager.parser, [
            getattr(commands, name) for name in dir(commands)
            if not name.startswith('_')
            and is_instance_method(getattr(commands, name))
        ])

class BuiltinCommands(ManagerCommands):
    def runserver(self):
        '''
        Run development server.
        '''

        manager = self.manager
        sass.start_watch(src_path=manager.sass_src_path,
                         dest_path=manager.sass_dest_path)
        webserver.start(root_dir=manager.site['outpath'])
        staticjinja.make_site(**manager.site).render(use_reloader=True)

def run(sass_src_path, sass_dest_path, site, name):
    manager = Manager(
        site_name=name,
        sass_src_path=sass_src_path,
        sass_dest_path=sass_dest_path,
        site=site
    )
    manager.parser.set_default_command('runserver')
    manager.run()
