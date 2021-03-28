# flask-mysql-0127

El presente proyecto utiliza la base de datos mysql con el ORM SQLAlchemy

## Instalación

```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Si queremos grabar en un archivo las dependencias que hemos instalado

```sh
$ pip freeze > requirements.txt
```

Asegurese de que la base de datos este encedida antes de utilzar el endpoint.

## Despliegue

Hacemos lo siguiente

```sh
$ python src/app.py
```