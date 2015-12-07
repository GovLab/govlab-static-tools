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
    def __init__(self):
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
