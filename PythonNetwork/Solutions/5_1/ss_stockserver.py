# ss_stockserver.py

# A stand-alone HTTP server that feeds real-time stock quotes.
# Stock quote data is obtained from Yahoo, but in reality you
# would use some other internal data source (data source, 
# real-time feed, etc.)
#
# This server is built directly on top of the SocketServer
# library--the lowest networking module in Python's library
# that's used to implement servers.

from SocketServer import BaseRequestHandler, TCPServer
from string import Template
import urllib, csv

# Output template that we'll fill in with various fields
output = Template("""<?xml version="1.0"?>
<quote>
   <stock>
       <symbol>$symbol</symbol>
       <name><![CDATA[$name]]></name>
       <price>$price</price>
       <change>$change</change>
       <percent>$percent</percent>
       <date>$date</date>
       <time>$time</time>
       <open>$open</open>
       <high>$high</high>
       <low>$low</low>
       <volume>$volume</volume>
    <stock>
<quote>
""")

class StockHandler(BaseRequestHandler):
    def handle(self):
        # Read 8K of any HTTP request data that has arrived
        req = self.request.recv(8192)

        # Unpack the three fields that make up the HTTP request line (e.g., GET /IBM HTTP/1.0)
        try:
            meth, doc, proto, remaining = req.split(None,3)
        except ValueError:
            # Malformed or incomplete request. Forget it
            self.request.close()
            return

        # Get the stock name.  Just need to strip the leading / 
        s = doc[1:]

        # Fetch data about the selected stock
        request = {
            's' : s,
            'f' : 'snl1d1t1c1p2ohgv',
            'e' : '.csv'
            }

        parms = urllib.urlencode(request)

        u = urllib.urlopen("http://download.finance.yahoo.com/d/quotes.csv?"+parms)
        reader = csv.DictReader(u,['symbol','name','price','date','time','change','percent',
                               'open','high','low','volume'])

        record = reader.next()

        # Send the raw HTTP response back to the client
        self.request.sendall("HTTP/1.0 200 OK\r\n")
        self.request.sendall("Content-type: application/xml\r\n")
        self.request.sendall("\r\n\r\n")
        self.request.sendall(output.substitute(record))

serv = TCPServer(("",45000),StockHandler)
serv.serve_forever()
