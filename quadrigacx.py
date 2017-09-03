import requests
import json
import sig
import time
from pprint import pprint

def get_current_trades(book):
    url = "https://api.quadrigacx.com/v2/ticker?book="+book
    r = requests.get(url)
    values = r.json()
    
    return values

def get_open_book(book):
    url = "https://api.quadrigacx.com/v2/order_book"
    payload = {'book': book} 
    r = requests.post(url,data=payload)
    values = r.json()
    
    return values

def get_recent_trades(book,time="hour"):
    url = "https://api.quadrigacx.com/v2/transactions"
    payload = {'book': book,"time": time}
    r = requests.post(url,data=payload)
    values = r.json()
    
    return values
    
def get_account_balance():
    url = "https://api.quadrigacx.com/v2/balance"
    
    signature = sig.hash()
    
    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature']}
    r = requests.post(url, data=payload)
    values = r.json()

    return values

def get_user_transactions(offset=0, limit=50,sort="desc",book="btc_cad"):
    url = "https://api.quadrigacx.com/v2/user_transactions"
    
    signature = sig.hash()
    
    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
    'offset': offset, 'limit':limit,'sort': sort,'book':book }
    r = requests.post(url, data=payload)
    values = r.json()

    return values

def get_open_orders(book="btc_cad"):
    url = "https://api.quadrigacx.com/v2/open_orders"
    
    signature = sig.hash()
    
    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
    'book':book }
    r = requests.post(url, data=payload)
    values = r.json()

    return values

def get_open_order(id):
    url = "https://api.quadrigacx.com/v2/lookup_order"

    signature = sig.hash()
    
    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
    'id': id }
    r = requests.post(url, data=payload)
    values = r.json()

    return values

def cancel_order(id):
    url = "https://api.quadrigacx.com/v2/cancel_order"
    
    signature = sig.hash()
    
    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
    'id': id }
    r = requests.post(url, data=payload)
    values = r.json()

    return values
    

def limit_buy_order(amount,price,book):
    url = "https://api.quadrigacx.com/v2/buy"

    signature = sig.hash()

    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
    'amount': amount, 'price': price, 'book': book }
    r = requests.post(url, data=payload)
    values = r.json()

    return values

def market_buy_order(amount, book):
    url = "https://api.quadrigacx.com/v2/buy"
    
    signature = sig.hash()

    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
    'amount': amount, 'book': book }
    r = requests.post(url, data=payload)
    values = r.json()

    return values

def limit_sell_order(amount, price, book):
    url = "https://api.quadrigacx.com/v2/sell"
    
    signature = sig.hash()

    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
    'amount': amount, 'price': price, 'book': book }
    r = requests.post(url, data=payload)
    values = r.json()

    return values

def market_sell_order(amount, book):
    url = "https://api.quadrigacx.com/v2/sell"
    
    signature = sig.hash()

    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
    'amount': amount, 'book': book }
    r = requests.post(url, data=payload)
    values = r.json()

    return values
