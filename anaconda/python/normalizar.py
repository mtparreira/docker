import re
import inflect
import unicodedata
import contractions

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk        import word_tokenize
from nltk.corpus import stopwords
from nltk.stem   import LancasterStemmer, WordNetLemmatizer

import pandas as pd
from pymongo import MongoClient

def remove_nao_ascii(palavras):
    novas_palavras = []
    for palavra in palavras:
        nova_palavra = unicodedata.normalize('NFKD', palavra).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        novas_palavras.append(nova_palavra)
    return novas_palavras

def caixa_baixa(palavras):
    novas_palavras = []
    for palavra in palavras:
        nova_palavra = palavra.lower()
        novas_palavras.append(nova_palavra)
    return novas_palavras

def remove_pontuacao(palavras):
    novas_palavras = []
    for palavra in palavras:
        nova_palavra = re.sub(r'[^\w\s]', '', palavra)
        if nova_palavra != '':
            novas_palavras.append(nova_palavra)
    return novas_palavras

def troca_numero_palavra(palavras):
    novas_palavras = []
    ie = inflect.engine()
    for palavra in palavras:
        if palavra.isdigit():
            nova_palavra = ie.number_to_words(palavra)
            novas_palavras.append(nova_palavra)
        else:
            novas_palavras.append(palavra)
    return novas_palavras

def remove_stopwords(palavras):
    novas_palavras = []
    for palavra in palavras:
        if palavra not in stopwords.words('english'):
            novas_palavras.append(palavra)
    return novas_palavras

def tratar_troncos(palavras):    
    stems = []
    stemmer = LancasterStemmer()
    for palavra in palavras:
        stem = stemmer.stem(palavra)
        stems.append(stem)
    return stems

def tratar_verbos(palavras):    
    lemmas = []
    lemmatizer = WordNetLemmatizer()
    for palavra in palavras:
        lemma = lemmatizer.lemmatize(palavra, pos='v')
        lemmas.append(lemma)
    return lemmas

def normalizar(palavras):
    palavras = remove_nao_ascii(palavras)
    palavras = caixa_baixa(palavras)
    palavras = remove_pontuacao(palavras)
    palavras = troca_numero_palavra(palavras)
    palavras = remove_stopwords(palavras)    
    palavras = tratar_verbos(palavras)
    #palavras = tratar_troncos(palavras)
    return palavras

mc = MongoClient('mongodb://usrtcc:usrtcc@206.189.205.141:27017/?authSource=tcc&readPreference=primary&ssl=false')
db = mc.tcc

twitters = db.twitters

bagofwords = db.bagofwords
bagofwords.drop()

id = ''
bolsa = ''
documento = ''

dias = list(db.twitters.distinct('data_coleta'))
for dia in dias:
    cursor = twitters.find({'data_coleta': dia})
    for documento in cursor:       
        id = documento['_id']
        bolsa = documento['tweet']
        bolsa = re.sub(r"http\S+", "", bolsa)
        bolsa = contractions.fix(bolsa)
        bolsa = nltk.word_tokenize(bolsa)
        bolsa = normalizar(bolsa)
        bolsa = list(dict.fromkeys(bolsa))
        documento = {
            '_id': id,
            'bolsa': bolsa
        }
        db.bagofwords.insert_one(documento).inserted_id
    print(dia)
