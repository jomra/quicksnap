# Get the credentials & take a screenshot
# This script is meant to be run from qs-upload.js
# Python includes secretstorage support, and Firebase supports JS, so it's easier to separate the two scripts
# Actually taking the screenshot with scrot/flameshot is done with here for no particular reason
# Copyright 2022 John Sarbak

import os, sys, secretstorage, time, subprocess
from shutil import which

# Ensure .quicksnap directory exists. Bonus: this is a good heuristic for whether the user has run quicksnap-quickstart.py
if not os.path.exists(os.path.expanduser("~/.quicksnap")):
  print("You need to run quicksnap-quickstart.py before running this script.")
  exit()


# Set file name and path
FILE_NAME = "screenshot-" + str(time.time()) + ".png"
FILE_PATH = os.path.expanduser("~/.quicksnap/screenshots/" + FILE_NAME)

# Get credentials
connection = secretstorage.dbus_init()
collection = secretstorage.get_default_collection(connection)

try:
  collection.unlock()
except:
  print("Failed to unlock collection.")
  exit()

attributes = {'application': 'Quicksnap'}
items = collection.search_items(attributes)

try:
    item = next(items)
except StopIteration:
    print("No credentials found. Did you run quicksnap-quickstart.py?")
    exit()

email: str = item.get_attributes()["email"]
password: str = item.get_secret().decode()

connection.close()

# Take screenshot

# Try to use flameshot if it's installed
if which("flameshot"):
  screenshot = subprocess.run(
    ["flameshot", "full", "-p", FILE_PATH],
    shell=False, capture_output=True
  )
else:
  # Scrot should be installed on most systems
  # Quickstart script makes sure at least one of the two is installed
  # Not running that script is unsupported behavior (todo?)
  screenshot = subprocess.run(
      ["scrot", "-p", "--file", FILE_PATH],
      shell=False, capture_output=True
  )

# Fail gracefully-ish
# if screenshot.stderr:
#   print("There was a problem. Details: " + screenshot.stderr.decode())
#   exit()
# TODO: doesn't work with flameshot. Bug upstream?

# Output credentials, plus file name and path
print(email + "\n" + password + "\n" + FILE_NAME + "\n" + FILE_PATH)

sys.stdout.flush()