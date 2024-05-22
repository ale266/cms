# Cms
Repo de ingenieria de software 2


# LISTA DE COMANDOS  

# para ejecutar ambiente de desarrollo

python manage.py makemigrations --settings=cms.settings.development

python manage.py migrate --settings=cms.settings.development 

python manage.py runserver --settings=cms.settings.development 

# para ejecutar ambiente de produccion
python manage.py collectstatic --settings=cms.settings.production </// para coleccionar archivos estaticos en produccion, si hay cambios

python manage.py migrate --settings=cms.settings.production </// para migrar todas las tablas en produccion, si hay cambios en las tablas

python manage.py runserver --settings=cms.settings.production  <//// para ejecutar ambiente de produccion sin web service

uvicorn cms.asgi:application --host 127.0.0.1 --port 8000 --reload <//// ejecutar uvicorn asgi (servidor web asincrono)


python -m django_pydoc.py -b <////  DOCUMENTATION

ingresar a la carpeta donde estan los test y ejecutar en consola: pytest <////  Test
