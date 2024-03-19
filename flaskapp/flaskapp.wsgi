# flaskapp.wsgi
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/ibrahim/Documents/MyFlashPrac/venv/lib/python3.11/site-packages')

# Add the application's directory to the PYTHONPATH
sys.path.insert(0, '/home/ibrahim/Documents/MyFlashPrac/flaskapp')

from app import app as application
