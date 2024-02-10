# Raspberry Pi Video Player

This code is intended to be run on a Raspberry Pi Zero W with a headless (light) installation of Raspberry Pi OS. It serves as a simple and inexpensive alternative to a media player. When executed, it will search the main directory for video files, and if one is found, it will play it. To stop playback, simply delete the file from the directory. Access to the file system is provided using Samba share. You may need to search online for instructions on how to map a local network drive to your computer.

## Usage

1. **Download the Code:**

   Run the following command to download the code to your Raspberry Pi (It is case sensitive):
   ```bash
   curl -L https://raw.githubusercontent.com/Sandstorrm/rpi-player/main/pi.py | python
2. **Run the Program:**

   Execute the following command to run the program:
   ```bash
   python loop.py
