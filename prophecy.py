import polling
import split

confirm = "n"
upside = input("Enter the minimum upside percentage in decemail I.E. 1% is 0.01 :")
downside = input("Enter the minimum downside percentage in decemail I.E. 1% is 0.01 :")

while float(downside) < -.001 and confirm == "n":
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

print("Buy in USD if upside margin is greated than", upside)
print("Sell back to USD if downside margin is less than", downside)

split.auto_split(k)

#runs the selected algorithm continually at the specified "steps" or seconds
polling.poll(
lambda: split.run(upside, downside, 0.004, f, c, k),
step=5,
poll_forever=True)
    

