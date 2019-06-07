#!/bin/sh

: '
Usage: ./run.sh <op>

<op>:

[0] - Dev                   - Export variables, run dev database, pgadmin notebooks and 
                             django servers.

[1] - Staging local 1       - Build and run the cluster with staging PostgreSQL DB container on 
                             local machine.

[2] - Delivery Staging      - Build the containers` RC images and push them to specific docker 
                             registry.

[3] - Staging local 2       - Run the production cluster on local machine, from remote container`s
                             images.

[4] - Delivery Production   - Build the containers` LATEST images and push them to specific docker 
                             registry.

[5] - Production            - Run the production cluster on a AWS, from remote container`s images.

'

if [ $1 = 5 ]; then
    export env_file="/efs/.env"
else
    export env_file="dev.env"
fi

if [ -f $env_file ]; then

    set -a
    . ./dev.env
    set +a

    if [ $1 = 0 ]; then

        export DB_HOST='localhost'

        docker-compose -f DockerCompose/dev1.yml down
        docker-compose -f DockerCompose/dev1.yml up -d

        #jupyter notebook > $PWD/logs/jupyterlog 2>&1 &

        source venv/bin/activate

        cd BinanceDataAPI

        #cd $DataHandlerDir

        sleep 60
        
        python manage.py makemigrations
        
        python manage.py migrate --noinput

        if [ $create_superuser = 'true' ]; then

        python manage.py shell -c "import os
from django.contrib.auth import get_user_model
User = get_user_model()
if (not User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_NAME')).exists()):
    User.objects.create_superuser(os.environ.get('DJANGO_SUPERUSER_NAME'), os.environ.get('DJANGO_SUPERUSER_MAIL'), os.environ.get('DJANGO_SUPERUSER_PASS'))
else:
    pass"
        fi

        #python manage.py shell_plus --notebook > $PWD/jupyterlog 2>&1 &

        python manage.py runserver $DJANGO_HOST:$DJANGO_PORT

    elif [ $1 = 1 ]; then

        #docker-compose -p $cluster_name down
        docker-compose build datahandler #--no-cache
        docker-compose up #-d

    else
        echo "Opção inválida para o setup do cluster"

    fi

else
    echo 'Arquivo .env não encontrado.'
fi