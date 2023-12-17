from bs4 import BeautifulSoup
import requests
import json
import pathlib

from plutonium.assets.headers import headers as h

class practice:
    def __init__(self) -> None:
        self.url = {
            'base': 'https://www.plutonium.best',
            'build': '/stats/practice/build',
            'gapple': '/stats/practice/gapple',
            'nodebuff': '/stats/practice/nodebuff',
            'sumo': '/stats/practice/sumo'
        }

        
    def build(self):
        url = self.url['base'] + self.url['build']
        
        path = pathlib.Path(__file__).parent.resolve()
        headers = h().variable
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            topPractice = soup.find_all('tr')[1:]
            
            result = {
                'code': response.status_code,
                'data': {}
            }
            
            for i in range(len(topPractice)):
                playerTop = int(topPractice[i].find_all('td')[0].get_text())
                
                name = topPractice[i].find_all('td')[1].get_text()
                
                kills = topPractice[i].find_all('td')[2].get_text()
                deaths = topPractice[i].find_all('td')[3].get_text()
                ratio = topPractice[i].find_all('td')[4].get_text()
                
                result['data'][int(playerTop)] = {'name': name, 'kills': kills, 'deaths': deaths, 'ratio': ratio}
            
            return result
    
    def gapple(self):
        url = self.url['base'] + self.url['gapple']
        
        path = pathlib.Path(__file__).parent.resolve()
        headers = h().variable
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            topPractice = soup.find_all('tr')[1:]
            
            result = {
                'code': response.status_code,
                'data': {}
            }
            
            for i in range(len(topPractice)):
                playerTop = int(topPractice[i].find_all('td')[0].get_text())
                
                name = topPractice[i].find_all('td')[1].get_text()
                
                kills = topPractice[i].find_all('td')[2].get_text()
                deaths = topPractice[i].find_all('td')[3].get_text()
                ratio = topPractice[i].find_all('td')[4].get_text()
                
                result['data'][int(playerTop)] = {'name': name, 'kills': kills, 'deaths': deaths, 'ratio': ratio}
            
            return result
    
    def nodebuff(self):
        url = self.url['base'] + self.url['nodebuff']
        
        path = pathlib.Path(__file__).parent.resolve()
        headers = h().variable
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            topPractice = soup.find_all('tr')[1:]
            
            result = {
                'code': response.status_code,
                'data': {}
            }
            
            for i in range(len(topPractice)):
                playerTop = int(topPractice[i].find_all('td')[0].get_text())
                
                name = topPractice[i].find_all('td')[1].get_text()
                
                kills = topPractice[i].find_all('td')[2].get_text()
                deaths = topPractice[i].find_all('td')[3].get_text()
                ratio = topPractice[i].find_all('td')[4].get_text()
                
                result['data'][int(playerTop)] = {'name': name, 'kills': kills, 'deaths': deaths, 'ratio': ratio}
            
            return result
    
    def sumo(self):
        url = self.url['base'] + self.url['sumo']
        
        path = pathlib.Path(__file__).parent.resolve()
        headers = h().variable
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            topPractice = soup.find_all('tr')[1:]
            
            result = {
                'code': response.status_code,
                'data': {}
            }
            
            for i in range(len(topPractice)):
                playerTop = int(topPractice[i].find_all('td')[0].get_text())
                
                name = topPractice[i].find_all('td')[1].get_text()
                
                kills = topPractice[i].find_all('td')[2].get_text()
                deaths = topPractice[i].find_all('td')[3].get_text()
                ratio = topPractice[i].find_all('td')[4].get_text()
                
                result['data'][int(playerTop)] = {'name': name, 'kills': kills, 'deaths': deaths, 'ratio': ratio}
            
            return result