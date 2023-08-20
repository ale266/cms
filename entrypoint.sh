#!/bin/sh

echo 'Running collecstatic...'
python manage.py collectstatic --no-input --settings=cms.settings.production

echo 'Applying migrations...'
python manage.py wait_for_db --settings=cms.settings.production
python manage.py migrate --settings=cms.settings.production

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=cms.settings.production cms.wsgi:application --bind 0.0.0.0:8000