import os
import cv2
from time import sleep

# Define the directory to scan
video_dir = "/home/sand/Desktop/"
upload_image = "/home/sand/Desktop/upload.png"

# Download the upload image if it doesn't exist
if not os.path.exists(upload_image):
    os.system(f"curl -L -o {upload_image} bit.ly/sand-pi-png")

# Define functions to play videos and display images
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Unable to open video: {video_path}")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def display_image(image_path):
    img = cv2.imread(image_path)
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Start scanning and playing videos in a loop
while True:
    video_count = 0
    for filename in os.listdir(video_dir):
        filepath = os.path.join(video_dir, filename)
        if os.path.isfile(filepath) and filename.endswith(".mp4"):
            video_count += 1
            play_video(filepath)

    # If no videos were found, display the upload image
    if video_count == 0:
        display_image(upload_image)

    # Sleep for a while before scanning again
    sleep(5)
