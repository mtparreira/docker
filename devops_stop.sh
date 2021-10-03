#/bin/bash

# Desmontando ambiente devops
echo "\e[01;33mDesmontando ambiente devops\e[00m"
docker-compose -f /root/docker/docker-compose.yml down
