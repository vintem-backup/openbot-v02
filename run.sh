#!/bin/bash

: '
Usage: ./run.sh <op>
<op>:
[0] - Default | Run the cluster on a AWS, from remote container`s images.
[1] - Dev 1   | Run the cluster on local machine, from locally built container`s images.
[2] - Dev 2   | Build the containers` images and push them to specific docker registry.
[3] - Dev 3   | Run the cluster on local machine, from remote container`s images.
'

export env_file="dev.env"  

if [ $1 = 0 ]; then
    export env_file=".env"
    if [ -f .env ]; then
        set -a
        . ./.env
        set +a

        #update the vm.max_map_count system limit: 
        sudo sysctl -w vm.max_map_count=262144
    
        #Recupera o ID desta instância:
        instanceid=`/usr/bin/curl -s http://169.254.169.254/latest/meta-data/instance-id`
        #OBS.: É preciso liberar a porta 80 para este CIDR (169.254.169.254/32)

        #Associa o IP a esta instância
        aws ec2 associate-address --region $aws_default_region --instance-id $instanceid --public-ip $aws_instance_set_ip

        #Loga no host das imagens docker
        docker login $docker_image_host -u $registry_login -p $registry_password

        docker-compose -f ./docker-compose-remote.yml down
        docker-compose -f ./docker-compose-remote.yml -p $operation_name up -d 

        #rm -f .env #Uncomment for safe

    else
        echo 'Arquivo .env não encontrado.'

    fi

elif [ $1 = 1 ]; then
    if [ -f dev.env ]; then
        set -a
        . ./dev.env
        set +a

        #update the vm.max_map_count system limit: 
        sudo sysctl -w vm.max_map_count=262144
    
        docker-compose -f ./docker-compose-local.yml down
        docker-compose -f ./docker-compose-local.yml -p $operation_name build
        docker-compose -f ./docker-compose-local.yml -p $operation_name up #-d
    
    else
        echo 'Arquivo dev.env não encontrado.'

    fi

elif [ $1 = 2 ]; then
    if [ -f dev.env ]; then
        set -a
        . ./dev.env
        set +a
        
        #Imagem do container get_data
        docker build --no-cache -t $docker_image_host/$image_path/get_data -f get_data/Dockerfile .

        #Imagem do worker
        docker build --no-cache -t $docker_image_host/$image_path/worker -f worker/Dockerfile .
    
        #Loga no host das imagens docker
        docker login $docker_image_host -u $registry_login -p $registry_password

        #Push das imagens
        docker push $docker_image_host/$image_path/get_data
        docker push $docker_image_host/$image_path/worker

    else
        echo 'Arquivo dev.env não encontrado.'
    fi

elif [ $1 = 3 ]; then
    if [ -f dev.env ]; then
        set -a
        . ./dev.env
        set +a
        
        #update the vm.max_map_count system limit: 
        sudo sysctl -w vm.max_map_count=262144

        #Loga no host das imagens docker
        docker login $docker_image_host -u $registry_login -p $registry_password

        #Sobe o cluster
        docker-compose -f ./docker-compose-remote.yml down
        docker-compose -f ./docker-compose-remote.yml -p $operation_name up -d

    else
        echo 'Arquivo dev.env não encontrado.'
    fi

else
    echo "Opção inválida para o setup do cluster"

fi