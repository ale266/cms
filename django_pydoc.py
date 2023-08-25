import django
import pydoc
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'cms.settings.development'
django.setup()
pydoc.cli()