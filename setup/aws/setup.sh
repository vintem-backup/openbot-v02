#!/bin/bash

#Preparado para amazon linux 2

#Atualizando
sudo yum update -y
sudo yum upgrade -y

#Nginx
sudo amazon-linux-extras install nginx1.12 -y
sudo systemctl start nginx
sudo systemctl enable nginx

#Docker
sudo amazon-linux-extras install docker -y
sudo systemctl start docker
sudo systemctl enable docker

#Variáveis de ambiente
#credenciais
nano credentials.txt #Copie e cole o conteúdo de credentials.txt para este arquivo no servidor, salvando em seguida.

#Outras Variáveis
nano environmet #Copie e cole o conteúdo de environment para este arquivo no servidor, salvando em seguida.

#Shell run_app.sh (no diretório /home/ec2-user/)
nano run_app.sh #Copie e cole o conteúdo de run_app.sh para este arquivo no servidor, salvando em seguida.
chmod +x run_app.sh #Torna o script executável

#Criando script na inicianização
sudo su
nano /etc/systemd/system/run_app.service #Copie e cole o conteúdo de run_app.service para este arquivo no servidor, salvando em seguida.
systemctl enable run_app.service         #Faz com que o serviço inicie com o início do linux (deamon)