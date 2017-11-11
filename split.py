import kraken
import exchange
import datetime
import kraken_api

#An object to represent any Fiat currency with the required meta-data
class Fiat:
    
    def __init__(self,currency,symbol):
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
        self.symbol = symbol

class Crypto:
    
    def __init__(self,currency):
        self.currency = currency
        self.balance = 0
        self.ask_price = 0 
        self.ask_volume = 0.0 
        self.bid_price = 0.0
        self.bid_volume = 0
        self.trade_fee = 0.02
        self.symbol = ""
        
class Trade_Pair:
    
    def __init__(self,pair, pair_decimals,base, quote, fee_volume_currency):
        self.pair = pair
        self.pair_decimals = pair_decimals
        self.base = base
        self.quote = quote
        self.fee_volume_currency = fee_volume_currency
    
#Create curriences and get USD exchange rate
def set_split():
  
    CAD = Fiat("CAD","ZCAD")
    print("CAD_USD", CAD.exchange_USD)
    GBP = Fiat("GBP","ZGBP")
    print("GBP_USD", GBP.exchange_USD)
    EUR = Fiat("EUR","ZEUR")
    print("EUR_USD", EUR.exchange_USD)
    JPY = Fiat("JPY","ZJPY")
    print("EUR_USD", EUR.exchange_USD)
    USD = Fiat("USD","ZUSD")
    print("USD_USD", USD.exchange_USD)
    
    all_currencies = {"USD":USD, "CAD":CAD, "EUR":EUR, "GBP":GBP, "JPY":JPY}
    core_currencies = {"USD":USD, "EUR":EUR}
    
    
    ETH = Crypto("ETH")
    ETH.fiats = all_currencies
    ETH.crypto_pairs = ["EOS"]
    ETH.symbol = "XETH"
    ETH.min_order = 0.02
    print("ETH Initialized")
    
    XBT = Crypto("XBT")
    XBT.fiats = all_currencies
    XBT.symbol = "XXBT"
    XBT.min_order = 0.002
    print("XBT Initilaized")
    
    BCH = Crypto("BCH")
    BCH.fiats = core_currencies
    BCH.symbol = "BCH"
    BCH.min_order = 0.002
    print("BCH Initilaized")
    
    #ToDo this may cause problems due to being 4 characters long
    DASH = Crypto("DASH")
    DASH.fiats = core_currencies
    DASH.symbol = "DASH"
    DASH.min_order = 0.03
    print("DASH Initilaized")
    
    ETC = Crypto("ETC")
    ETC.fiats = core_currencies
    ETC.symbol = "XETC"
    ETC.min_order = 0.3
    print("ETC Initilaized")
    
    LTC = Crypto("LTC")
    LTC.fiats = core_currencies
    LTC.symbol = "XLTC"
    LTC.min_order = 0.1
    print("LTC Initilaized")

    REP = Crypto("REP")
    REP.fiats = core_currencies
    REP.symbol = "XREP"
    REP.min_order = 0.3
    print("REP Initilaized")
    
    XMR = Crypto("XMR")
    XMR.fiats = core_currencies
    XMR.symbol = "XXMR"
    XMR.min_order = 0.1
    print("XMR Initilaized")
    
    XRP = Crypto("XRP")
    XRP.fiats = core_currencies
    XRP.symbol = "XXRP"
    XRP.min_order = 30
    print("XRP Initilaized")
    
    ZEC = Crypto("ZEC")
    ZEC.fiats = core_currencies
    ZEC.symbol = "XZEC"
    ZEC.min_order = 0.03
    print("ZEC Initilaized")
    
    my_cryptos = {"ETH":ETH, "XBT":XBT, "ETC": ETC, "LTC":LTC, "XMR":XMR, "XRP":XRP, "ZEC":ZEC, "BCH":BCH}
    
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
    
    now = datetime.time
    if now.hour == 12:
        if now.minute >0 and if now.minute <5: 
            for currency in currencies:
                update_exchange(currency)
    
    for crypto_key, crypto in cryptos.items():
    
        #get currency bids and asks for all currencies
        for currency_key, currency in crypto.fiats.items():
            kraken.get_ask_bid(currency,crypto,k)
    
        #calculate USD arbitrage margin    
        for currency_1_key, currency_1 in crypto.fiats.items():
            for currency_2_key, currency_2 in crypto.fiats.items():
                #(price currency is being bought at) - (price USD is being sold at) / (price USD is being sold at)
                currency_1.upside_arbitrage[currency_2.currency] = ((float(currency_2.bid_price) - float(currency_1.ask_price))/float(currency_1.ask_price))-trans_fee
                
                #(price USD is being bought at) - (price currency is being sold at) / (price currency is being sold at)
                currency_1.downside_arbitrage[currency_2.currency] = ((float(currency_1.bid_price) - float(currency_2.ask_price))/float(currency_2.ask_price))-trans_fee 
        
        #begin trading evaluation and execution    
        print(datetime.datetime.now().time())    
        
        for currency_1_key, currency_1 in crypto.fiats.items():
            for currency_2_key, currency_2 in crypto.fiats.items():
                #if currency is USD ignore    
                if(currency_1.currency != currency_2.currency):
                    
                    #evaluates to see if gain is sufficent to go from USD to non-USD
                    if(float(currency_1.upside_arbitrage[currency_2.currency])>float(target_up)):
                        print("upside op found")
                        #determine if bids or asks are volume limiting and only trade the smallest of the two 
                        #so we don't get stuck with extra 
                        
                        if((float(currency_1.ask_volume) - float(currency_2.bid_volume)) < 0):
                            volume = currency_1.ask_volume
                        else:
                            volume = currency_2.bid_volume
                             
                        #triggers the buy action with a safety factor to again insure we don't get stuck with 
                        #extra currency
                        print("Buy", volume, "of", crypto.currency, "in", currency_1.currency, "and sell", currency_2.currency, "for a margin of", currency_1.upside_arbitrage[currency_2.currency])
                        kraken.buy_sell(volume, currency_1, currency_2, crypto, 0.8,k)
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
                            kraken.buy_sell(volume,currency_2, currency_1, crypto,0.8,k)
                        else:
                        #no trades found that meet our criteria
                            print("Hold", crypto.currency, currency_1.currency, "downside margin is:",currency_1.downside_arbitrage[currency_2.currency])
            
    # multiCryptoSplit(target_up, target_down, trans_fee, currencies, cryptos, k)
    
    return

def multiCryptoSplit(target_up, target_down, trans_fee, currencies, cryptos, k):
    
    #quote is unit currency is priced in i.e. quote of XXBT means currency is priced in Bitcoin
    #base is first currency in pair i.e. base of XETH means pair would be XETHXXBT
    
    print("starting crypto split test")
    
    #ask is price you can buy at
    #bid is price you can sell at
    XBT_buy = float(kraken.get_ask_bid(currencies["USD"],cryptos["XBT"],k ).ask_price)
    ETH_sell = float(kraken.get_ask_bid(currencies["USD"],cryptos["ETH"],k ).bid_price)
    
    values = k.query_public('Depth',
                    {'pair': "XETHXXBT"
                        })
                        
    ETH_buy = values["result"]["XETHXXBT"]["asks"][0].pop(0)
    print("eth buy", ETH_buy)
    # print("bidding pricing", values["result"]["XETHXXBT"]["bids"][0])
    
    print("ETH per USD via arbitrge is", XBT_buy*float(ETH_buy))
    
    print("ETH per USD", ETH_sell)
   
    print("USD->XBT->ETH->USD arbitrage is", ( (ETH_sell-(XBT_buy*float(ETH_buy))) / (XBT_buy*float(ETH_buy))))  
    
    
    # print(kraken.get_ask_bid(cryptos["XBT"],cryptos["ETH"],k ))
    
    
    # for crypto in cryptos:
    #     if crypto.currency == "ETH":
            
            # print(crypto.ask_price)
    
    
    
    
    
    # for crypto_1 in cryptos:
        
    #     kraken.get_ask_bid(currencies[0],crypto_1,k)
    #     print(crypto_1.symbol, "Selling at", crypto_1.fiats[0].ask_price)
            
    #     for crypto_2 in cryptos:
                
    #         #get currency bids and asks for all currencies
    #         kraken.get_ask_bid(currencies[0],crypto_2,k)
                
    #         if crypto_1 != crypto_2:
                
                
    #             print(crypto_2.symbol, "Buying at", crypto_2.fiats[0].bid_price)
                    
    #             split = ((crypto_1.fiats[0].ask_price - crypto_2.fiats[0].bid_price)/crypto_1.fiats[0].ask_price) - (trans_fee * 3)
    
    #             print("percentage split between", crypto_1.symbol, "and", crypto_2.symbol, "is", split)
    
                
        
    # ETH_XBT_Split = ((cryptos["ETH"].ask_price - cryptos.XBT.bid_price)/cryptos.ETH.ask_price)-(trans_fee*3)
    # print("ETH to XBT split is", ETH_XBT_Split)
    
    # XBT_ETH_Split = ((cryptos.XBT.ask_price - cryptos.ETH.bid_price)/cryptos.XBT.ask_price)-(trans_fee*3)
    # print("XBT to ETH split is", XBT_ETH_Split)
    
    return