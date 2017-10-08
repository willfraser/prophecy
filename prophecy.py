import polling
import split

upside = input("Enter the minimum upside percentage in decemail I.E. 1% is 0.01 :")
downside = input("Enter the minimum downside percentage in decemail I.E. 1% is 0.01 :")

#setup the split algorithim 
b = split.set_split()

f = b[0] #set f to fiat
c = b[1] #set c to crypto
k = b[2] #set k to kraken

print("Buy in USD if upside margin is greated than", upside)
print("Sell back to USD if downside margin is less than", downside)

#runs the selected algorithm continually at the specified "steps" or seconds
polling.poll(
lambda: split.run(upside, downside, 0.0044, f, c, k),
step=3,
poll_forever=True)
    

