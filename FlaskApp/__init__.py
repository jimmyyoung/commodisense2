from flask import Flask
app = Flask(__name__)

import blpapi
from optparse import OptionParser

import getMarketData

@app.route('/bapi')
def bapi():
    a = '123'
    return a
    #return os.system("python text.py")

@app.route("/")
def hello():
    return "hi"

@app.route("/getdata")
@app.route("/getdata/<ticker>")
def getData(ticker=None):
    if not ticker:
	return '{"error":"Empty Ticker"}'
    #if (name === None) return '{"error":"No Ticker Provided"}'
    ticker = ticker.replace('_', ' ')
    a = getMarketData.main(ticker)
    return a

if __name__ == "__main__":
    app.run()
