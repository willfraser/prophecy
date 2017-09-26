import quadrigacx
import bittrex
import china_volatility
import polling
import time
import datetime
from pprint import pprint
import kraken

import json

global orderID
orderID = 1

def buy_low(book, low_price):
    global orderID
    
    print("Time is ", datetime.datetime.now().time())
    
    current_price = float(quadrigacx.get_current_trades(book)['last'])
    print('current price $', current_price)
    
    quadrigacx.cancel_order(orderID)
    time.sleep(1)
    coin_available = quadrigacx.get_account_balance()['cad_available']
    print('Coin Available ', coin_available)
    
    if current_price < low_price:
        time.sleep(1)
        orderID = quadrigacx.limitt_buy_order(coin_available, current_price, book)['id']
        print("Lower Limt Hit. Buy Order - ",orderID)
    
    print()
        
    return
    

def stop_loss(book, low_price):
    global orderID
  
    print("Time is ", datetime.datetime.now().time())  
    
    current_price = float(quadrigacx.get_current_trades(book)['last'])
    print('current price $', current_price)
    
    quadrigacx.cancel_order(orderID)
    time.sleep(1)
    coin_available = quadrigacx.get_account_balance()['eth_available']
    print('Coin Available ', coin_available)
    
    if current_price < low_price:
        time.sleep(1)
        order = quadrigacx.limitt_sell_order(coin_available, current_price, book)
        print("Stop loss active")

    return


def margin_hunter(book, margin):
    global orderID
  
    print("Time is ", datetime.datetime.now().time())  
    
    current_price = float(quadrigacx.get_current_trades(book)['last'])
    print('current price $', current_price)
    
    quadrigacx.cancel_order(orderID)
    time.sleep(1)
    coin_available = quadrigacx.get_account_balance()['ltc_available']
    print('Coin Available ', coin_available)
    
    if current_price < low_price:
        time.sleep(1)
        orderID = quadrigacx.limitt_sell_order(coin_available, current_price, book)['id']
        print("Lower Limt Hit")
        
    if current_price > high_price:
        time.sleep(1)
        orderID = quadrigacx.limit_sell_order(coin_available,current_price,book)
        print("Upper Limit Hit")
        
    return

def buy_sell_at(book, target_buy_price, target_sell_price):
    global orderID
  
    print("Time is ", datetime.datetime.now().time()) 
    #bittrex.get_current_trades(book)
    
    current_price = float(quadrigacx.get_current_trades(book)['last'])
    print('current price $', current_price)
    
    quadrigacx.cancel_order(orderID)
    time.sleep(1)
    
    
    if current_price < target_buy_price:
        coin_available = quadrigacx.get_account_balance()['cad_available']
        print('Coin Available ', coin_available)
        
        if float(coin_available) > 0.0:
            coins = float(coin_available) / float(current_price)
            order = quadrigacx.limit_buy_order(coins, current_price, book)
            pprint(order)
            print("Lower Limt Hit")
    else:
        print("Current price above target buy")
        
    if current_price > target_sell_price:
        coin_available = quadrigacx.get_account_balance()['eth_available']
        print('Coin Available ', coin_available)
        
        if float(coin_available) > 0.0:
            coins = float(coin_available)
            order = quadrigacx.limit_sell_order(coins, current_price, book)
            pprint(order)  
            print("Upper Limit Hit")
    else:
        print("Current price below target sell")
        
       
    return

v = china_volatility.set_volatility(341050, 341050, .03)
china_volatility.get_volatility(v)

polling.poll(
lambda: kraken.get_current_book('ETHUSD'):,
step=900,
poll_forever=True)


    

