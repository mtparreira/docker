#/bin/bash


# .ipynb_checkpoints
docker exec -it mongo_devops /bin/bash -c "mongoimport --host localhost --port 27017 --username usrtcc --password usrtcc --db tcc --collection twitters --type json --jsonArray --file /home/novos/.ipynb_checkpoints"
mv /root/docker/anaconda/python/coleta/.ipynb_checkpoints /root/docker/anaconda/python/carga/.ipynb_checkpoints

# 20618920514120210627133114.json
docker exec -it mongo_devops /bin/bash -c "mongoimport --host localhost --port 27017 --username usrtcc --password usrtcc --db tcc --collection twitters --type json --jsonArray --file /home/novos/20618920514120210627133114.json"
mv /root/docker/anaconda/python/coleta/20618920514120210627133114.json /root/docker/anaconda/python/carga/20618920514120210627133114.json

# 20618920514120210627135958.json
docker exec -it mongo_devops /bin/bash -c "mongoimport --host localhost --port 27017 --username usrtcc --password usrtcc --db tcc --collection twitters --type json --jsonArray --file /home/novos/20618920514120210627135958.json"
mv /root/docker/anaconda/python/coleta/20618920514120210627135958.json /root/docker/anaconda/python/carga/20618920514120210627135958.json
