# Cms
Este es el repositorio del proyecto de Ingeniería de Software 2.
[![cms1.png](https://i.postimg.cc/SNT6j6TQ/cms1.png)](https://postimg.cc/mt9z5HWK)
## Comandos

### 1. **Ambiente de Desarrollo**
Para configurar y ejecutar el entorno de desarrollo, sigue estos pasos:
1. **Instalar dependencias**:
```BASH
pip install -r requirements.txt
```
2. **Crear migraciones**:
```bash
python manage.py makemigrations --settings=cms.settings.development
```
3. **Aplicar migraciones**:
```bash
python manage.py migrate --settings=cms.settings.development 
```
4. **Ejecutar el servidor de desarrollo**:
```bash
python manage.py runserver --settings=cms.settings.development 
```
### 2. **Ambiente de Producción**
Para ejecutar el entorno de producción, utiliza los siguientes comandos según sea necesario:
1. **Coleccionar archivos estáticos** (solo si hay cambios):
```bash
python manage.py collectstatic --settings=cms.settings.production
```
2. **Migrar las tablas en producción** (si hay cambios en las tablas):
```bash
python manage.py migrate --settings=cms.settings.production 
```
3. **Ejecutar el servidor de producción** (sin web service):
```bash
python manage.py runserver --settings=cms.settings.production  
```
### 3. **Ejecutar Uvicorn (Servidor Web Asíncrono)**
Para ejecutar el servidor web asíncrono, usa el siguiente comando:

```bash
uvicorn cms.asgi:application --host 127.0.0.1 --port 8000 --reload 
```
### 4. **Generar Documentación**
```
python -m django_pydoc.py -b 
```
### 3. **Ejecutar Tests**
Para ejecutar los tests, ingresa a la carpeta donde están los archivos de prueba y ejecuta:
```bash
pytest
``` 
