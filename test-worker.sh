#!/bin/bash

#O contexto do build deve ser a home do projeto, a fim de tornar 
#possível a importação do módulo lib, comum aos containers get_data e worker;
#já o dockerfile é localizado através da flaf -f

set -a
. ./.env
set +a

docker rmi test_worker_img

docker build --no-cache -t test_worker_img -f worker/Dockerfile .

docker stop test_worker_ctn

docker container rm test_worker_ctn

docker run --env-file .env -it --name test_worker_ctn test_worker_img