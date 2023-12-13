import os
import time
import vlc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
  def __init__(self):
    self.vlc_instance = vlc.Instance()
    self.player = self.vlc_instance.media_player_new()

  def on_modified(self, event):
    if event.is_directory:
      return None
    elif event.src_path.endswith(('.mp4', '.mov', '.avi')):
      if self.player.is_playing():
        self.player.stop()
      media = self.vlc_instance.media_new(event.src_path)
      self.player.set_media(media)
      self.player.set_fullscreen(True)
      self.player.play()

if __name__ == "__main__":
  while True:
    try:
      event_handler = Handler()
      observer = Observer()
      observer.schedule(event_handler, path=os.path.expanduser('/home/sand/Desktop'), recursive=False)
      observer.start()

      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      observer.stop()
      observer.join()
      break
    except Exception as e:
      print(f"An error occurred: {e}. Retrying...")
