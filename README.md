# Cms
Repo de ingenieria de software 2


<<<<<<<<< Temporary merge branch 1
<////  LISTA DE COMANDOS   ////>

<//// para ejecutar ambiente de desarrollo
=========
# LISTA DE COMANDOS  

# para ejecutar ambiente de desarrollo

python manage.py makemigrations --settings=cms.settings.development

python manage.py migrate --settings=cms.settings.development 

python manage.py runserver --settings=cms.settings.development 

<<<<<<<<< Temporary merge branch 1
<//// para ejecutar ambiente de produccion
=========
# para ejecutar ambiente de produccion
>>>>>>>>> Temporary merge branch 2
python manage.py collectstatic --settings=cms.settings.production </// para coleccionar archivos estaticos en produccion, si hay cambios

python manage.py migrate --settings=cms.settings.production </// para migrar todas las tablas en produccion, si hay cambios en las tablas

python manage.py runserver --settings=cms.settings.production  <//// para ejecutar ambiente de produccion sin web service

uvicorn cms.asgi:application --host 127.0.0.1 --port 8000 --reload <//// ejecutar uvicorn asgi (servidor web asincrono)


<<<<<<<<< Temporary merge branch 1
gunicorn --env DJANGO_SETTINGS_MODULE=cms.settings.production cms.wsgi:application --bind 127.0.0.1:8000 <//// gunicorn no tiene soporte en windows, pero se podria hacer funcionar en un contenedor linux con docker

=========
>>>>>>>>> Temporary merge branch 2

python -m django_pydoc.py -b <////  DOCUMENTATION

ingresar a la carpeta donde estan los test y ejecutar en consola: pytest <////  Test
