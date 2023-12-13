import os
import subprocess
import time

def play_videos(directory):
    while True:
        files = os.listdir(directory)
        videos = [file for file in files if file.endswith(('.mp4', '.avi', '.mkv'))]  # Add more video formats if needed
        if videos:
            for video in videos:
                video_path = os.path.join(directory, video)
                if os.path.exists(video_path):
                    try:
                        subprocess.call(['omxplayer', video_path])
                    except Exception as e:
                        print(f"Unable to open {video}. Error: {str(e)}")
                        continue
        else:
            display_image = os.path.join(directory, 'upload.png')
            if not os.path.exists(display_image):
                subprocess.call(['curl', '-L', '-o', '~/Desktop/upload.png', 'bit.ly/sand-pi-png'])
            subprocess.call(['feh', '-F', display_image])
        time.sleep(1)

play_videos('/home/sand/Desktop')
