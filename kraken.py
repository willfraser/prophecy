from pprint import pprint
import time 
import requests
import json


#get the 1st bid and 1st ask of any specified currency
def get_ask_bid(fiat_currency,crypto_currency,k):
    
    values = {}
    
    if(crypto_currency.symbol != "BCH" and crypto_currency.symbol!="DASH"):
        pair=crypto_currency.symbol+fiat_currency.symbol

    else:
        pair=crypto_currency.symbol+fiat_currency.symbol[1:4]
    
    while True:

        try:
            values = k.query_public('Depth',
                                {'pair': pair
                                })
        
        except requests.HTTPError as e:
            status_code = e.response.status_code
            
            time.sleep(0.5)
            if(int(status_code)>=500):
                get_ask_bid(fiat_currency, crypto_currency, k)
                                
        except requests.Timeout:
            time.sleep(0.5)
            get_ask_bid(fiat_currency, crypto_currency, k)
        
        try:
            if "result" in values:
                if pair in values["result"]:
                    if "bids" in values["result"][pair]:
                        if "asks" in values["result"][pair]:
                            if len(values["result"][pair]["bids"])>0:
                                break
        except:
            get_ask_bid(fiat_currency,crypto_currency,k)
            
        time.sleep(.1)
                                
    fiat_currency.ask_price = values["result"][pair]["asks"][0].pop(0)
    fiat_currency.ask_price = float(fiat_currency.ask_price) * float(fiat_currency.exchange_USD)
    fiat_currency.ask_volume = values["result"][pair]["asks"][0].pop(0)
    
    fiat_currency.bid_price = values["result"][pair]["bids"][0].pop(0)
    fiat_currency.bid_price = float(fiat_currency.bid_price) * float(fiat_currency.exchange_USD)
    fiat_currency.bid_volume = values["result"][pair]["bids"][0].pop(0)
    
    return fiat_currency

def buy_sell(amount, buy_currency, sell_currency, transfer_currency,saftey_margin,k):
    
    minimum_order = float(transfer_currency.min_order)
    
    #safety adjust trade volume
    amount = float(amount) * float(saftey_margin)
    
    if(amount>1000):
        amount = 1000
    
    #setup pairs
    if(transfer_currency.symbol != "BCH" and transfer_currency.symbol!="DASH"):
        buy_pair = transfer_currency.symbol+buy_currency.symbol
        sell_pair = transfer_currency.symbol+sell_currency.symbol
    else:
        buy_pair = transfer_currency.symbol+buy_currency.symbol[1:4]
        sell_pair = transfer_currency.symbol+sell_currency.symbol[1:4]
    
    if(amount < minimum_order):
        print("less than min order")
        return 0
    else:
        #buy at market price
        if(buy_market(amount, buy_pair, buy_currency, transfer_currency, k)):
            #sell all currency
            sell_all_market(transfer_currency, sell_pair, k )
                    
        return 1
        
def buy_market(amount, pair, buy_fiat, crypto, k):
    
    if((float(crypto.ask_price)*float(amount))>800.0):
        amount=800.0/float(crypto.ask_price)
        print("Amount over limit. Reducing to 800")
    
    print("Placing buy order for", amount, "of", pair)
    
    fiat = buy_fiat.symbol
    
    fiat_balance = float(get_fiat_balance(fiat,k))
    
    print(fiat, "balance of", fiat_balance)
    
    total_purchase_price = float(crypto.ask_price)*float(amount)
    
    if(fiat_balance>10):
    
        if(fiat_balance>total_purchase_price):
            print("purchase total")
            #make buy
            
            market_buy(buy_fiat.symbol, crypto.symbol, amount,k)
            
        else:
            amount = round(0.8*(float(fiat_balance)/float(crypto.ask_price)),4)
            print("purchase reduced total")
            
            #make buy
            market_buy(buy_fiat.symbol, crypto.symbol, amount,k)
        
        while is_balance(k):
            time.sleep(.1)
            
           
        print("Buy order for", amount, "of", pair, "filled successfully")
        
        return 1
    
    else:
        # print("Insufficent funds")
        
        return 0
    
def sell_all_market(crypto, pair, k):
    
    print("preparing to sell all market")
    while(get_balance(crypto, k)):
    
        amount = get_balance(crypto, k)
        
        if(amount>0):
            print("Placing sell order for", amount, "of", pair)
            
            #make sell
            market_sell(pair, amount,k)
            
            time.sleep(.5)
  
        else:
            print("Nothing to Sell")
    
    print("Sell order for of", pair, "filled successfully")
    return 1
    
def market_sell(pair, amount,k):
    try:
        pprint(k.query_private('AddOrder',
                        {'pair': pair,
                         'type': 'sell',
                         'ordertype': 'market',
                         'volume': amount,
                        }))
                        
    except requests.HTTPError as e:
        print('market sell http error')
        status_code = e.response.status_code
        if(int(status_code)>=500):
            time.sleep(.5)
            market_sell(pair, amount,k)
                
    except requests.Timeout:
        time.sleep(.5)
        market_sell(pair, amount,k)
        
def market_buy(fiat_symbol, crypto_symbol, amount,k):
    
    pair = crypto_symbol+fiat_symbol
    
    print("market buy", amount)
    
    amount = round(amount,4)
    
    if is_balance(k):
        print("order outstanding")
    else:
        try:
            pprint(k.query_private('AddOrder',
                                {'pair': pair,
                                 'type': 'buy',
                                 'ordertype': 'market',
                                 'volume': amount,
                                }))
                            
        except requests.HTTPError as e:
            print('market buy http error')
            status_code = e.response.status_code
                    
            if(int(status_code)>=500):
                if is_balance(k):
                    print("order outstanding")
                else:
                    time.sleep(.5)
                    market_buy(fiat_symbol, crypto_symbol, amount,k)
                        
        except requests.Timeout:
            if is_balance(k):
                    print("order outstanding")
            else:
                time.sleep(.5)
                market_buy(fiat_symbol, crypto_symbol, amount,k)
        
def get_balance(crypto, k):
    
    
    try:
        amt = k.query_private('Balance')
        
        
    except requests.HTTPError as e:
        status_code = e.response.status_code
                
        if(int(status_code)>=500):
            time.sleep(.5)
            amt = get_balance(crypto, k)
                
    except requests.Timeout:
        time.sleep(.5)
        amt = get_balance(crypto, k)    
    
    try:
        if 'result' in amt:
            amount = amt['result']
            if crypto.symbol in amount:
                print(amount)
                amount = float(amount[crypto.symbol])
            else:
                time.sleep(0.2)
                get_balance(crypto,k)
        else:
                time.sleep(0.2)
                get_balance(crypto,k)
    except:
        get_balance(crypto, k)
      
    return amount
    
def is_balance(k):
        
    while True:
        print('is balance')
        
        try: 
            openOrders = k.query_private('OpenOrders')
            
        except KeyError:
            is_balance(k)
        
        except requests.HTTPError as e:
            status_code = e.response.status_code
                    
            if(int(status_code)>=500):
                time.sleep(.5)
                return(is_balance(k))
                    
        except requests.Timeout:
            time.sleep(.5)
            return(is_balance(k))
        
        try:
            if 'result' in openOrders:
                if 'open' in openOrders['result']:
                    break 
        
        except:
            is_balance(k)
            
        time.sleep(.1)
        
    return(openOrders['result']['open'])

def get_fiat_balance(fiat,k):
    
    while True:
        # print('get fiat balance')
        try:
            balance = k.query_private('Balance')
            print(balance)
        
        except KeyError:
            break
        
        except requests.HTTPError as e:
            status_code = e.response.status_code
                    
            if(int(status_code)>=500):
                time.sleep(.5)
                balance = get_fiat_balance(fiat,k)
                    
        except requests.Timeout:
            time.sleep(.5)
            balance = get_fiat_balance(fiat,k)
        
        if balance != 0:
            try:
                if 'result' in balance:
                    if fiat in balance['result']:
                        balance = balance['result'][fiat]
                        break
                    else:
                        balance = 0
                        break
            except:
                get_fiat_balance(fiat,k)
        
        time.sleep(.1)
    
    return balance
    
def is_open_order(k):
    
    while True:    
        print('is open order')
        try:
            open = k.query_private('OpenOrders')
            
        except KeyError:
              open = 0
            
        except requests.HTTPError as e:
            status_code = e.response.status_code
                        
            if(int(status_code)>=500):
                time.sleep(.5)
                open = is_open_order(k)
                        
        except requests.Timeout:
            time.sleep(.5)
            open = is_open_order(k)
        
        try:
            if 'result'in open:
                open = open['result']['open']
                break
        except:
            is_open_order(k)
            
        time.sleep(.1)
            
    return open
    
    
def get_all_pairs(k):
    
    try:
        values = k.query_public('AssetPairs')
        
        return values
        
    except requests.HTTPError as e:
        status_code = e.response.status_code
                    
        if(int(status_code)>=500):
            time.sleep(.5)
            pairs = get_all_pairs(k)
                    
    except requests.Timeout:
        time.sleep(.5)
        pairs = get_all_pairs(k)
    