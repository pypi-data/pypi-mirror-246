from setuptools import setup

description = """\
Plutonium MCPE Scraper est un module Python qui extrait et organise les informations de statistiques à partir du site de Plutonium MCBE, les présentant sous forme de dictionnaire propre.

## Utilisation

Obtention des statistiques d'un joueur
```python
import plutonium

name = 'Cylion LM'

playerClass = plutonium.player()
data = playerClass.get(name)
```

### Valeur de 'data'
```
{'code': 200, 'data': {'rank': 'Joueur', 'head': 'https://cdn.plutonium.best/Cylion LM/head', 'body': 'https://cdn.plutonium.best/Cylion LM/body', 'kills': {'amount': '0', 'top': '#8155'}, 'money': {'amount': '15189', 'top': '#439'}, 'jobs': {'farmer': {'level': '0', 'exp': '0%'}, 'Miner': {'level': '0', 'exp': '0%'}, 'Lumberjack': {'level': '0', 'exp': '0%'}, 'Killer': {'level': '0', 'exp': '0%'}}}}
```

## License

Copyright (c) 2023 LocheMan
"""

setup(
    name='PlutoniumMCPE',

    version='0.0.1.dev3',

    description='Plutonium MCPE Scraper',

    url="https://github.com/LocheMan/",

    author='LocheMan',
    
    include_package_data=True,

    install_requires=['requests', 'beautifulsoup4'],

    keywords=['plutonium', 'mcpe', 'mcbe'],

    long_description=description,
    long_description_content_type='text/markdown',
)