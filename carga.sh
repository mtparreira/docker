#/bin/bash

/bin/rm -rf /root/docker/anaconda/python/*.sh

/usr/bin/docker exec devops_anaconda /bin/bash -c "python /home/python/twitter_carga.py"

/bin/sh /root/docker/anaconda/python/importar_registros_nosql.sh

/bin/rm -rf /root/docker/anaconda/python/*.sh
