import requests
import json
from pprint import pprint

def get_exchanged_value(amount, base, second):
    
    if(second == "USD"):
        return 1
    else:
        url = 'http://api.fixer.io/latest'
        payload = {'base': base, 'symbols': second}
        #print(second)
        
        try:
            r = requests.get(url,params=payload)
            values =r.json()
        
            print(values)
        
            usd_value = float(amount)/float(values['rates'][second])
        
        #print("Exchanged Value is:", usd_value )
    
    return usd_value