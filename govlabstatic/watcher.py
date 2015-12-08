import time

from staticjinja.reloader import Reloader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class StaticjinjaReloaderEventHandler(FileSystemEventHandler):
    def __init__(self, reloader):
        FileSystemEventHandler.__init__(self)
        self.reloader = reloader

    def on_any_event(self, event):
        self.reloader.event_handler(event.event_type, event.src_path)

class Watcher(object):
    '''
    Encapsulates the watching of directories and files and taking
    actions when they change.
    '''

    def __init__(self):
        #: A :py:class:`watchdog.observers.api.BaseObserver` instance.
        #: Feel free to schedule the watching of new paths and
        #: reacting to changes in them as needed.
        self.observer = Observer()

    def add_site(self, site):
        reloader = Reloader(site)
        self.observer.schedule(StaticjinjaReloaderEventHandler(reloader),
                               reloader.searchpath,
                               recursive=True)

    def run(self):
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
