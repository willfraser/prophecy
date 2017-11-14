import polling
import split
import kraken
import logging

logger = logging.getLogger('prophecy')
hdlr = logging.FileHandler('/prophecy.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


logger.info('Prophecy Start')

confirm = "n"
upside = input("Enter the minimum upside percentage in decimal I.E. 1% is 0.01:")
downside = input("Enter the minimum downside percentage in decimal I.E. .1% is 0.001 :")
trade_cost = input("Enter the commision price paid for both buy and sell. I.E. if it's 0.2% per trade then enter 0.004:")
            
#setup the split algorithim 
b = split.set_split()

f = b[0] #set f to fiat
c = b[1] #set c to crypto
k = b[2] #set k to kraken

# split.multiCryptoSplit(0,0,0,f,c,k)

print("Buy in USD if upside margin is greated than", upside)
logger.info("Upside Margin set to %s", upside)
print("Sell back to USD if downside margin is less than", downside)
logger.info("Downside Margin set to %s", downside)
print("Trading costs set at", downside)
logger.info("Trading cost set to %s", trade_cost)

#runs the selected algorithm continually at the specified "steps" or seconds
polling.poll(
lambda: split.run(upside, downside, float(trade_cost), f, c, k),
step=5,
poll_forever=True)
    

