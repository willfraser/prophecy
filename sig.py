import time
import hashlib
import hmac
import requests
import config
import calendar
import base64
import urllib.parse

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
    
def get_kraken_sig(urlpath, data ={}):
    
    key = config.get_kraken_key()
    secret = config.get_kraken_secret()
    otp = config.get_kraken_otp()

    nonce =  int(time.time()*1000)
    data = {"nonce" : nonce}
    postdata = urllib.parse.urlencode(data)

    # Unicode-objects must be encoded before hashing
    encoded = (str(nonce) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    signature = hmac.new(base64.b64decode(secret),
                             message, hashlib.sha512)
    sigdigest = base64.b64encode(signature.digest())
    
    return( {"key":key, "signature": sigdigest.decode(), "data": data})