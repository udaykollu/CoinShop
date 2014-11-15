#!C:\Python27\python.exe
import cgi
import blpapi
import json

def getExchangeName(code):
	if code == "CNBS":
		return "CoinBase"
	elif code == "BTSP":
		return "BitStamp"
	elif code == "ITBT":
		return "itBit"
	elif code == "KRKN":
		return "Kraken"


		
sessionOptions = blpapi.SessionOptions()
sessionOptions.setServerHost("10.8.8.1")
sessionOptions.setServerPort(8194)
session = blpapi.Session(sessionOptions)
session.start()
session.openService("//blp/refdata")
refDataService = session.getService("//blp/refdata")
# Create and fill the request for the historical data
request = refDataService.createRequest("ReferenceDataRequest")
request.getElement("securities").appendValue("XBT BTSP Curncy")
request.getElement("securities").appendValue("XBT CNBS Curncy")
request.getElement("securities").appendValue("XBT ITBT Curncy")
request.getElement("securities").appendValue("XBT KRKN Curncy")
request.getElement("fields").appendValue("PX_LAST")
request.getElement("fields").appendValue("PX_BID")
#request.getElement("fields").appendValue("OPEN")
#request.set("periodicityAdjustment", "ACTUAL")
#request.set("periodicitySelection", "DAILY")
#request.set("startDate", "20140101")
#request.set("endDate", "20141114")
#request.set("maxDataPoints", 100)

#print "Sending Request:", request
# Send the request
session.sendRequest(request)
#fd = open("historicalData.txt","w")
# Process received events
json_array_buy = {}
json_array_sell = {}
while(True):
    # We provide timeout to give the chance for Ctrl+C handling:
    ev = session.nextEvent(500)
    for msg in ev:
		if str(msg.messageType()) == "ReferenceDataResponse":
			arr = str(msg.getElement("securityData"))
			while arr != "":
				key_index = arr.find("security =")
				if key_index == -1:
					break
				key_index +=  len("security = \"XBT ")
				name = getExchangeName(arr[key_index:key_index+4])
				value_index = arr.find("PX_LAST = ")
				if value_index == -1:
					break
				#print arr[value_index:value_index]
				value_index+=  len("PX_LAST =")
				val_index_end = arr.find("\n",value_index)
				json_array_buy[name] = float(arr[value_index:val_index_end])
				value_index = arr.find("PX_BID = ")
				if key_index == -1:
					break
				#print arr[value_index:value_index]
				value_index+=  len("PX_BID =")
				val_index_end = arr.find("}",value_index)
				json_array_sell[name] = float(arr[value_index:val_index_end])
				arr = arr[value_index:]
				
    if ev.eventType() == blpapi.Event.RESPONSE:
        # Response completly received, so we could exit
        break

print "Content-type: application/json"
print
print json.dumps({"key1":json_array_buy,"key2":json_array_sell})
