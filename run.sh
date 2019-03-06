#!/bin/bash

#Recupera o ID desta instância:
#instanceid=`/usr/bin/curl -s http://169.254.169.254/latest/meta-data/instance-id`
    #OBS.: É preciso liberar a porta 80 para este CIDR (169.254.169.254/32)

#Associa o IP a esta instância
#aws ec2 associate-address --region us-east-1 --instance-id $instanceid --public-ip 3.92.67.179

#Exporta as variáveis de ambiente no arquivo cluster.env

echo 'Lendo e exportando variáveis de ambiente'
set -a
. ./cluster.env
set +a

echo 'Lendo e exportando credenciais'
set -b
. ./credentials.env
set +b

#Limpando credenciais
#rm -f . ./credenciais.env

#Loga no registry
#docker login registry.gitlab.com -u $GITLAB_REGISTRY_LOGIN -p $GITLAB_REGISTRY_PASSWORD

echo 'Parando docker cluster'
#docker-compose down

echo 'Subindo cluster atachado a volume(s)'
#docker-compose up #&>/dev/null &
#&>/dev/null & "muta" a saida do docker-compose