# Conversion csv - Prueba Liftit


### Variables de entorno
* Archivo de variables de entorno .env en la raíz del repositorio

```
SECRET_KEY
POSTGRES_PASSWORD
POSTGRES_USER
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
```

### Deploy development
* Construir y lanzar el proyecto en local y servidor de desarrollo
``` bash
docker-compose build --no-cache
docker-compose up

make migrate
make statics
make superuser

```

### Makefile
``` bash
# Crear y ejecutar migraciones
make migrate

# Instalar requerimientos de django/requirements.txt
make requirements

# Ejecutar collectstatic
make statics

# Crear superusuario
make superuser

# Crear app
make app APP_NAME=my_app

# Eliminar base de datos y migraciones
make clean

# Eliminar base de datos y volumenes de los contenedores
make reset
```