CatInstaller
##

CatInstaller is an installer that allows you to easily install something on your OS.

All you need is Python and the necessary modules.

How to support CatInstaller
==

To support CatInstaller, simply write a program in a Python file.

Upload Installer.py to GitHub and it will be ready for installation.

Installer.py must be written in the following format.

::

  requiments = ["time"] # Enter the required Python modules here.

  numbersofprogress = 10 # Enter the steps

  import time # import required python modules

  def install(progress): # "progress" is number of steps
      print("Output ", progress) # Enter the install process here.

  # Enter the other functions...
