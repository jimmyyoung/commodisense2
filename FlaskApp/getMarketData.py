# SimpleRefDataExample.py

import blpapi
import json
from optparse import OptionParser


def parseCmdLine():
    parser = OptionParser(description="Retrieve reference data.")
    parser.add_option("-a",
                      "--ip",
                      dest="host",
                      help="server name or IP (default: %default)",
                      metavar="ipAddress",
                      default="10.8.8.1")
    parser.add_option("-p",
                      dest="port",
                      type="int",
                      help="server port (default: %default)",
                      metavar="tcpPort",
                      default=8194)

    (options, args) = parser.parse_args()

    return options


def main(ticker):
    global options
    options = parseCmdLine()

    # Fill SessionOptions
    sessionOptions = blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print "Connecting to %s:%d" % (options.host, options.port)

    # Create a Session
    session = blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print "Failed to start session."
        return

    if not session.openService("//blp/refdata"):
        print "Failed to open //blp/refdata"
        return

    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("ReferenceDataRequest")

    # append securities to request
    request.append("securities", ticker)
    #request.append("securities", "IBM US Equity")

    # append fields to request
    request.append("fields", "PX_LAST")
    request.append("fields", "DS002") #Description
    request.append("fields", "BID")
    request.append("fields", "ASK")

    #print "Sending Request:", request
    session.sendRequest(request)

    try:
        # Process received events
        while(True):
            # We provide timeout to give the chance to Ctrl+C handling:
            ev = session.nextEvent(500)
            for msg in ev:
                if msg.hasElement('securityData'):
			data_last = msg.getElement('securityData').getValue(0).getElement('fieldData');
			if not data_last.hasElement('DS002'):
				return '{"error":' + ticker + ' not found"}'
			if not data_last.hasElement('PX_LAST'):
				return '{"error":"Current Price Not Available"}'
			data_price = data_last.getElement('PX_LAST').getValue(0)
			data_desc = data_last.getElement('DS002').getValue(0)
			data_bid = None;
			data_ask = None;
			if data_last.hasElement('BID'):
				data_bid = data_last.getElement('BID').getValue(0)
			if data_last.hasElement('ASK'):
				data_ask = data_last.getElement('ASK').getValue(0)

			a = { "ticker" : ticker,
			      "price" : data_price,
			      "desc" : data_desc,
			      "bid" : data_bid,
			      "ask" : data_ask  
			}
			return str(json.dumps(a))
	# Response completly received, so we could exit
            if ev.eventType() == blpapi.Event.RESPONSE:
                break
    finally:
        # Stop the session
        session.stop()

__copyright__ = """
Copyright 2012. Bloomberg Finance L.P.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  The above
copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
