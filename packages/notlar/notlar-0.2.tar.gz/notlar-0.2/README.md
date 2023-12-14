# ![Notlar Logo](notlar/static/img/notlar_logo_256.png)

Note: [English Readme](README.en.md).

Notlar es una aplicación web en Flask de gestión de notas. Podremos crear y eliminar notas por fechas haciendo uso de un calendario dinámico.

En el frontend se ha utilizado [tailwindcss](https://tailwindcss.com/), un Framework CSS que aunque tenga una curva de aprendizaje un poco complicada al principio, nos permitirá crear componentes de forma muy rápida y agilizar nuestro desarrollo. Se ha usado también el plugin [flowbite](https://flowbite.com/).

La aplicación es multiidioma. Se ha utilizado el módulo [Flask-Babel](https://python-babel.github.io/flask-babel/) como extensión de Flask que permite el soporte i18n para poder utilizar distintos lenguajes en nuestra aplicación.

Como base de datos utilizamos PostgreSQL.

La aplicación depende mucho de javascript. Al tener que interactuar con calendarios y notas, se han añadido muchos listeners, funciones que hacen fetch de distintos endpoints, etc.

Flask tiene un sistema de templates basado en jinja. Esto nos facilitará mucho el desarrollo y nos hará reducir la cantidad de código repetido. Podemos ver por ejemplo como en [notlar/templates/head.html](notlar/templates/head.html) cargamos los estilos de tailwind, el módulo de flowbite, jquery y en [notlar/templates/base.html](notlar/templates/base.html) se incluyen otras plantillas, entre ellas, el head. Luego en otras templates incluímos el base y de esta manera no tenemos que escribir todo el código del header, nav, footer, entre otros, en todas y cada una de las plantillas disponibles. De esta manera el código está dividido de mejor forma.

## Como ejecutar Notlar

Podemos levantar todo el escenario usando Docker compose. Debemos asegurarnos de tener [Docker](https://docs.docker.com/engine/install/) instalado y [Docker Compose](https://docs.docker.com/compose/install/).

1. Clonamos el repositorio donde se encuentra nuestro proyecto:

```bash
$ git clone https://gitlab.iessanclemente.net/dawd/a23adrianfa.git
$ cd notlar
```

2. Construimos e iniciamos la infrastructura con docker:

```bash
$ docker-compose up --build
```

Esto basicamente creará la imagen que se encuentra en el [Dockerfile](./Dockerfile) que será donde se encuentre nuestro backend con Flask e instalará todas las dependencias.

Tendremos 3 dockers ejecutándose:

- Uno con Flask que se ejecutará con gunicorn (servidor HTTP WSGI para ejecutar aplicaciones web de Python). Mucho mejor y más seguro ya que no es buena práctica usar el servidor web que viene con Flask por defecto.
- Uno con PostgreSQL que es donde se encontrará nuestra base de datos.
- Uno con Nginx que servirá como proxy inverso para redirigir nuestras peticiones. Suele ser buena practica ya que podríamos hacer infinidades de cosas con Nginx ya que es una capa adicional más. En este caso Nginx se encargará de gestionar las peticiones pero en un caso más avanzado podríamos configurar reglas de control de acceso, restricciones, balanceo de carga, etc.

La primera vez que lo ejecutemos se creará un volumen para el docker con PostgreSQL e importará y ejecutará automáticamente el fichero `notlar.sql` creando así toda la estructura de la base de datos.

Podemos ver en el [docker-compose.yml](./docker-compose.yml) que importamos un fichero de configuración de Nginx [nginx/nginx.conf](./nginx/nginx.conf) que contiene un dominio actualmente. Podemos modificarlo según el dominio que queramos usar:

```bash
$ sed 's/afusco.eu/mydomain.com/' nginx/nginx.conf
```

Podemos añadir el dominio `/etc/hosts` si es necesario:

```bash
$ grep afusco.eu /etc/hosts
127.0.0.1 afusco.eu
```

## Desarrollo

### Idiomas

Como hemos mencionado al principio, se ha utilizado `Flask-Babel` para el sistema de traducciones.

El fichero de configuración principal es [babel.cfg](babel.cfg). Aquí es donde definiremos que ficheros queremos escanear para su traducción:

e.g. Si queremos escanear todas las plantillas HTML debemos añadir:

```
[jinja2: **/templates/**.html]
```

Todas las palabras o frases que queramos traducir deberán ir de este modo:

```
{{ _('Insert here') }}
```

Se ha creado un [Makefile](Makefile) con distintos targets para automatizar el proceso. Podemos ejecutar:

```bash
$ make execute_translate
```

Este target hará lo siguiente:

- Comprobará que pybabel esté instalado.
- Escaneará los ficheros definidos en [babel.cfg](babel.cfg) y creará la plantilla principal de traducciones.
- Por cada uno de los idiomas definidos en la variable `AVAILABLE_LANGUAGES` creará una carpeta para ese idioma.

Para cada idioma tendremos ficheros `.po` que llenaremos con las traducciones, e.g.

```
msgid "Message"
msgstr "Mensaje"
```

Luego podremos ejecutar el target de nuevo y esto compilará las traducciones y tendremos los ficheros `.mo`.

### Base de Datos

PostgreSQL puede ser un poco confuso. Podemos ejecutar consultas directamente desde la CLI sin tener que acceder al contenedor, ejecutar sentencias SQL en psql, etc:

```
$ psql -U notlar -h $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' notlar_db) -d notlar -c "COPY (SELECT * FROM users) TO STDOUT WITH CSV HEADER"
Password for user notlar:
id,email,username,password,name,last_name,phone_number,telegram_user,profile_picture
25,adri@adri.com,adri@adri.com,pbkdf2:sha256:600000$P15dtIxIEOGyDjYG$8d4e56c4742391647f4e6e9ea6d68e4e887934b13927e0383888c7990547bc07,adrian,fusco,"","",
```

El SQL se encuentra en [notlar.sql](notlar.sql).

Estamos usando SQLAlchemy como ORM. Cada una de las tablas de la base de datos están mapeadas con clases.

### tailwindcss

Estamos usando [tailwindcss](https://tailwindcss.com/) como Framework CSS. El fichero de configuración se encuentra en [tailwind.config.js](tailwind.config.js).

Si añadimos cambios, nuevos componentes o plugins, debemos ejecutar el siguiente comando:

```bash
$ npx tailwindcss -i ./notlar/static/css/tailwind_input.css -o ./notlar/static/dist/css/output.css
```

Esto leera el fichero `tailwind_input.css` y el fichero `tailwind.config.js` que se encargará de escanear en todo el código que hayamos definido en el `content` los componentes. Si se ha agregado algún componente nuevo o eliminado, el [./notlar/static/dist/css/output.css](./notlar/static/dist/css/output.css) cambiará.

### tox.ini

[tox](https://tox.wiki/en/4.11.4/) es una manera de automatizar testing en aplicaciones basadas en Python.

En este caso hemos definido un fichero [tox.ini](tox.ini) que ejecutará los comandos `flake8` (para forzar la guía de estilos de Python PEP8 para buenas practicas) y yamllint (que buscará en los ficheros YAML definidos que haya una sintáxis correcta).

### CI/CD

En el fichero [.gitlab-ci.yml](.gitlab-ci.yml) tenemos el pipeline correspondiente que se encargará de ejecutar distintos stages que nos ayudarán con el desarrollo.

### scripts

En la carpeta [scripts](./scripts) se encontrarán scripts que facilitarán distintos procedimientos.

### Dependencias

Todas las dependencias de la aplicación en Flask se encuentran en el fichero [requirements.txt](./requirements.txt).

### Configuración de app y credenciales

La configuracion de la aplicación se encontrará en el fichero [notlar/__init__.py](notlar/__init__.py).

Aquí se inicializa Flask, Babel, SQLAlchemy, LoginManager y se define la configuración de cada uno de ellos.

Los parámetros de configuración estarán definidos en un fichero [.env](.env) en el que tendremos las variables de configuración de la aplicación.

### Rutas

Tendremos dos ficheros donde gestionaremos cada una de las rutas disponibles para hacer peticiones:

- [notlar/auth.py](notlar/auth.py): En este tendremos las rutas para login y registro.
- [notlar/routes.py](notlar/routes.py): En este tendremos el resto de rutas, tanto las que cargan las distintas vistas que existen (templates) como las que gestionan peticiones con las notas según calendario.


## Logo

Logo de la aplicación creado con: [NameCheap Logo Maker](https://www.namecheap.com/logo-maker/)

## Licencia

Copyright 2023.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
