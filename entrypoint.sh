echo 'Running collecstatic...'
python manage.py collectstatic --no-input --settings=cms.settings.production


echo 'Applying migrations...'
python manage.py migrate --settings=cms.settings.production


echo 'Running server...'
uvicorn cms.asgi:application --host 127.0.0.1 --port 8000 --reload 
