import urllib3.request
var price = urllib3.request.urlopen("https://api.quadrigacx.com/v2/ticker?book=eth_cad").read
print price 