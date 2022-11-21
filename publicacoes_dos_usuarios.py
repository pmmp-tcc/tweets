

Importando Bibliotecas necessarias
"""

import os
import tweepy
import pandas as pd

"""Alterando o diretorio 

"""

Path = '/content/drive/MyDrive/Projeto ITS'

os.chdir(Path)

"""Fazendo autenticação da conta google para ter acesso as planilhas do Drive"""

from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default
creds, _ = default()

gc = gspread.authorize(creds)

"""Abrindo planilha do drive"""

sh = gc.open('faltantes_bot')
worksheet = sh.get_worksheet(0)
ids = worksheet.col_values(1)
ids = ids[1:]
df = pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])

df.head()

"""Pegando apenas os ID de casa usuario na planilha"""

ids = df.id.values

import random

"""Pegando uma amostra de tamanho 50"""

# amostra = random.sample(ids, 50)
amostra = ids

"""Alterando o diretorio para a pasta que contem as chaves de autenticação, o arquivo secret."""

Path = '/content/drive/MyDrive/Colab Notebooks'

os.chdir(Path)

from secret import *

"""O bloco abaixo está extraindo os 50 últimos tweets de cada conta da amostra"""

import time
json = list()

for c in range(len(amostra)):
  time.sleep(1)
  try:
    for tweet in api.user_timeline(user_id=amostra[c], count = 50):
      json.append(tweet._json) 
  except Exception as erro:
    print(f'Error: {erro.__class__}')

"""Proximo bloco está extraindo variaveis que um tweet pode fornecer"""

value = list()
for i in range(len(json)):
      value.append([])
      value[i].append(json[i]['user']['id'])
      value[i].append(json[i]['created_at'])
      value[i].append(json[i]['id_str'])
      value[i].append(json[i]['text'])
      value[i].append(json[i]['lang'])
      value[i].append(json[i]['source'])
      value[i].append(json[i]['in_reply_to_screen_name'])
      value[i].append(json[i]['geo'])
      value[i].append(json[i]['coordinates'])
      value[i].append(json[i]['place'])
      value[i].append(json[i]['contributors'])
      value[i].append(json[i]['is_quote_status'])
      value[i].append(json[i]['retweet_count'])
      value[i].append(json[i]['favorite_count'])
      value[i].append(json[i]['favorited'])
      value[i].append(json[i]['retweeted'])

keys = ['user', 'created_at', 'id_srt', 'text', 'lang', 'source', 'in_reply_to ',
        'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', 'retweet_count',
        'favorite_count', 'favorited', 'retweeted']

"""salvando em csv"""

df = pd.DataFrame(value, columns = keys)
df.head()

df.to_csv('tweets.csv', na_rep='Na', index = False)
