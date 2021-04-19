# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 09:20:01 2021

@author: Administrador
"""

import requests
from bs4 import BeautifulSoup

townhall_name = 'Vigo'
resp = requests.get('https://irdgcdinfo.data.blog/ayuntamientos/')
soup = BeautifulSoup(resp.content.decode(), 'html.parser') # decodificamos el contenido de la respuesta para que lo lea como texto

dict = {}
for element in soup.find_all('tr'):
        columnas = element.find_all('th')
        dict[columnas[1].get_text()] = columnas[0].get_text()
        
print('Ayuntamiento:', townhall_name, '\nCódigo:', dict[townhall_name])
identificador = dict[townhall_name]
        
        
sky_resp = requests.get(f'http://servizos.meteogalicia.gal/rss/predicion/jsonPredConcellos.action?idConc={identificador}')    

sky_resp = sky_resp.json()   


sky_data = str(sky_resp['predConcello']['listaPredDiaConcello'][0]['ceo']['manha'])

    
code_sky = requests.get('https://irdgcdinfo.data.blog/codigos/')
soup2 = BeautifulSoup(code_sky.content.decode(), 'html.parser')

dict2 = {}
for element2 in soup2.find_all('tr'):
    columnas2 = element2.find_all('th')

    dict2[columnas2[0].get_text()] = columnas2[1].get_text()

  
sky_state = dict2[sky_data]
print('Estado del cielo por la mañana:', sky_state)