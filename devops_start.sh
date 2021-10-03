#/bin/bash

# Montando ambiente devops
echo "\e[01;33mMontando ambiente devops\e[00m"
docker-compose -f /root/docker/docker-compose.yml up -d

# Instalando bibliotecas complementares
echo "\e[01;33mInstalando bibliotecas Python complementares\e[00m"
docker exec -it devops_anaconda pip install pymongo
docker exec -it devops_anaconda pip install configparser
docker exec -it devops_anaconda pip install TwitterSearch
docker exec -it devops_anaconda pip install contractions==0.0.18
docker exec -it devops_anaconda pip install inflect
docker exec -it devops_anaconda pip install nltk
docker exec -it devops_anaconda pip install emojis

# Aguardando carga de serviço notebook
echo "\e[01;33mCarregando serviço notebook\e[00m"
sleep 10

# Verificando token de acesso serviço notebook
echo "\e[01;33mVerificando token de acesso ao serviço notebook\e[00m"
docker exec -it devops_anaconda /bin/bash -c "jupyter notebook list > /home/tokenrun"
sh token.sh
