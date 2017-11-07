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
            
        except requests.Timeout:
            time.sleep(.2)
            get_exchanged_value(amount, base, second)
            
        #print("Exchanged Value is:", usd_value )
    
    return usd_value
    
def get_exchanged_value_quandl(amount, base, second):
    
    if(second == "USD"):
        return 1
    else:
        url = 'http://www.quandl.com/api/v3/datasets/BOE'
        payload = {'base': base, 'symbols': second}
        #print(second)
        
        try:
            r = requests.get(url,params=payload)
            values =r.json()
        
            print(values)
            usd_value = float(amount)/float(values['rates'][second])
            
        except requests.Timeout:
            time.sleep(.2)
            get_exchanged_value(amount, base, second)
            
        #print("Exchanged Value is:", usd_value )
    
    
    https://api.fixer.io/latest
    
    return usd_value