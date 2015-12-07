import sys
import os
import argparse
import inspect

import argh
import colorama
import staticjinja

from . import sass, webserver, watcher

def init_colors():
    if sys.platform == 'win32':
        # Workaround for https://github.com/tartley/colorama/issues/48.
        if 'TERM' in os.environ:
            del os.environ['TERM']
    colorama.init()

class Manager(object):
    '''
    Command-line interface manager for static site generation and
    associated tools.
    '''

    def __init__(self, site_name, sass_src_path, sass_dest_path,
                 site, usage=None, help=None):
        self.site = site
        self.site_name = site_name
        self.sass_src_path = sass_src_path
        self.sass_dest_path = sass_dest_path
        self.parser = argparse.ArgumentParser(
            description='Static site generator for %s' % site_name
        )
        self.watcher = watcher.Watcher()
        self.watcher.add_site(site)
        BuiltinCommands.add_to(self)

    def run(self):
        init_colors()
        dirs = [self.site.outpath, os.path.dirname(self.sass_dest_path)]
        for dirname in dirs:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        argh.dispatch(self.parser)

def is_instance_method(obj):
    '''
    Returns whether the given object is an instance method (and specifically
    *not* a class method).
    '''

    return inspect.ismethod(obj) and not inspect.isclass(obj.__self__)

class ManagerCommands(object):
    '''
    This is just a simple class that makes it easy for commands to
    access their associated Manager instance.

    Commands are defined as public instance methods of a ManagerCommands
    subclass and can access their Manager via self.manager.
    '''

    def __init__(self, manager):
        self.manager = manager

    @classmethod
    def add_to(cls, manager):
        '''
        Add all public instance methods of this class to the given Manager
        as commands.
        '''

        commands = cls(manager)
        argh.add_commands(manager.parser, [
            getattr(commands, name) for name in dir(commands)
            if not name.startswith('_')
            and is_instance_method(getattr(commands, name))
        ])

class BuiltinCommands(ManagerCommands):
    @argh.arg('--port', help='port to serve on')
    def runserver(self, port=7000):
        '''
        Run development server.
        '''

        manager = self.manager
        sass.start_watch(src_path=manager.sass_src_path,
                         dest_path=manager.sass_dest_path)
        webserver.start(root_dir=manager.site.outpath, port=port)
        manager.site.render()
        manager.watcher.run()

    def build(self):
        '''
        Build the static site.
        '''

        print "Building SASS..."
        sass.compile(src_path=self.manager.sass_src_path,
                     dest_path=self.manager.sass_dest_path)
        print "Generating site..."
        self.manager.site.render()
        print "Done."
