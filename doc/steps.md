# Passos para desenvolvimento

## From structure below (template do django + PostgreSQL + Docker):


### 1 - Iniciar o projeto em django "BinanceDataAPI"

    $ cd DataHandler
    $ django-admin startproject BinanceDataAPI  

### 2 - Conectar o banco de dados postgreSQL. 

No arquivo BinanceDataAPI/settings.py, acrescentar:

    if (os.environ.get('postgreSQL') == 'True'):

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('POSTGRES_DB=postgress_dev'),                      
                'USER': os.environ.get('POSTGRES_USER'),
                'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
                'HOST': os.environ.get('DB_HOST'),
                'PORT': os.environ.get('DB_PORT'), 
            }
        } 

Logo abaixo de:  

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

### 3 - Servir o jupyter notebook

i) Com virtualenv ativado e na pasta BinanceDataAPI:

    $ pip install jupyter
    $ pip install django-extensions

ii) Editar arquivo BinanceDataAPI/settings.py, para acrescentar django extensions:

    INSTALLED_APPS = (
        ...
        'django_extensions',
    )

    $ python manage.py shell_plus --notebook (já está na shell run.sh)

iii) Escolher o kernel "***Django Shell-Plus notebook***"

iv) Para consumir a API do djando, iniciar o notebook com:

    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myDjangoProject.settings")
    import django
    django.setup() 

Fonte: https://stackoverflow.com/questions/35483328/how-to-setup-jupyter-ipython-notebook-for-django

### 4 - Criar o app GetData

    $ python manage.py startapp GetData