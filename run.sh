#!/bin/bash

#Exporta as variáveis de ambiente no arquivo cluster.env
set -a
. ./cluster.env
set +a

echo 'Parando docker cluster'
docker-compose down

echo 'Subindo cluster atachado a volume(s)'
docker-compose up &>/dev/null &
#&>/dev/null & "muta" a saida do docker-compose