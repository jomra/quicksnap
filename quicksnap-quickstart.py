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
  print(sys.stderr, "Neither Flameshot nor Scrot is installed. Please install one (Flameshot prefered) before running this script.")
  exit()

# Ensure we're not attempting to use scrot with wayland
# At this point, no flameshot = scrot is installed

if os.getenv("XDG_SESSION_TYPE") == "wayland" and not which("flameshot"):
  print(sys.stderr, "Scrot generally doesn't work in Wayland sessions. Please install Flameshot or switch to X11 before running this script.")
  exit()

# Initialize secretstorage and check if it is available
connection = secretstorage.dbus_init()
collection = secretstorage.get_default_collection(connection)

if not secretstorage.check_service_availability(connection):
  print(sys.stderr, "SecretStorage is not available. Aborting installation.")
  exit()

# Make app & screenshot directories if they don't exist

directory = os.path.expanduser("~/.quicksnap")
screenshotDirectory = os.path.expanduser("~/.quicksnap/screenshots")

try:
  os.mkdir(directory)
except FileExistsError as e:
  print(sys.stderr, "Directory already exists. Did you already run this script?")
  exit()

os.mkdir(screenshotDirectory)

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


# Get ready to store credentials

attributesToSearch = {'application': 'Quicksnap'}

try:
  collection.unlock()
except:
  print("Failed to unlock collection.")
  exit()

# Check if item already exists
items = collection.search_items(attributesToSearch)
try:
  item = next(items)
except StopIteration:
  # Item doesn't exist, everything is fine
  pass
else:
  # Item exists, offer to delete it (and any others that match)
  confirmDeleteCredentials = input("\nCredentials already exist and must be removed to install Quicksn.app. Delete them? [y/n] ")
  if confirmDeleteCredentials.lower() == "y":
    try:
      while item is not None:  # Exits when StopIteration is raised
        item.delete()
        item = next(items)
    except StopIteration:
      # Exit the loop; everything has been deleted
      print("Deleted credentials.")
  else:
    print("Aborting.")
    exit()

# Get credentials
email = input("\nEnter email: ")
password = input("Enter password: ")

# Store credentials
attributes = {'application': 'Quicksnap', 'email': email}
item = collection.create_item('Quicksnap', attributes, password.encode())
connection.close()

# Create .desktop file
iconPath = os.path.expanduser("~/.quicksnap/icon.png")
desktop = f"""[Desktop Entry]
Name=Quicksn.app
Comment=Upload screenshots to Quicksn.app
Exec=npm --prefix {directory} run start
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