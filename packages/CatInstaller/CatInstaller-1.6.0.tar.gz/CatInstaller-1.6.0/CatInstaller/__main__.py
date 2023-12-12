from rich.progress import Progress
import time
import requests
import os



# This program is require "rich" and "requests"

print("Cat Installer for Python: Catch file, and Installing.")
print("V1.6.0")
print("")
print("What do you want to install?")
installername = input("> ")

print("Downloading installer.py for " + installername + " from GitHub...")

url='https://raw.githubusercontent.com' + installername + "main/installer.py"
filename='./installer.py'

urlData = requests.get(url).content

with open(filename ,mode='wb') as f:
  f.write(urlData)

print("Downloaded.")

print("Installing requiments...")

import installer

requiments = installer.requiments

for requiment in requiments:
    os.system("pip","install",requiment)

progressnumbers = installer.numbersofprogress

totalkun = 0

with Progress() as progress:
    task_id = progress.add_task("Installing...", total= int(100 / progressnumbers))
    while not progress.finished:
        totalkun = totalkun + 1
        progress.update(task_id, advance=1)
        installer.install(totalkun)

print("Installed: " + installername)

os.remove('./installer.py')

print("installer.py is removed.")

print("Done.")
