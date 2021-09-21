#!/bin/bash

: '
Usage: ./run.sh <op>
<op>:
[0] - Production | Run the production cluster on a AWS, from remote container`s images.
[1] - Staging 1  | Run the production cluster (build and run) on local machine.
[2] - Delivery   | Build the containers` images and push them to specific docker registry.
[3] - Staging 2  | Run the production cluster on local machine, from remote container`s images.
[4] - Dev 1      | Up the dev database (build and run), for python tests on get_data and/or worker.
[5] - Dev 2      | Up the dev database and get_data (build and run), for python tests on worker.
[6] - Dev 3      | Run the dev cluster on local machine (build and run).
'

if [ $1 = 0 ]; then
    export env_file="/efs/.env"
else
    export env_file="dev.env"
fi

if [ -f $env_file ]; then
    set -a
    . ./$env_file
    set +a

    if [ $1 = 0 ]; then
        #update the vm.max_map_count system limit:
        sudo sysctl -w vm.max_map_count=262144
        
        #Recupera o ID desta instância:
        instanceid=`/usr/bin/curl -s http://169.254.169.254/latest/meta-data/instance-id`
        #OBS.: É preciso liberar a porta 80 para este CIDR (169.254.169.254/32)

        #Associa o IP a esta instância
        aws ec2 associate-address --region $aws_default_region --instance-id $instanceid --public-ip $aws_instance_set_ip

        #Loga no host das imagens docker
        docker login $docker_image_host -u $registry_login -p $registry_password

        #Para o cluster e o renicia
        docker-compose -f ./docker-compose-remote.yml down
        docker-compose -f ./docker-compose-remote.yml -p $operation_name up -d 

        #rm -f .env #Uncomment for safe

    elif [ $1 = 1 ]; then
        sudo sysctl -w vm.max_map_count=262144
        
        docker-compose -f ./docker-compose-local.yml down
        docker-compose -f ./docker-compose-local.yml -p $operation_name build --no-cache
        docker-compose -f ./docker-compose-local.yml -p $operation_name up #-d
        
    elif [ $1 = 2 ]; then
        #Imagem do container get_data
        docker build --no-cache -t $docker_image_host/$image_path/get_data -f get_data/Dockerfile .

        #Imagem do worker
        docker build --no-cache -t $docker_image_host/$image_path/worker -f worker/Dockerfile .
        
        docker login $docker_image_host -u $registry_login -p $registry_password

        #Push das imagens
        docker push $docker_image_host/$image_path/get_data
        docker push $docker_image_host/$image_path/worker

    elif [ $1 = 3 ]; then
        sudo sysctl -w vm.max_map_count=262144

        docker login $docker_image_host -u $registry_login -p $registry_password

        docker-compose -f ./docker-compose-remote.yml down
        docker-compose -f ./docker-compose-remote.yml -p $operation_name up -d

    elif [ $1 = 4 ]; then
        sudo sysctl -w vm.max_map_count=262144
        
        docker-compose -f ./dev/src/compose1.yml down
        docker-compose -f ./dev/src/compose1.yml -p $operation_name build --no-cache
        docker-compose -f ./dev/src/compose1.yml -p $operation_name up #-d
        
    elif [ $1 = 5 ]; then
        sudo sysctl -w vm.max_map_count=262144
        
        docker-compose -f ./dev/src/compose2.yml down
        docker-compose -f ./dev/src/compose2.yml -p $operation_name build --no-cache
        docker-compose -f ./dev/src/compose2.yml -p $operation_name up #-d

    elif [ $1 = 6 ]; then
        sudo sysctl -w vm.max_map_count=262144
        
        docker-compose -f ./dev/src/compose3.yml down
        docker-compose -f ./dev/src/compose3.yml -p $operation_name build --no-cache
        docker-compose -f ./dev/src/compose3.yml -p $operation_name up #-d

    else
        echo "Opção inválida para o setup do cluster"

    fi

else
    echo 'Arquivo .env não encontrado.'
fi