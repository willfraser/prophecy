from pprint import pprint
import time 

#get the 1st bid and 1st ask of any specified currency
def get_ask_bid(fiat_currency,crypto_currency,k):
    pair="X"+crypto_currency+"Z"+fiat_currency.currency
    
    values = k.query_public('Depth',
                        {'pair': pair
                        })
    
    while(len(values["result"][pair]["bids"])<0):
        values = k.query_public('Depth',
                        {'pair': pair
                        })
  
        while(len(values["result"][pair]["asks"])<0):
            values = k.query_public('Depth',
                        {'pair': pair
                        })
            
    fiat_currency.ask_price = values["result"][pair]["asks"][0].pop(0)
    fiat_currency.ask_price = float(fiat_currency.ask_price) * float(fiat_currency.exchange_USD)
    fiat_currency.ask_volume = values["result"][pair]["asks"][0].pop(0)
    
    fiat_currency.bid_price = values["result"][pair]["bids"][0].pop(0)
    fiat_currency.bid_price = float(fiat_currency.bid_price) * float(fiat_currency.exchange_USD)
    fiat_currency.bid_volume = values["result"][pair]["bids"][0].pop(0)
    
    return fiat_currency

# def get_book(book, count):
    
#     url = 'https://api.kraken.com/0/public/Depth'
#     pair="XETHZ"+book
#     payload = {'pair': pair, 'count': count}
    
#     r = requests.get(url,params=payload)
#     values =r.json()
    
#     while(len(values["result"][pair]["bids"])<0):
#         r = requests.get(url,params=payload)
#         values =r.json()
  
#         while(len(values["result"][pair]["asks"])<0):
#             r = requests.get(url,params=payload)
#             values =r.json()
    
#     return values
    
# def get_all_current_books(base, count,currency_book):
    
#     currencies = ["USD","CAD"]
    
#     url = 'https://api.kraken.com/0/public/Depth'
#     for currency in currencies:
#         pair="X"+currency+"Z"+currency
#         payload = {'pair': pair, 'count': count}
#         r = requests.get(url,params=payload)
#         #print(r.status_code)
        
#         while(r==0):
#             r = requests.get(url,params=payload)
            
#         values = r.json()
#         #pprint(values)
        
#         #print("Get book for", pair)
#         #pprint(values)
#         #print("Currency:", currency)
        
#         #pprint(values["result"][pair]["bids"])
        
#         if(len(values["result"][pair]["bids"])>0):
#             if(currency!="USD"):
#                 #print('Bid length is', len(values["result"][pair]["bids"]))
#                 currency_book.currency = exchange.get_exchanged_value(values["result"][pair]["bids"][0].pop(0), "USD", currency)
#                 margin = (float(currency_book.currency)-float(currency_book.USD))/float(currency_book.USD)
#                 if(margin > 0.0152):
#                     print("buy", values["result"][pair]["bids"][0].pop(0), "CAD", "with margin", margin)
#                 else:
#                     print("hold")
                    
#                 #print("Ask in USD", currency_book.currency)
#                 #print("Percentage split from USD", ((float(currency_book.currency)-float(currency_book.USD))/float(currency_book.USD)))
#             elif(len(values["result"][pair]["asks"])>0) :
#                 #print('Ask length is', len(values["result"][pair]["asks"]))
#                 currency_book.USD = values["result"][pair]["asks"][0].pop(0)
#                 if(currency_book.CAD>0):
#                     margin = (float(currency_book.USD)-float(currency_book.CAD))/float(currency_book.CAD)
#                     if(margin > 0.0152):
#                         print("buy", values["result"][pair]["bids"][0].pop(0), "USD", "with margin", margin)
#                     else:
#                         print("hold")
          
            
#     return currency_book


def buy_sell(amount, buy_currency, sell_currency, transfer_currency,saftey_margin,k):
    
    minimum_order = 0.01

    #safety adjust trade volume
    amount = float(amount) * float(saftey_margin)
    
    #setup pairs 
    buy_pair = "X"+transfer_currency+"Z"+buy_currency.currency
    sell_pair = "X"+transfer_currency+"Z"+sell_currency.currency
    
    if(amount < minimum_order):
        return 0
    else:
        #buy at market price
        if(buy_market(amount, buy_pair, buy_currency, k)):
            #sell all currency
            sell_all_market(sell_pair, k )
                    
        return 1
        
def buy_market(amount, pair, currency, k):
    
    print("Placing buy order for", amount, "of", pair)
    
    if((float(currency.ask_price)*float(amount))>800.0):
        amount=800.0/float(currency.ask_price)
    
    fiat = pair[4:8]

    try:
        fiat_balance = float(k.query_private('Balance')['result'][fiat])
    except KeyError:
        fiat_balance = float(0)
    
    total_purchase_price = float(currency.ask_price)*float(amount)
    
    if(fiat_balance>10):
    
        if(fiat_balance>total_purchase_price):
            print("purchase total")
            #make buy
            pprint(k.query_private('AddOrder',
                        {'pair': pair,
                         'type': 'buy',
                         'ordertype': 'market',
                         'volume': amount,
                        }))
            
        else:
            amount = round(float(fiat_balance)/float(currency.ask_price),4)
            
            #make buy
            pprint(k.query_private('AddOrder',
                        {'pair': pair,
                         'type': 'buy',
                         'ordertype': 'market',
                         'volume': amount,
                        }))
        
        while k.query_private('OpenOrders')['result']['open']:
                time.sleep(.1)
           
        print("Buy order for", amount, "of", pair, "filled successfully")
        
        return 1
    
    else:
        # print("Insufficent funds")
        
        return 0
    
    
    
def sell_all_market(pair, k):
    
    crypto = pair[0:4]
    
    amount = float(k.query_private('Balance')['result'][crypto])
    
    if(amount>0):
        print("Placing sell order for", amount, "of", pair)
        
        #make sell
        pprint(k.query_private('AddOrder',
                    {'pair': pair,
                     'type': 'sell',
                     'ordertype': 'market',
                     'volume': amount,
                    }))
    
        while k.query_private('OpenOrders')['result']['open']:
            time.sleep(.1)
        
        print("Sell order for", amount, "of", pair, "filled successfully")
    else:
        print("Nothing to Sell")
    
    return 1
