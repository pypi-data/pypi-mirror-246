from bs4 import BeautifulSoup
import requests
import json
import pathlib

from plutonium.assets.headers import headers as h

class bounty:
    def __init__(self) -> None:
        self.url = {
            'base': 'https://www.plutonium.best'
        }
    
    def getHighest(self):
        url = self.url['base']
        
        path = pathlib.Path(__file__).parent.resolve()
        headers = h().variable
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        else:
            name = soup.find('p', class_='wanted-name').get_text()
            reward = soup.find('p', class_='wanted-reward').get_text()
            
            return {
                'code': response.status_code,
                'data': {
                    'name': name,
                    'reward': reward
                }
            }