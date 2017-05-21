
from __future__ import print_function

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory, Protocol
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession

"""
Example coded: 
https://github.com/crossbario/autobahn-python/blob/master/examples/twisted/wamp/app/serial2ws/serial2ws.py
"""


class SerialDataTwistedAppSession(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        print("component created")

    @inlineCallbacks
    def onJoin(self, details):
        print("session joined serial data twisted")

        # Create an insatance of TCP Protocol and pass itself
        # so it can use it to publish.  Use factory to auto reconnect
        reactor.connectTCP("localhost", 55056, SerialDataTwistedFactory(self))

    def onConnect(self):
        print("transport connected serial data twisted")
        self.join(self.config.realm)

    def onChallenge(self, challenge):
        print("authentication challenge received twisted")

    def onLeave(self, details):
        print("session left twisted")
        reactor.stop()

    def onDisconnect(self):
        print("--------------transport disconnected twisted---------------")


class SerialDataTwistedProtocol(Protocol):
    def __init__(self, session):
        # Get the WAMP session
        self.session = session

    def dataReceived(self, data):
        #print("Server said:", data)
        # Publish data to WAMP
        self.session.publish(u'com.rti.serialdata', str(data))
        print("published to 'serialdata' with " + str(len(data)) + " amount of data")

    def connectionMade(self):
        print('connection made twisted')

    def connectionLost(self, reason):
        print("connection lost")


class SerialDataTwistedFactory(ReconnectingClientFactory):

    def __init__(self, session):
        # Get the WAMP session
        self.session = session

    def buildProtocol(self, addr):
        print('Connected.')
        print('Resetting reconnection delay')
        self.resetDelay()

        # Pass the WAMP session
        return SerialDataTwistedProtocol(self.session)

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - try to reconnect " + str(reason))
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - try to reconnect! " + str(reason))
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
