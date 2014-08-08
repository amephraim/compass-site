# pinax.wsgi is configured to live in projects/mysite/deploy.

import os
import sys

# redirect sys.stdout to sys.stderr for bad libraries like geopy that uses
# print statements for optional import exceptions.
sys.stdout = sys.stderr

from os.path import abspath, dirname, join
from site import addsitedir
#sys.path.append("/home/ruchtan/Documents/Networks/finalone/compass-site")
#sys.path.insert(0, abspath(join(dirname(__file__), "../../")))
#sys.path.insert(0,"/home/ruchtan/Documents/Networks/finalone/compass-site/Pinax-0.7.3-bundle/pinax_env/bin")
sys.path.insert(0, "/home/ruchtan/Documents/Networks/finalone/compass-site/Pinax-0.7.3-bundle/pinax_env/lib/python2.7/site-packages")
import django 
print (django.__path__)
from django.conf import settings
sys.path.insert(0, "/home/ruchtan/Documents/Networks/finalone/compass-site/Pinax-0.7.3-bundle")
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
sys.path.insert(0, join(settings.PINAX_ROOT, "apps"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
