from flask import Flask
app = Flask(__name__)

import blpapi
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


def main():
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
    request.append("securities", "IBM US Equity")
    request.append("securities", "MSFT US Equity")

    # append fields to request
    request.append("fields", "PX_LAST")
    request.append("fields", "DS002")

    print "Sending Request:", request
    session.sendRequest(request)
    jsonBack = '';


    try:
        # Process received events
        while(True):
            # We provide timeout to give the chance to Ctrl+C handling:
            ev = session.nextEvent(500)
            for msg in ev:
		print msg.toString()
            # Response completly received, so we could exit
            if ev.eventType() == blpapi.Event.RESPONSE:
		return ev.toString()
                break
    finally:
        # Stop the session
	
        session.stop()

__copyright__ = """
Copyright 2012. Bloomberg Finance L.P."""



@app.route('/bapi')
def bapi():
    a = '123'
    return a
    #return os.system("python text.py")

@app.route("/")
def hello():
    a = main()
    return a

if __name__ == "__main__":
    app.run()
