import urllib
import xml.sax

class PredictionHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.predictions = []
        self.pt = None

    def startElement(self,name,attrs):
        # If the starting 'pt' is encountered, set the self.pt to
        # the empty string.  This attribute will start to collect text
        if name == 'pt':
            self.pt = ""

    def characters(self,data):
        # Collect text if self.pt is set to something other than None
        if self.pt is not None:
            self.pt += data

    def endElement(self,name):
        # If ending 'pt' is encountered, append the collect text
        # to the prediction list
        if name == 'pt':
            self.predictions.append(self.pt)
            self.pt = None

def bus_prediction(route,stop):
    fields = { 'route' : route, 
               'stop' : stop }
    parms = urllib.urlencode(fields)
    u = urllib.urlopen("http://ctabustracker.com/bustime/map/getStopPredictions.jsp?"+parms)

    # Parse the XML
    hand = PredictionHandler()
    xml.sax.parse(u, hand)
    
    # Return the prediction list
    return hand.predictions
