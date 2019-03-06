#!/bin/sh

#Credenciais
export AWS_ACCESS_KEY_ID=$K8S_SECRET_AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$K8S_SECRET_AWS_SECRET_ACCESS_KEY

#Recupera o Id da instância em produção
instanceid=`aws ec2 describe-instances --region us-east-1 --filters 'Name=tag:Name,Values=Tlg_msg_pipeline' --output text --query 'Reservations[*].Instances[*].InstanceId'`
    #OBS.: O nome deve coincidir com aquele usado pela instância, neste caso "Tlg_msg_pipeline"

#Termina a instância
aws ec2 terminate-instances --region us-east-1 --instance-id $instanceid