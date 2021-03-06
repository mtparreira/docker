# Carrega bibliotecas
import unicodedata
import configparser
import pandas as pd

from TwitterSearch import *
from datetime import datetime

# Parametros iniciais
vg_conta      = ''
vg_log        = []
vg_registros  = []
vg_resultado  = pd.DataFrame()
vg_pasta      = '/home/python/'
vg_ini        = configparser.ConfigParser()
vg_hora       = int(datetime.today().strftime('%M'))
vg_arquivo    = datetime.today().strftime('%Y%m%d%H%M%S')

# Chaves de pesquisa
vg_pesquisas  = ['Playstation','Xbox','Nintendo','Blizzard', 'Activision', 'Naughty Dog', 'EA', 'Konami','Capcom', 'Nintendo Switch Online', 'Gamepass', 'EA Access', 'Playstation Now', 'CD PROJEKT RED']

# Minera dados no Twitter
vg_ini.read(vg_pasta+'/parametros.ini')

# Define conta para coleta
if vg_hora < 10:
    vg_conta = 'ts_app_01'
elif vg_hora < 20:
    vg_conta = 'ts_app_11'
elif vg_hora < 30:
    vg_conta = 'ts_app_21'
elif vg_hora < 40:
    vg_conta = 'ts_app_31'
elif vg_hora < 50:
    vg_conta = 'ts_app_41'
elif vg_hora < 60:
    vg_conta = 'ts_app_51'

# Para cada chave de pesquisa
for v_index, v_pesquisa in enumerate(vg_pesquisas):    
    
    # Controle de 10 tentativas
    v_controle = 0
    while v_controle < 10:
        v_tso = None
        v_tcc_app_01 = None
        v_controle += 1
        vg_log.append([datetime.today().strftime('%Y-%m-%d %H:%M:%S') \
                      +' Tentativa -> '+format(v_controle,'02') \
                      +' | Pesquisa -> '+v_pesquisa])
        
        try:
            # Credenciais do Twitter
            v_ts = TwitterSearch(
                consumer_key = vg_ini[vg_conta]['consumer_key'],
                consumer_secret = vg_ini[vg_conta]['consumer_secret'],
                access_token = vg_ini[vg_conta]['access_token'],
                access_token_secret = vg_ini[vg_conta]['access_token_secret']
            )
            
            # Filtros para pesquisa
            v_tso = TwitterSearchOrder()
            v_tso.set_count(100)
            v_tso.set_locale('en')
            v_tso.set_language('en')            
            v_tso.set_keywords([v_pesquisa])
            v_tso.set_include_entities(False) 
            
            # Coleta
            for v_tweet in v_ts.search_tweets_iterable(v_tso):
                v_texto = v_tweet['text']
                v_texto = v_texto.replace('"','')
                vg_registros.append([datetime.today().strftime('%Y-%m-%d')
                                    ,datetime.today().strftime('%H:%M:%S')
                                    ,vg_ini['coletor']['ip']
                                    ,v_pesquisa
                                    ,v_tweet['user']['screen_name']
                                    ,v_texto])
            
            v_controle = 10
            vg_log.append([datetime.today().strftime('%Y-%m-%d %H:%M:%S')+' Extra????o realizada'])
            
        except:
            vg_log.append([datetime.today().strftime('%Y-%m-%d %H:%M:%S')+' Falha na extra????o'])

# Armazena coleta
if len(vg_registros) > 0:
    vg_resultado = pd.DataFrame(vg_registros)
    vg_resultado.index.name='indice'
    vg_resultado.columns = ['data_coleta','hora_coleta','ip_coletor','chave_pesquisa','twitter','tweet']
    v_duplicados = vg_resultado['tweet'].count()
    vg_resultado.drop_duplicates(['tweet'],inplace=True)
    v_duplicados = v_duplicados-vg_resultado['tweet'].count()
    vg_log.append(['Foram removidas '+str(v_duplicados)+' duplicidades'])
    vg_log.append(['Foram coletados '+str(vg_resultado.tweet.count())+' tweets'])
    vg_resultado.to_json(vg_pasta+'coleta/'+vg_ini['coletor']['ip'].replace('.','')+vg_arquivo+'.json',orient="records")

# Armazena log
vg_log = pd.DataFrame(vg_log)
vg_log.to_csv(vg_pasta+'log/'+vg_ini['coletor']['ip'].replace('.','')+vg_arquivo+'.log',columns=None,header=False,index=False)
