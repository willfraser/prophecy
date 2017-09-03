import quadrigacx
import json
import requests
from pprint import pprint
import time
import hashlib
import hmac
from sig import hash


def printPrice():
    
    url = "https://api.quadrigacx.com/v2/ticker?book=eth_cad"
    
    r = requests.get(url)
    pprint(r.json())
    
    return

def printBalance():
  
    
    nonce =  int(time.time())
    
    message = str(nonce)+clientID+key
    
    signature = hash(message,secret)
    signature = str(signature)
    signature = str.lower(signature)
    
    url = "https://api.quadrigacx.com/v2/balance"
    payload = {'key': key, 'nonce': nonce, 'signature': signature} 
    r = requests.post(url, data=payload)
    pprint(r.json())

    return


print("Test Get Current Trades")
quadrigacx.get_current_trades("eth_btc")
print("Test Complete")

print("Test Get Open Book")
quadrigacx.get_open_book("eth_btc")
print("Test Complete")

print("Test Get Last Trades")
quadrigacx.get_recent_trades("eth_btc")
print("Test Complete")

print("Test Get Account Balance")
quadrigacx.get_account_balance()
print("Test Complete")  

print("Test Get User Transactions")
quadrigacx.get_user_transactions()
print("Test Complete")  

print("Test Get Open Orders")
quadrigacx.get_open_orders()
print("Test Complete") 

