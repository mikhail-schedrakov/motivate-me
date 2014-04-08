import os
import sys
	
sys.path.append('/home/mikhail/sites/motivate-me.local/')
sys.path.append('/home/mikhail/sites/motivate-me.local/project/')
sys.path.append('/usr/local/lib/python3.3/dist-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
