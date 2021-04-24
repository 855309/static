#!/usr/bin/python3

from zipfile import ZipFile
import requests
from tqdm import tqdm
import os
import sys

if os.getenv("SUDO_USER") == None:
    sys.exit("light installation script must be run as root.")

def log(x):
    print(":: " + x)

if os.path.exists("/tmp/light.zip"):
    os.system("sudo rm -rf /tmp/light.zip")

log("Fetching light...")

url = "https://raw.githubusercontent.com/fikret0/static/main/light/light.zip"

response = requests.get(url, stream=True)

total_size_in_bytes = int(response.headers.get('content-length', 0))

block_size = 1024

progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

with open('/tmp/light.zip', 'wb') as file:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)

progress_bar.close()

if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
    print("Error.")
    exit()

if os.path.exists("/usr/share/light"):
    log("Removing existing installation...")
    os.system("sudo rm -rf /usr/share/light")

if os.path.islink("/usr/bin/light"):
    log("Removing existing symlinks...")
    os.system("sudo rm -rf /usr/bin/light")

log("Extracting...")

with ZipFile('/tmp/light.zip', 'a') as zipObj:
    zipObj.extractall("/usr/share/light")

log("Creating symlinks...")

os.system("sudo chmod +x /usr/share/light/light.py")

os.system("sudo ln -s /usr/share/light/light.py /usr/bin/light")

log("Installation successful!")
