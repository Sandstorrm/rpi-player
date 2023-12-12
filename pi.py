# Import modules
import os

# Define function to get username
def get_username():
    username = input("Please enter your username: ")

    # Check if username is empty
    if not username:
        print("Username cannot be empty. Please try again.")
        return get_username()
    else:
        return username

# Get username
username = get_username()

# Update and upgrade system
os.system("sudo apt update && sudo apt upgrade -y")

# Install VLC
os.system("sudo apt install vlc -y")

# Install Samba
os.system("sudo apt install samba -y")

# Add user to Samba
os.system(f"sudo smbpasswd -a {username}")

# Edit Samba config file
samba_config_path = "/etc/samba/smb.conf"
with open(samba_config_path, "r+") as f:
    content = f.read()
    new_content = content.replace("username", username)
    f.seek(0)
    f.write(new_content)
    f.truncate()

# Add user specific share configuration
new_share_config = f"\n[{username}]\n" + \
f"path = /home/{username}/Desktop\n" + \
f"valid users = {username}\n" + \
f"write list = {username}\n" + \
f"browsable = yes\n" + \
f"comment = \"smbshare\"\n"

# Append new share configuration to the Samba config file
with open(samba_config_path, "a") as f:
    f.write(new_share_config)

# Restart Samba as smbd
os.system("sudo systemctl restart smbd")

# Print success message
print(f"System updated, upgraded, VLC and Samba installed successfully for user '{username}'. Samba service restarted!")
