from bs4 import BeautifulSoup
import requests
import json
import pathlib

class server:
    def __init__(self) -> None:
        self.url = {
            'base': 'https://www.plutonium.best'
        }
    
    def info(self):
        url = self.url['base']
        
        path = pathlib.Path(__file__).parent.resolve()
        with open(f'{path}\\assets\\headers.txt', 'r') as file:
            headers = json.load(file)
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            serverStats = soup.find_all('p', class_='server-stats')
            
            onlinePlayers = serverStats[0].find('span').get_text()
            registeredPlayers = serverStats[1].find('span').get_text().replace(" ", "")
            
            return {
                'code': response.status_code,
                'data': {
                    'onlinePlayers': int(onlinePlayers),
                    'registeredPlayers': int(registeredPlayers)
                }
            }