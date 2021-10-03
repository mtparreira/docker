#!/bin/bash

echo "rodou `date`" >> cl.txt
sh /root/docker/coleta.sh
sh /root/docker/carga.sh
