#!/bin/bash

# para poblar la BD 
echo ">>> CREAR CATEGORIAS ----"
python manage.py poblar_bd --settings=cms.settings.development
