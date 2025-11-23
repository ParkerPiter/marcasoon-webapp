"""
gunicorn.conf.py

Gunicorn configuration file.
"""
import multiprocessing

# Socket Path
# The path to the Gunicorn socket file.
# This is used for communication between Gunicorn and the web server (e.g., Nginx).
# bind = 'unix:/var/run/gunicorn.sock'

# Worker Options
# The number of worker processes for handling requests.
# For Render's free/starter tiers, it's better to limit workers to avoid OOM (Out Of Memory) errors.
workers = 2
# The type of workers to use. 'gthread' is a standard choice that supports threads.
worker_class = 'gthread'
# The number of threads per worker.
threads = 4

# Logging Options
# The path to the log file for Gunicorn access logs.
# accesslog = '/var/log/gunicorn/access.log'
# The path to the log file for Gunicorn error logs.
# errorlog = '/var/log/gunicorn/error.log'
# The level of logging.
loglevel = 'info'

# Process Naming
# A name for the Gunicorn process. This is useful for process management.
proc_name = 'marcasoon-gunicorn'

# Django WSGI Application
# The path to the Django WSGI application.
# This should be in the format 'your_project_name.wsgi:application'.
# Replace 'marcasoon' with the name of your Django project directory
# (the one that contains settings.py).
wsgi_app = 'marcasoon.wsgi:application'

# The directory to chdir to at startup.
# This should be the root of your Django project.
# chdir = '/home/u967020933/marcasoon-webapp' # Change this to your project's path on the server

# User and Group
# The user and group to run the Gunicorn process as.
# It's a security best practice to run Gunicorn as a non-root user.
# user = 'your_user' # Change this to your user on the server
# group = 'your_group' # Change this to your group on the server
