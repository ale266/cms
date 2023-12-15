# /bin/bash

##### PRD

#migrate produccion 
python manage.py migrate --settings=cms.settings.production


# para poblar la BD 
echo ">>> Poblando la base de datos de produccion"
python manage.py loaddata db.json --settings=cms.settings.production

echo ">>> Iniciando el servidor con la base de datos de produccion"
python manage.py runserver --settings=cms.settings.production