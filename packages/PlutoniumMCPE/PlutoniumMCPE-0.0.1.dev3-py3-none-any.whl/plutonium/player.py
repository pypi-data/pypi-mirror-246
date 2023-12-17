from bs4 import BeautifulSoup
import requests
import json
import pathlib

from plutonium.assets.headers import headers as h

class player:
    def __init__(self) -> None:
        self.url = {
            'base': 'https://www.plutonium.best',
            'profil' : '/stats/profil/[name]',
            
            'head': 'https://cdn.plutonium.best/[name]/head',
            'body': 'https://cdn.plutonium.best/[name]/body'
        }
    
    def get(self, name:str):
        url = self.url['base'] + self.url['profil'].replace('[name]', name)
        
        path = pathlib.Path(__file__).parent.resolve()
        headers = h().variable
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code != 200:
            return {'code': response.status_code, 'data': None}
        elif soup.find(class_="contener") != None and soup.find(class_="contener").find('h1') == 'Chemin inconnu':
            return {'code': 404, 'data': None}
        else:
            rank = soup.find('p', class_='legende').find('span').get_text().strip('[').strip(']')
            
            classement = soup.find_all('p', class_='classement')

            kills = soup.find(class_="card kill").find('p').get_text()
            money = soup.find(class_="card money").find('p').get_text()
            
            jobsLevel = soup.find_all(class_="level-job")
            jobsExp = soup.find_all(class_="pourcent-job")
            
            return {
                'code': response.status_code,
                'data': {
                    'rank': rank,
                    'head': self.url['head'].replace('[name]', name),
                    'body': self.url['body'].replace('[name]', name),
                    'kills': {
                        'amount': kills,
                        'top': classement[0].get_text()
                    },
                    'money': {
                        'amount': money,
                        'top': classement[1].get_text()
                    },
                    'jobs': {
                        'farmer': {
                            'level': jobsLevel[0].get_text().strip('Niveau '),
                            'exp': jobsExp[0].get_text()
                        },
                        'Miner': {
                            'level': jobsLevel[1].get_text().strip('Niveau '),
                            'exp': jobsExp[1].get_text()
                        },
                        'Lumberjack': {
                            'level': jobsLevel[2].get_text().strip('Niveau '),
                            'exp': jobsExp[2].get_text()
                        },
                        'Killer': {
                            'level': jobsLevel[3].get_text().strip('Niveau '),
                            'exp': jobsExp[3].get_text()
                        }
                    }
                }
            }