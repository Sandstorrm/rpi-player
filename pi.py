import os
import pathlib

# Define function to get username
def get_username():
    # Check if script is running with sudo
    if os.geteuid() == 0:
        # Use SUDO_USER environment variable if running with sudo
        username = os.environ["SUDO_USER"]
    else:
        # Get username without prompting if not running with sudo
        username = os.path.expanduser("~")

    # Check if username is empty (optional)
    if not username:
        print("Username could not be determined. Please enter your username:")
        return input()
    else:
        return username

# Get username
username = get_username()

# Update and upgrade system
os.system("sudo apt update && sudo apt upgrade -y")

# Download additional script
# os.system("curl -L -o loop.py raw.githubusercontent.com/Sandstorrm/python-scripts/main/loop.py")

# Install VLC
os.system("sudo apt install vlc python-vlc python3-watchdog -y")

# Install Samba
os.system("sudo apt install samba -y")

# Add user to Samba
os.system(f"sudo smbpasswd -a {username}")

# Edit Samba config file
samba_config_path = pathlib.Path("/etc/samba/smb.conf")
with samba_config_path.open("r+") as f:
    content = f.read()
    new_content = content.replace("username", str(username))
    f.seek(0)
    f.write(new_content)
    f.truncate()

# Add user specific share configuration
new_share_config = f"\n[{username}]\n" + \
                   f"path = {pathlib.Path(f'/home/{username}/Desktop')}\n" + \
                   f"valid users = {username}\n" + \
                   f"write list = {username}\n" + \
                   f"browsable = yes\n" + \
                   f"comment = \"smbshare\"\n"

# Append new share configuration to the Samba config file
with samba_config_path.open("a") as f:
    f.write(new_share_config)

# Restart Samba as smbd
os.system("sudo systemctl restart smbd")

# Get IP address
ip_address = os.popen("hostname -I").read().strip()

# Print success message
print(f"System updated, upgraded, VLC and Samba installed successfully for user '{username}'. Samba service started!")
print(f"Your IP address is: {ip_address}. Use this along with your SMB password to transfer files.")
print("When you have finished uploading videos you may run 'python loop.py' to play the videos.")
print("Scripts created by Sandstorm. Enjoy!")
