import os
import time
import vlc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def __init__(self):
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.current_file = None

    def on_modified(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith(('.mp4', '.mov', '.avi')):
            self.current_file = event.src_path
            if self.player.is_playing():
                self.player.stop()

            # Wait for the video to finish uploading
            while not os.path.isfile(self.current_file):
                time.sleep(1)

            # Play the video
            media = self.vlc_instance.media_new(self.current_file)
            self.player.set_media(media)
            self.player.set_fullscreen(True)
            self.player.play()

    def on_ended(self, event):
        if event.media.get_path() == self.current_file:
            # Loop the video
            self.player.set_position(0)
            self.player.play()

if __name__ == "__main__":
    event_handler = Handler()
    observer = Observer()

    # Add on_ended event listener to loop the video
    observer.schedule(event_handler, event_handler.on_ended, path=os.path.expanduser('/home/sand/Desktop'), recursive=False)

    observer.schedule(event_handler, path=os.path.expanduser('/home/sand/Desktop'), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
