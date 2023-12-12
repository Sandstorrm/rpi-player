import os
import time
import cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def __init__(self):
        self.video = None

    def play_video(self, path):
        self.video = cv2.VideoCapture(path)
        cv2.namedWindow('Video', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        self.video.release()
        cv2.destroyAllWindows()

    def on_modified(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith(('.mp4', '.mov', '.avi')):
            if self.video and self.video.isOpened():
                self.video.release()
                cv2.destroyAllWindows()
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
