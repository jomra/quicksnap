#!/usr/bin/env python3

# This utility deletes Quicksnap's .desktop file, deletes the .quicksnap directory, and deletes the credentials from the keyring

from shutil import rmtree
import secretstorage
import os

proceed = input("\nReally delete Quicksnap [y/n]? ")

if proceed.lower() != "y":
  # No need for fancy input validation here. The user can always run the script again if they enter the wrong thing.
  print("Aborting.")
  exit()

print() # For formatting

# Delete .desktop file
try:
  os.remove(os.path.expanduser("~/.local/share/applications/quicksnap.desktop"))
  print("Desktop file deleted.")
except FileNotFoundError as e:
  print("Desktop file not found.")

# Delete .quicksnap directory
try:
  rmtree(os.path.expanduser("~/.quicksnap"))
  print("Quicksnap directory deleted.")
except FileNotFoundError as e:
  print("Quicksnap directory not found.")

# Delete credentials from keyring

connection = secretstorage.dbus_init()
collection = secretstorage.get_default_collection(connection)
attributes = {'application': 'Quicksnap'}

try:
  collection.unlock()
except:
  print("Failed to unlock collection.")
  exit()

# Find all matching items
noItemsHaveBeenDeleted = True
items = collection.search_items(attributes)
try:
  item = next(items)
  # Delete all matching items
  while item is not None: # Exits when StopIteration is raised
    item.delete()
    noItemsHaveBeenDeleted = False
    item = next(items)

except StopIteration:
  # Everything has been deleted
  if noItemsHaveBeenDeleted:
    print("Quicksn.app credentials not found.")
  else:
    print("Credentials deleted from keyring.")

connection.close()

print("\nQuicksn.app has been deleted. You can now delete this script.\n")
