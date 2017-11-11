import polling
import split
import kraken

confirm = "n"
upside = input("Enter the minimum upside percentage in decimal I.E. 1% is 0.01 :")
downside = input("Enter the minimum downside percentage in decimal I.E. .1% is 0.001 :")
trade_cost = input("Enter the commision price paid for both buy and sell. I.E. if it's 0.2% per trade then enter 0.004:")

while float(downside) < -.002 and confirm == "n":
    confirm = input("Are you sure you want downside to be", downside, "which is less than -.001")
    if str(confirm) == "y" or str(confirm) == "Y":
        print("confirmed")
    else:
        confirm = "n"
    
            
#setup the split algorithim 
b = split.set_split()

f = b[0] #set f to fiat
c = b[1] #set c to crypto
k = b[2] #set k to kraken

# split.multiCryptoSplit(0,0,0,f,c,k)

print("Buy in USD if upside margin is greated than", upside)
print("Sell back to USD if downside margin is less than", downside)

#runs the selected algorithm continually at the specified "steps" or seconds
polling.poll(
lambda: split.run(upside, downside, float(trade_cost), f, c, k),
step=5,
poll_forever=True)
    

