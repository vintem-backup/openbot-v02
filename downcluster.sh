#!/bin/sh

#export env_file="dev.env"
export env_file=$PWD'/dev/dev.env'

if [ -f $env_file ]; then

    set -a
    . ./dev/dev.env
    set +a

    if [ $1 = 'dev1' ]; then

        docker-compose -f DockerCompose/dev1.yml down

    elif [ $1 = 'staging1' ]; then

        docker-compose -f DockerCompose/staging1.yml down

    else
        echo "Opção inválida para o setup do cluster"

    fi

else
    echo 'Arquivo .env não encontrado.'
fi