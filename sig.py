import time
import hashlib
import hmac
import requests
import config
import calendar

def hash():
    
#    url = "https://api.heroku.com/apps/frozen-garden-83591/config-vars"
#    r = requests.get(url)
#    values = r.json()

    key = config.get_key()
    secret = config.get_secret()
    clientID = config.get_clientID()
    
    
    nonce =  int(time.time()*1000000)+374491605044
    

    
    message = str(nonce)+clientID+key   
    message = bytes(message,'utf-8')
    byte_key = bytes(secret,'utf-8')
 
    signature = hmac.new(
    byte_key,
    message,
    hashlib.sha256
).hexdigest()
    
    return( {"key":key, "signature": str.lower(signature), "nonce": nonce})