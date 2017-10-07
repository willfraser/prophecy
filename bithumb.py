import requests
import json
from pprint import pprint

def get_ticker(currency):
    
    url = 'https://api.bithumb.com/public/ticker/'+currency
    r = requests.get(url)
    values =r.json()

    return values['data']['closing_price']