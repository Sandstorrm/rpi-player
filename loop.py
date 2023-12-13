import os
import time
import vlc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def __init__(self):
        self.vlc_instance = vlc.Instance()
        self.list_player = self.vlc_instance.media_list_player_new()
        self.player = self.vlc_instance.media_player_new()

    def on_modified(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith(('.mp4', '.mov', '.avi')):
            if self.list_player.is_playing():
                self.list_player.stop()
            time.sleep(5)  # increase the delay
            try:
                media = self.vlc_instance.media_new(event.src_path)
                media_list = self.vlc_instance.media_list_new([event.src_path])  # create a new MediaList
                self.list_player.set_media_list(media_list)  # set the player's media list
                self.list_player.set_playback_mode(vlc.PlaybackMode.loop)  # set playback mode to loop
                self.player.set_fullscreen(True)  # set fullscreen
                self.list_player.play()
            except Exception as e:
                print(f"Failed to play {event.src_path} due to {str(e)}")

if __name__ == "__main__":
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.expanduser('/home/sand/Desktop'), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
