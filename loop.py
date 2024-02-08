import os
import time
import pathlib
import subprocess

def get_username():
    if os.geteuid() == 0:
        return os.environ["SUDO_USER"]
    else:
        return os.path.expanduser("~")

def check_for_video():
    global current_video, video_files, video_index

    video_dir = pathlib.Path(get_username())

    if not video_files:
        video_files = [file for file in video_dir.glob("*") if file.suffix.lower() in ['.3g2', '.3gp', '.a52', '.aac', '.avi', '.dv', '.flv', '.mka', '.mkv', '.mov', '.mp4', '.mpeg', '.mpg', '.ogg', '.ogm', '.ogv', '.vob', '.wav', '.webm', '.wmv']]

    if video_files:
        current_video = video_files[video_index]
        video_index = (video_index + 1) % len(video_files)
        return True
    return False

def play_video():
    global current_video

    if current_video:
        player = subprocess.Popen(["cvlc", "--play-and-exit", "--quiet", str(current_video)])
        while player.poll() is None:
            if not current_video.exists():
                player.terminate()
                break
            time.sleep(1)

current_video = None
video_files = []
video_index = 0

while True:
    if check_for_video():
        play_video()

    time.sleep(1)
