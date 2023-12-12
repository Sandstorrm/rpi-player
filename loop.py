import os
import vlc
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path to desktop directory
desktop_path = "/home/pi/Desktop/"

# No-video image URL and filename
no_video_image_url = "bit.ly/sand-pi-png"
no_video_image_filename = "upload.png"

# VLC instance
vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()

# Flag to indicate no video image is playing
no_video_playing = True


class FileSystemHandler(FileSystemEventHandler):
    def on_created(self, event):
        global no_video_playing
        if event.is_file and event.src_path.endswith(".mp4") or event.src_path.endswith(".avi"):
            # New video file detected, stop image and start playing
            if no_video_playing:
                player.stop()
                no_video_playing = False
                play_videos(desktop_path)


def play_videos(directory):
    # Get list of video files
    videos = [f for f in os.listdir(directory) if f.endswith(".mp4") or f.endswith(".avi")]

    # Loop through videos and play them
    for video in videos:
        player.set_mrl(os.path.join(desktop_path, video))
        player.play()
        player.set_fullscreen(True)

        # Wait until video finishes playing
        while player.get_state() != vlc.State.Ended:
            vlc.libvlc_video_output_set_window(vlc_instance, player, 0)
            player.play()


def download_no_video_image():
    """Downloads the no-video image if it doesn't exist."""
    if not os.path.exists(os.path.join(desktop_path, no_video_image_filename)):
        os.system(f"curl -L -o {os.path.join(desktop_path, no_video_image_filename)} {no_video_image_url}")


# Download the no-video image if needed
download_no_video_image()

# Start watching for new files on desktop
event_handler = FileSystemHandler()
observer = Observer()
observer.schedule(event_handler, desktop_path, recursive=False)
observer.start()

# Check for existing videos and play image if needed
if not os.listdir(desktop_path):
    # No videos found, play no-video image
    player.set_mrl(os.path.join(desktop_path, no_video_image_filename))
    player.play()
    player.set_fullscreen(True)
    no_video_playing = True

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    player.stop()
    observer.join()
