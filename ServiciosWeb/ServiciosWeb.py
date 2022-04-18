# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 09:20:01 2021

@author: Borja Souto Prego
"""

import requests
from bs4 import BeautifulSoup
from gmg import gmg

if __name__=="__main__":

    townhall_list = ['Verín', 'Vigo', 'Santiago de Compostela', 'Burela', 'Viveiro', 'Ponteceso', 'Lugo', 'Guitiriz', 'Tui', 'Ribadavia']
    resp = requests.get('https://irdgcdinfo.data.blog/ayuntamientos/')
    soup = BeautifulSoup(resp.content.decode(), 'html.parser') 
    
    map_list = []
    
    dict = {}
    
    for element in soup.find_all('tr'):
            columnas = element.find_all('th')
            dict[columnas[1].get_text()] = columnas[0].get_text()

    for townhall in townhall_list:
    
        townhall_name = townhall 
        
        print('Ayuntamiento:', townhall_name, '\nCódigo de ayuntamiento:', dict[townhall_name])
        identificador = dict[townhall_name]
                
        sky_resp = requests.get(f'http://servizos.meteogalicia.gal/rss/predicion/jsonPredConcellos.action?idConc={identificador}')    
        
        sky_resp = sky_resp.json()   
        
        sky_data = str(sky_resp['predConcello']['listaPredDiaConcello'][0]['ceo']['manha'])
        
        print('Código de estado del cielo:', sky_data)
          
        code_sky = requests.get('https://irdgcdinfo.data.blog/codigos/')
        soup2 = BeautifulSoup(code_sky.content.decode('utf-8'), 'html.parser')
        
        dict2 = {}
        for element2 in soup2.find_all('tr'):
            columnas2 = element2.find_all('th')
        
            dict2[columnas2[0].get_text()] = columnas2[1].get_text()
        
        sky_state = dict2[sky_data]
        print('Estado del cielo por la mañana:', sky_state)
        
        coords_resp = requests.get('https://eu1.locationiq.com/v1/search.php?key=pk.e9566b1abfca4228171ce88e459b94aa&q='+townhall_name+'&format=xml')
        coords_soup = BeautifulSoup(coords_resp.content.decode('utf-8'), 'lxml')
        
        list_place = []
        
        for element3 in coords_soup.find_all('place'):
            list_place.append(element3)
    
        list_importance = []
        
        for i in range(len(list_place)):
            imp = float(list_place[i]['importance'])
            list_importance.append(imp)
        importance = max(list_importance)
        
        for e in range(len(list_place)):
            if float(list_place[e]['importance']) == importance:
                lat = list_place[e]['lat']
                lon = list_place[e]['lon']
                
        print('Latitud:', lat)
        print('Longitud:', lon)
        print('-'*50)
        
        map_list.append([sky_data, [lon, lat]])
    
    gmg.plotMap(map_list)
    
