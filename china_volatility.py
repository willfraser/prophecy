import bithumb
import json
import quadrigacx

class Volatility:
    
    def __init__(self):
        self.local_max = 0
        self.local_min = 0
        self.state = "unknown"
    
def set_volatility(max, min, percent_movement):
    
    v = Volatility()
    v.local_max = float(max)
    v.local_min = float(min)
    v.tolerance = percent_movement
    v.last_price = 0
    v.mode = "detect"
    return v
        
def get_volatility(volatility):
    
    #Get latest closing price from the bithumb exchange
    ticker = float(bithumb.get_ticker("ETH"))
    target = 0 
    
    #update min and max        
    if ticker > volatility.local_max:
        volatility.local_max = ticker
        
        
    if ticker < volatility.local_min:
        volatility.local_min = ticker
        
    
    if volatility.mode == "buy":
        #looking to buy
        target = volatility.local_min*(1+volatility.tolerance)
        if (target)<ticker:
                print("BUY", target)
                quadrigacx.market_buy_all("eth_cad")
                volatility.mode = "sell"
                volatility.local_max = ticker
                volatility.local_min = ticker
    
    elif volatility.mode == "sell":
        #looking to sell
        target = volatility.local_max*(1-volatility.tolerance)
        if ticker < (target):
            print("SELL", target)
            quadrigacx.market_sell_all("eth_cad")
            volatility.mode = "buy"
            volatility.local_min = ticker
            volatility.local_max = ticker
    else:
        #detect logic 
        print("Detecting mode...")
        print("Cad Available ", quadrigacx.get_account_balance("cad_available"))
        if float(quadrigacx.get_account_balance("cad_available")) > 0:
            volatility.mode = "buy"
            print(volatility.mode, " mode selected")
        else:
            volatility.mode = "sell"
            print(volatility.mode, " mode selected")

    print("Last Price", volatility.last_price, "Closing Price ", ticker, "Local Max", volatility.local_max, "Local Min", 
    volatility.local_min, "mode", volatility.mode, "tolerance", volatility.tolerance, "target", target)
    
    volatility.last_price = ticker
    
    return