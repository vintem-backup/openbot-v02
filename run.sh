#!/bin/bash

#Exporting environment variables
set -a
. ./.env
set +a

#update the vm.max_map_count system limit: 
sudo sysctl -w vm.max_map_count=262144

if [ "$run_set" = "from_build" ]
then
    docker-compose -f ./compose/local.yml down
    docker-compose -f ./compose/local.yml -p $operational_name up #-d'

elif [ "$run_set" = "aws" ]
then
    #Recupera o ID desta instância:
    instanceid=`/usr/bin/curl -s http://169.254.169.254/latest/meta-data/instance-id`
    #OBS.: É preciso liberar a porta 80 para este CIDR (169.254.169.254/32)

    #Associa o IP a esta instância
    aws ec2 associate-address --region $aws_default_region --instance-id $instanceid --public-ip $aws_instance_set_ip

    #Loga no host das imagens docker
    docker login $docker_image_host -u $GITLAB_REGISTRY_LOGIN -p $GITLAB_REGISTRY_PASSWORD

    docker-compose -f ./compose/remote.yml down
    docker-compose -f ./compose/remote.yml -p $operational_name up -d 

    rm -f . ./.env

else
    echo "Not a valid environment"
fi