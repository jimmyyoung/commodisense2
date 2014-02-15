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
    #if (name === None) return '{"error":"No Ticker Provided"}'
    a = getMarketData.main()
    return a

if __name__ == "__main__":
    app.run()
