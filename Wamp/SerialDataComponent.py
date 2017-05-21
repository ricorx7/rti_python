#import txaio
#txaio.use_twisted()
import threading
import time
import json
import socket
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from Comm.ReadTcpPort import ReadTcpPort


class SerialDataComponent(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        print("component created")
        self.tcp = None

    @inlineCallbacks
    def onJoin(self, details):
        print("session joined serial data")

        # Connect and read TCP
        self.connect_tcp(55056)

        threading.Thread(self.read_tcp()).start()

    def onConnect(self):
        print("transport connected serial data")
        self.join(self.config.realm)

    def onChallenge(self, challenge):
        print("authentication challenge received")

    def onLeave(self, details):
        print("session left")

    def onDisconnect(self):
        print("--------------transport disconnected---------------")
        self.tcp.close()

    def connect_tcp(self, port):
        self.log.debug("Make TCP Connection")
        print("Make TCP Connection")
        try:
            self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp.connect(('localhost', port))
            self.tcp.settimeout(1)  # Set timeout to stop thread if terminated
            print('TCP Connected')
        except ConnectionRefusedError as err:
            self.log.error("Serial Send Socket: ", err)
            print("Error connection refused to TCP")
            exit()
        except Exception as err:
            self.log.error('Serial Send Socket: ", Error Opening socket', err)
            print("Error connecting to TCP")
            exit()

    def read_tcp(self):
        while True:
            try:
                print("Start TCP Read")
                # Read data from socket
                data = self.tcp.recv(4096)
                print("Read TCP " + data)

                # If data exist process
                if len(data) > 0:
                    self.publish(u'com.rti.serialdata', data)
                    print(data)

            except socket.timeout:
                # Just a socket timeout, continue on
                print("tcp timeout")
                pass
            except Exception as e:
                self.log.error("Exception in reading data.", e)
                self.tcp.close()

    def process(self, adcp_data):
        """
        Receive data for the UDP port.  Publish it to the WAMP router.
        :param json_data: JSON data from UDP port.
        :return:
        """
        #try:
        #json_data = json.dumps(adcp_data.__dict__)
        #print(json_data)
        yield self.publish(u'com.rti.serialdata', adcp_data)
        #yield self.publish('com.rti.serialdata', adcp_data)
        #print('.')
        #except Exception as e:
        #    print("could not publish to com.rti.serial.data: {0}".format(e))
        #    self.log.error(format(e))
