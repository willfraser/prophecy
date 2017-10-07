import requests
import json
from pprint import pprint

def get_current_trades(book):
    url = 'https://bittrex.com/api/v1.1/public/getticker'
    payload = {'market': 'BTC-LTC'}
    r = requests.get(url,params=payload)
    values =r.json()
  
    pprint(values)
    
    return values['data']