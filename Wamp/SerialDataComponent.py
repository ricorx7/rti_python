#import txaio
#txaio.use_twisted()
import threading
import time
import json
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from Comm.ReadTcpPort import ReadTcpPort


class SerialDataComponent(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        print("component created")

        self.tcp = None

        #self.ensemble_rcvr = EnsembleReceiver()
        #self.ensemble_rcvr.EnsembleEvent = self.process


    @inlineCallbacks
    def onJoin(self, details):
        print("session joined serial data")
        self.tcp = ReadTcpPort()
        self.tcp.process = self.process()
        threading.Thread(target=self.tcp.connect('55056'))
        print('TCP port connected')

    def onConnect(self):
        print("transport connected serial data")
        self.join(self.config.realm)

    def onChallenge(self, challenge):
        print("authentication challenge received")

    def onLeave(self, details):
        print("session left")

    def onDisconnect(self):
        print("--------------transport disconnected---------------")

    def process(self, adcp_data):
        """
        Receive data for the UDP port.  Publish it to the WAMP router.
        :param json_data: JSON data from UDP port.
        :return:
        """
        try:
            json_data = json.dumps(adcp_data.__dict__)
            #print(json_data)
            #self.publish(u'com.rti.serial.data', json_data)
            yield self.publish('com.rti.serialdata', json_data)
            print('.')
        except Exception as e:
            print("could not publish to com.rti.serial.data: {0}".format(e))
            self.log.error(format(e))
