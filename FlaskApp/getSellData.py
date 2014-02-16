import pymongo
import json
import datetime
from pymongo import MongoClient
from datetime import datetime

def getSells(ticker, datefrom=1):  #datefrom is unix time
	client = MongoClient()
	db = client.test
	mongo_records = db.securitySell.find( { "datelisted" : { "$gt": datefrom }, "ticker_code": ticker})

	json_data = []
	for record in mongo_records:
		a = record;
		a['datelisted'] =  str(a['datelisted'])
		a['_id'] = None;
		json_data.append(a)
	print json.dumps(json_data)
	return json.dumps(json_data)
#getSells("ZWH4 Comdty", 0)
