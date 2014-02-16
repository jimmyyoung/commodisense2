from flask import Flask
app = Flask(__name__)

import blpapi
from optparse import OptionParser

import getMarketData
import tickPredict
import getSellData

@app.route("/getsell")
@app.route("/getsell/<ticker>")
def getSellDatam(ticker=None):
    if not ticker:
        return '{"error":"Empty Ticker"}'
    ticker = ticker.replace('_', ' ')
    ticker = tickPredict.parse(ticker)
    a = getSellData.getSells(ticker)
    return a

@app.route('/bapi')
def bapi():
    a = '123'
    return a
    #return os.system("python text.py")

@app.route("/")
def hello():
    return "hi"

@app.route("/fastparse")
@app.route("/fastparse/<ticker>")
def parseTicker(ticker=None):
    if not ticker:
	return '{"error":"Empty Ticker"}'
    ticker = ticker.replace('_', ' ')
    ticker = tickPredict.parse(ticker)
    return ticker

@app.route("/getdata")
@app.route("/getdata/<ticker>")
def getData(ticker=None):
    if not ticker:
	return '{"error":"Empty Ticker"}'
    #if (name === None) return '{"error":"No Ticker Provided"}'
    ticker = ticker.replace('_', ' ')
    ticker = tickPredict.parse(ticker)
    a = getMarketData.main(ticker)
    return a

if __name__ == "__main__":
    app.run()
