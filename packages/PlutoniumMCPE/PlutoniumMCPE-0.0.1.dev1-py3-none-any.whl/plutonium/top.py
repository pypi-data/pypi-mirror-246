from bs4 import BeautifulSoup
import requests
import json
import pathlib

class top:
    def __init__(self) -> None:
        self.url = {
            'base': 'https://www.plutonium.best',
            'kill': '/stats/player/kill',
            'money': '/stats/player/money',
            'job': '/stats/player/job'
        }
    
    def vote(self):
        url = self.url['base']
        
        path = pathlib.Path(__file__).parent.resolve()
        with open(f'{path}\\assets\\headers.txt', 'r') as file:
            headers = json.load(file)
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            names = soup.find_all('p', class_='vote-name')
            votes = soup.find_all('p', class_='vote-details')
            
            result = {
                'code': response.status_code,
                'data': {}
            }
            
            for i in range(len(names)):
                result['data'][i+1] = {'name': names[i].get_text(), 'votes': votes[i].get_text().strip(' votes')}
            
            return result
    
    def kill(self):
        url = self.url['base'] + self.url['kill']
        
        path = pathlib.Path(__file__).parent.resolve()
        with open(f'{path}\\assets\\headers.txt', 'r') as file:
            headers = json.load(file)
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            topKill = soup.find_all('tr')[1:]
            
            result = {
                'code': response.status_code,
                'data': {}
            }
            
            for i in range(len(topKill)):
                playerTop = int(topKill[i].find_all('td')[0].get_text())
                
                name = topKill[i].find_all('td')[1].get_text()
                kills = topKill[i].find_all('td')[2].get_text()
                pourcentage = topKill[i].find_all('td')[5].get_text()
                
                result['data'][int(playerTop)] = {'name': name, 'kills': int(kills), 'pourcentage': pourcentage}
            
            return result
    
    def money(self):
        url = self.url['base'] + self.url['money']
        
        path = pathlib.Path(__file__).parent.resolve()
        with open(f'{path}\\assets\\headers.txt', 'r') as file:
            headers = json.load(file)
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            topMoney = soup.find_all('tr')[1:]
            
            result = {
                'code': response.status_code,
                'data': {}
            }
            
            for i in range(len(topMoney)):
                playerTop = int(topMoney[i].find_all('td')[0].get_text())
                
                name = topMoney[i].find_all('td')[1].get_text()
                money = topMoney[i].find_all('td')[2].get_text()
                pourcentage = topMoney[i].find_all('td')[5].get_text()
                
                result['data'][int(playerTop)] = {'name': name, 'kills': int(money), 'pourcentage': pourcentage}
            
            return result

        
    def job(self):
        url = self.url['base'] + self.url['job']
        
        path = pathlib.Path(__file__).parent.resolve()
        with open(f'{path}\\assets\\headers.txt', 'r') as file:
            headers = json.load(file)
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            topJob = soup.find_all('tr')[1:]
            
            result = {
                'code': response.status_code,
                'data': {}
            }
            
            for i in range(len(topJob)):
                playerTop = int(topJob[i].find_all('td')[0].get_text())
                
                name = topJob[i].find_all('td')[1].get_text()
                
                farmer = topJob[i].find_all('td')[2].get_text()
                killer = topJob[i].find_all('td')[3].get_text()
                lumberjack = topJob[i].find_all('td')[4].get_text()
                miner = topJob[i].find_all('td')[5].get_text()
                
                result['data'][int(playerTop)] = {'name': name, 'jobs': {'farmer': farmer, 'killer': killer, 'lumberjack': lumberjack, 'miner': miner}}
            
            return result