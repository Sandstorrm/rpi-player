import os
import time
import vlc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
  def __init__(self):
    self.vlc_instance = vlc.Instance()
    self.player = self.vlc_instance.media_player_new()
    self.current_video_index = 0

  def on_modified(self, event):
    if event.is_directory:
      return None
    elif event.src_path.endswith(('.mp4', '.mov', '.avi')):
      # Stop the player if already playing
      if self.player.is_playing():
        self.player.stop()

      # Get the list of video files in the monitored directory
      video_files = sorted(os.listdir(os.path.expanduser('/home/sand/Desktop')))

      # Handle looping
      if self.current_video_index < len(video_files):
        # Play the current video
        media = self.vlc_instance.media_new(os.path.join(os.path.expanduser('/home/sand/Desktop'), video_files[self.current_video_index]))
        self.player.set_media(media)
        self.player.set_fullscreen(True)
        self.player.play()

        # Update the current video index
        self.current_video_index += 1
      else:
        # Reached the end of the list, reset the index and restart looping
        self.current_video_index = 0
        self.on_modified(event)  # Trigger the event again to play the first video

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
