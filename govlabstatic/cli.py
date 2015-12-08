import sys
import os
import argparse
import inspect

import argh
import colorama
import staticjinja

from . import sass, webserver, watcher, testing

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

    :param site_name:
        The name of the site, e.g. ``'GovLab Academy Website'`` or
        ``'www.mysite.com'``.

    :param sass_src_path:
        The path to SASS source, e.g. ``'sass/styles.scss'``.

    :param sass_dest_path:
        The path to compile SASS source to, e.g.
        ``'static/styles/styles.css'``.

    :param site:
        A :py:class:`staticjinja.Site` object representing the site
        to build.
    '''

    def __init__(self, site_name, sass_src_path, sass_dest_path,
                 site):
        self.site = site
        self.site_name = site_name
        self.sass_src_path = sass_src_path
        self.sass_dest_path = sass_dest_path

        #: An :py:class:`argparse.ArgumentParser` responsible for
        #: parsing command-line arguments. Feel free to add to this
        #: via :py:func:`argh.assembling.add_commands` to add new commands to your CLI.
        self.parser = argparse.ArgumentParser(
            description='Static site generator for %s' % site_name
        )

        #: A :py:class:`govlabstatic.watcher.Watcher` instance used
        #: to watch directories for changes.
        self.watcher = watcher.Watcher()
        self.watcher.add_site(site)
        BuiltinCommands.add_to(self)

    def run(self):
        '''
        Runs the command-line interpreter.
        '''

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
    '''
    These are built-in commands that come with any :py:class:`Manager`
    instance.
    '''

    @argh.arg('--port', help='port to serve on')
    def runserver(self, port=7000):
        '''
        Run development server.

        This builds the static site, and rebuilds necessary files
        whenever changes are detected.
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

    def test(self):
        '''
        Run test suite.

        Currently, this builds the site and checks links.
        '''

        print "Running smoke test."
        self.build()
        print "Checking links."
        if not testing.linkcheck_site(root_dir=self.manager.site.outpath):
            print "Errors found while checking links, aborting."
            sys.exit(1)
        print "Tests pass!"
