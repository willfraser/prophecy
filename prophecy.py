import polling
import split
import kraken
import kraken_api

#setup the split algorithim 
b = split.set_split()

f = b[0] #set f to fiat
c = b[1] #set c to crypto
k = b[2] #set k to kraken

#runs the selected algorithm continually at the specified "steps" or seconds
polling.poll(
lambda: split.run(0.018, 0.0122, 0.0044, f, c, k),
step=5,
poll_forever=True)
    

