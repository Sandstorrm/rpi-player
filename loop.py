import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def __init__(self):
        self.process = None

    def play_video(self, path):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(['bv', path])

    def on_modified(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith(('.mp4', '.mov', '.avi')):
            self.play_video(event.src_path)

if __name__ == "__main__":
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.expanduser('~/Desktop'), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
