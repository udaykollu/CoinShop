#!C:\Python27\python.exe
import os
import hashlib
import hmac
import urllib2
import time
import json
import cgi
#This code sample demonstrates a GET and a POST call to the Coinbase API
#Before implementation, set environmental variables with the names API_KEY and API_SECRET.

def make_request(url, body=None):
  opener = urllib2.build_opener()
  nonce = int(time.time() * 1e6)
  message = str(nonce) + url + ('' if body is None else body)
  signature = hmac.new("Hvr8G5Qb2fWA6DA63yELBWa38oMEgyAu", message, hashlib.sha256).hexdigest()


  headers = {'ACCESS_KEY' : "d1oSqbnz9vRcsdW2",
             'ACCESS_SIGNATURE': signature,
             'ACCESS_NONCE': nonce,
             'Accept': 'application/json'}

  # If we are passing data, a POST request is made. Note that content_type is specified as json.
  if body:
    headers.update({'Content-Type': 'application/json'})
    req = urllib2.Request(url, data=body, headers=headers)

  # If body is nil, a GET request is made.
  else:
    req = urllib2.Request(url, headers=headers)

  try:
    return opener.open(req)
  except urllib2.HTTPError as e:
    print e
    return e

print "Content-type: text/html"
print 
fields=cgi.FieldStorage()
buy= fields.getvalue("buy")

qty=float(fields.getvalue("qty"))
# Example of a GET request, where body is nil.
if (buy == "x") :
    print make_request('https://api.coinbase.com/v1/buys',json.dumps({"qty":qty}))
else :
    print make_request('https://api.coinbase.com/v1/sells',json.dumps({"qty":qty}))