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
        #print(columnas[1].get_text(), columnas[0].get_text())
        dict[columnas[1].get_text()] = columnas[0].get_text()
        
print(townhall_name, dict[townhall_name])
        
        
        
                
        