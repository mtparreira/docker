# Carrega bibliotecas
import os

# Parametros iniciais
vg_comandos     = []
vg_dir_local    = '/home/python/'
vg_dir_servidor = '/root/docker/anaconda/python/'
vg_arquivos     = os.listdir(vg_dir_local+'coleta/')

# Comandos para carga automatizada NoSQL e guarda de coletas
if len(vg_arquivos) > 0:
    for v_arquivo in vg_arquivos:
        v_comando = ''
        if v_arquivo[v_arquivo.index('.'):] == '.json':
            v_comando =  '\n# '+v_arquivo+'\n'
            v_comando += '/usr/bin/docker exec devops_mongo /bin/bash -c'
            v_comando += ' "mongoimport --host localhost --port 27017 --username usrtcc --password usrtcc'
            v_comando += ' --db tcc --collection twitter'
            v_comando += ' --type json --jsonArray --file /home/coleta/'+v_arquivo+ '"\n'
            v_comando += '/usr/bin/mv '+vg_dir_servidor+'coleta/'+v_arquivo+' '+vg_dir_servidor+'carga/'+v_arquivo+'\n'
        vg_comandos.append(v_comando)

# Gerar script de importacao
with open(vg_dir_local+'importar_registros_nosql.sh', 'w') as v_arquivo:
    v_arquivo.write('#/bin/bash\n')
    for v_comando in vg_comandos:
        v_arquivo.write(v_comando)
