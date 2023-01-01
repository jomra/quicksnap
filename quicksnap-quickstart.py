#!/usr/bin/env python3

# This utility fetches Quicksnap's latest release, generates a .desktop file, and creates the config file if necessary

import subprocess
import urllib.request
from base64 import encode
from shutil import which
import secretstorage
import os, sys

print("\nHi there!")
print("\nBefore using this script, ensure...")
print("\t* You have created a Quicksn.app account (https://quicksn.app)")
print("\t* nodejs, npm, and flameshot (or at least scrot) are installed on the system")
print("\nQuicksn.app is licensed under the Mozilla Public License 2.0. THERE IS NO WARRANTY!\n")

proceed = input("Do you want to proceed with installation? [y/n] ")
if proceed.lower() != "y":
  # No need for fancy input validation here. The user can always run the script again if they enter the wrong thing.
  print("Aborting.")
  exit()

# Ensure Linux
if not sys.platform.startswith('linux'):
  print(sys.stderr, "This script is only compatible with Linux.")
  exit()

# Ensure dependencies are installed
if not which("node"):
  print(sys.stderr, "NodeJS is not installed. Please install it before running this script.")
  exit()
if not which("npm"):
  print(sys.stderr, "NPM is not installed. Please install it before running this script.")
  exit()
if not which("flameshot") and not which("scrot"):
  print(sys.stderr, "Neither Flameshot nor Scrot is not installed. Please install one (Flameshot prefered) before running this script.")
  exit()

# TODO: check if secretstorage is available

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
iconPath = os.path.expanduser("~/.quicksnap/icon.png")
desktop = f"""[Desktop Entry]
Name=Quicksn.app
Comment=Upload screenshots to Quicksn.app
Exec=cd ~/.quicksnap && npm run start
Icon={iconPath}
Terminal=false
Type=Application
Categories=Utility"""

if not os.path.exists(os.path.expanduser("~/.local/share/applications")):
  os.mkdir(os.path.expanduser("~/.local/share/applications"))

with open(os.path.expanduser("~/.local/share/applications/quicksnap.desktop"), "w") as f:
  f.write(desktop)

print("\nDone! You can now run Quicksn.app from your applications menu.\n")

def programExists(program: str) -> bool:
  return which(program) is not None