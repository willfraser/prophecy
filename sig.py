import time
import hashlib
import hmac
import config

def hash():
    key = config.get_key()
    secret = config.get_secret()
    clientID = config.get_clientID()
    
    nonce =  int(time.time())
    
    message = str(nonce)+clientID+key   
    message = bytes(message,'utf-8')
    byte_key = bytes(secret,'utf-8')
 
    signature = hmac.new(
    byte_key,
    message,
    hashlib.sha256
).hexdigest()
    
    return( {"key":key, "signature": str.lower(signature), "nonce": nonce})