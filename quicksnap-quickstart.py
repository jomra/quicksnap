#!/usr/bin/env python3

# This utility fetches Quicksnap's latest release, generates a .desktop file, and creates the config file if necessary

import subprocess
import urllib.request
from base64 import encode
import secretstorage
import configparser
import os, sys

print("\nHi there!")
print("Before using this script, make sure you've created a Quicksn.app account for this user. You can do that at https://quicksn.app.")
print("⚠️ Please ensure scrot is installed on the system before running this script.")
print("Quicksn.app is licensed under the Mozilla Public License 2.0. THERE IS NO WARRANTY!\n")

# Make app directory if it doesn't exist

directory = os.path.expanduser("~/.quicksnap")
try:
  os.mkdir(directory)
except FileExistsError as e:
  print(sys.stderr, "Directory already exists. Did you already run this script?")
  exit()
# Make sure .desktop file doesn't exist
if os.path.exists("~/.local/share/applications/quicksnap.desktop"):
  print(sys.stderr, "Desktop file already exists. Did you already run this script?")
  exit()

# Get the latest release from GitHub
# Not ideal, but works for now. FIXME
urls = [
  "https://raw.githubusercontent.com/jomra/quicksnap/main/client/quicksnap-client.js",
  "https://raw.githubusercontent.com/jomra/quicksnap/main/client/package.json",
  "https://raw.githubusercontent.com/jomra/quicksnap/main/client/qs-snap.py",
  "https://raw.githubusercontent.com/jomra/quicksnap/main/client/icon.png"
]
# Download the files
for url in urls:
  filename = url.split("/")[-1]
  urllib.request.urlretrieve(url, os.path.expanduser("~/.quicksnap/" + filename))

# Install dependencies for quicksnap-client.js
deps = subprocess.run(
    ["npm", "install"],
    shell=False, capture_output=False, cwd=os.path.expanduser("~/.quicksnap")
)

# Fail gracefully-ish
if deps.stderr:
  print("There was a problem. Is NPM installed? Details: " + deps.stderr)
  exit()


# Store credentials
email = input("Enter email: ")
password = input("Enter password: ")

# TODO: make sure an item with these attributes doesn't already exist
connection = secretstorage.dbus_init()
collection = secretstorage.get_default_collection(connection)
attributes = {'application': 'Quicksnap', 'email': email}

try:
  collection.unlock()
except:
  print("Failed to unlock collection. Is the keyring unlocked?")
  exit()

item = collection.create_item('Quicksnap', attributes, password.encode())

connection.close()

# Create .desktop file
desktop = """[Desktop Entry]
Name=Quicksn.app
Comment=Upload screenshots to Quicksn.app
Exec=node run ~/.quicksnap/quicksnap-client.js
Icon=~/.quicksnap/icon.png
Terminal=false
Type=Application
Categories=Utility"""

if not os.path.exists(os.path.expanduser("~/.local/share/applications")):
  os.mkdir(os.path.expanduser("~/.local/share/applications"))

with open(os.path.expanduser("~/.local/share/applications/quicksnap.desktop"), "w") as f:
  f.write(desktop)

print("\nDone! You can now run Quicksn.app from your applications menu.\n")
