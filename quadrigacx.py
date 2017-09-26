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
    
def get_account_balance(currency):
    url = "https://api.quadrigacx.com/v2/balance"
    
    time.sleep(1)
    signature = sig.hash()
    
    payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature']}
    r = requests.post(url, data=payload)
    values = r.json()
    
    return values[currency]

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

def market_buy_order(cad, book):
    url = "https://api.quadrigacx.com/v2/buy"
    cad = float(cad)
    print("Buy order")
    
    while cad > 100:
        time.sleep(1)
        ticker = float(get_current_trades("eth_cad")["ask"])
        print("ask",ticker)
        
        amount = (round(((cad/ticker)*.98),8))
        print("amount of eth", amount)
        signature = sig.hash()
        payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
        'amount': amount, 'book': book }
        r = requests.post(url, data=payload)
        values = r.json()
        print("Buy order placed")
        time.sleep(1)
        cad = float(get_account_balance("cad_available"))
        print("cad remaining",cad)
   
    
def market_buy_all(book):
    url = "https://api.quadrigacx.com/v2/buy"
    cad = float(get_account_balance("cad_available"))

    market_buy_order(cad,book)
      
    print("all bought") 
    return

def limit_sell_order(amount, price, book):
    url = "https://api.quadrigacx.com/v2/sell"
    
    time.sleep(1)
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
    
def market_sell_all(book):
    url = "https://api.quadrigacx.com/v2/sell"
    time.sleep(1)
    signature = sig.hash()
    
    eth = get_account_balance('eth_available')
    amount = float(eth)
    
    if amount>0:
        signature = sig.hash()
        payload = {'key': signature['key'], 'nonce': signature['nonce'], 'signature': signature['signature'], 
        'amount': amount, 'book': book }
        r = requests.post(url, data=payload)
        values = r.json()
        print("Sell all order placed")
        return values
    return