#!/bin/sh

: '
Usage: ./run.sh <op>
<op>:
[0] - Production | Run the production cluster on a AWS, from remote container`s images.
[1] - Staging 1  | Run the production cluster (build and run) on local machine.
[2] - Delivery   | Build the containers` images and push them to specific docker registry.
[3] - Staging 2  | Run the production cluster on local machine, from remote container`s images.
[4] - Dev 1      | Up the dev database (build and run), for python tests on get_data and/or worker.
[5] - Dev 2      | Up the dev database and get_data (build and run), for python tests on worker.
[6] - Dev 3      | Run the dev cluster on local machine (build and run).==[1]
'

if [ $1 = 0 ]; then
    export env_file="/efs/.env"
else
    export env_file="dev.env"
fi

if [ -f $env_file ]; then

    if [ $1 = 1 ]; then

        #docker-compose -p $cluster_name down
        docker-compose build web #--no-cache
        docker-compose up #-d

    else
        echo "Opção inválida para o setup do cluster"

    fi

else
    echo 'Arquivo .env não encontrado.'
fi
