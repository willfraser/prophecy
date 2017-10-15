import kraken
import exchange
import datetime
import kraken_api

#An object to represent any Fiat currency with the required meta-data
class Fiat:
    
    def __init__(self,currency):
        self.currency = currency
        self.exchange_USD = exchange.get_exchanged_value(1, "USD", currency)
        self.balance = 0
        self.ask_price = 0 
        self.ask_volume = 0.0 
        self.bid_price = 0.0
        self.bid_volume = 0
        self.upside_arbitrage = {}
        self.downside_arbitrage = {}
        self.fiats = []

class Crypto:
    
    def __init__(self,currency):
        self.currency = currency
        self.balance = 0
        self.ask_price = 0 
        self.ask_volume = 0.0 
        self.bid_price = 0.0
        self.bid_volume = 0
        self.trade_fee = 0.024
    
#Create curriences and get USD exchange rate
def set_split():
  
    CAD = Fiat("CAD")
    print("CAD_USD", CAD.exchange_USD)
    GBP = Fiat("GBP")
    print("GBP_USD", GBP.exchange_USD)
    EUR = Fiat("EUR")
    print("EUR_USD", EUR.exchange_USD)
    JPY = Fiat("JPY")
    print("EUR_USD", EUR.exchange_USD)
    USD = Fiat("USD")
    print("USD_USD", USD.exchange_USD)
    
    all_currencies = [USD, CAD, EUR, GBP, JPY]
    core_currencies = [USD, EUR]
    
    
    ETH = Crypto("ETH")
    ETH.fiats = all_currencies
    ETH.symbol = "XETHZ"
    print("ETH Initialized")
    
    XBT = Crypto("XBT")
    XBT.fiats = all_currencies
    XBT.symbol = "XXBTZ"
    print("XBT Initilaized")
    
    BCH = Crypto("BCH")
    BCH.fiats = core_currencies
    BCH.symbol = "BCH"
    print("BCH Initilaized")
    
    #ToDo this may cause problems due to being 4 characters long
    DASH = Crypto("DASH")
    DASH.fiats = core_currencies
    DASH.symbol = "DASH"
    print("DASH Initilaized")
    
    ETC = Crypto("ETC")
    ETC.fiats = core_currencies
    ETC.symbol = "XETCZ"
    print("ETC Initilaized")
    
    LTC = Crypto("LTC")
    LTC.fiats = core_currencies
    LTC.symbol = "XLTCZ"
    print("LTC Initilaized")

    REP = Crypto("REP")
    REP.fiats = core_currencies
    REP.symbol = "XREPZ"
    print("REP Initilaized")
    
    XMR = Crypto("XMR")
    XMR.fiats = core_currencies
    XMR.symbol = "XXMRZ"
    print("XMR Initilaized")
    
    XRP = Crypto("XRP")
    XRP.fiats = core_currencies
    XRP.symbol = "XXRPZ"
    print("XRP Initilaized")
    
    ZEC = Crypto("ZEC")
    ZEC.fiats = core_currencies
    ZEC.symbol = "XZECZ"
    print("ZEC Initilaized")
    
    my_cryptos = [ETH, XBT, BCH, ETC, LTC, XMR, XRP, ZEC]
    
    k = kraken_api.API()
    k.load_key('kraken.key')
    
    return [all_currencies,my_cryptos,k]

def update_exchange(currency):
    
    currency.exchange_USD = exchange.get_exchanged_value(1, "USD", currency.currency)
    
    return 1

#execute the currency split arbitrage algorithim
#ask = selling price (price at which you can buy the instrument)
#bid = buying price (price at which you can sell the instrument)
def run(target_up,target_down, trans_fee,currencies, cryptos, k):
    
    
    
    # for currency in currencies:
    #     update_exchange(currency)
    
    for crypto in cryptos:
    
        #get currency bids and asks for all currencies
        for currency in crypto.fiats:
            kraken.get_ask_bid(currency,crypto,k)
    
        #calculate USD arbitrage margin    
        for currency_1 in crypto.fiats:
            for currency_2 in crypto.fiats:
                #(price currency is being bought at) - (price USD is being sold at) / (price USD is being sold at)
                currency_1.upside_arbitrage[currency_2.currency] = ((float(currency_2.bid_price) - float(currency_1.ask_price))/float(currency_1.ask_price))-trans_fee
                
                #(price USD is being bought at) - (price currency is being sold at) / (price currency is being sold at)
                currency_1.downside_arbitrage[currency_2.currency] = ((float(currency_1.bid_price) - float(currency_2.ask_price))/float(currency_2.ask_price))-trans_fee 
        
        #begin trading evaluation and execution    
        print(datetime.datetime.now().time())    
        
        for currency_1 in crypto.fiats:
            for currency_2 in crypto.fiats:
                #if currency is USD ignore    
                if(currency_1.currency != currency_2.currency):
                    
                    #evaluates to see if gain is sufficent to go from USD to non-USD
                    if(float(currency_1.upside_arbitrage[currency_2.currency])>float(target_up)):
                        print("upside op found")
                        #determine if bids or asks are volume limiting and only trade the smallest of the two 
                        #so we don't get stuck with extra 
                        # print(currency_1.ask_volume, "units being asked for in", currency_1.currency)
                        # print(currency_2.bid_volume, "units being bid for in", currency_2.currency)
                        
                        if((float(currency_1.ask_volume) - float(currency_2.bid_volume)) < 0):
                            volume = currency_1.ask_volume
                        else:
                            volume = currency_2.bid_volume
                             
                        #triggers the buy action with a safety factor to again insure we don't get stuck with 
                        #extra currency
                        print("Buy", volume, "of", crypto.currency, "in", currency_1.currency, "and sell", currency_2.currency, "for a margin of", currency_1.upside_arbitrage[currency_2.currency])
                        kraken.buy_sell(volume, currency_1, currency_2, crypto.currency, 0.8,k)
                    else:
                        #no trades found that meet our criteria
                        print("Hold", crypto.currency, currency_1.currency, "through", currency_2.currency, "upside margin is:", currency_1.upside_arbitrage[currency_2.currency])
                    
                    #evaluates if losses are small enough to bring fiat back from non-USD to USD
                    if(currency_2.currency == "CAD"):
                        if(float(currency_1.downside_arbitrage[currency_2.currency])>(float(target_down))):
                            print("downside op found")
                            if(currency_1.bid_volume < currency_2.ask_volume):
                                volume = currency_1.bid_volume
                            else:
                                volume = currency_2.ask_volume
                            
                            #triggers the buy action with a safety factor to again insure we don't get stuck with 
                            #extra currency
                            print("Buy", volume, "of", crypto.currency, "in", currency_2.currency, "and sell", currency_1.currency, "for a margin of", currency_1.downside_arbitrage[currency_2.currency])
                            kraken.buy_sell(volume,currency_2, currency_1, crypto.currency,0.8,k)
                        
                        else:
                        #     #no trades found that meet our criteria
                            print("Hold", crypto.currency, currency_1.currency, "downside margin is:",currency_1.downside_arbitrage[currency_2.currency])
            
    return
