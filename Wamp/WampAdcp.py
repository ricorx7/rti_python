import six
from os import environ
import json
import glob
import datetime

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.defer import inlineCallbacks
from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import LineReceiver
import twisted.internet.error

from autobahn.twisted.wamp import ApplicationSession
from Codecs.AdcpCodec import AdcpCodec


class WampSerialProtocol(LineReceiver):
    """
    Serial communication protocol.
    """
    # need a reference to our WS-MCU gateway factory to dispatch PubSub events
    def __init__(self, session, port, baud):
        # Get a reference to Application session
        self.session = session
        self.serialPort = None

        #port = self.session.config.extra['port']
        #baud = self.session.config.extra['baudrate']

        try:
            self.serialPort = SerialPort(self, port, reactor, baudrate=baud)
        except Exception as e:
            self.session.log.error('Could not open serial port: {0}'.format(e))

        # Setup codec
        self.codec = AdcpCodec()
        self.codec.EnsembleEvent += self.ensemble_event

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
        self.factory.resetDelay()

    def connectionMade(self):
        """
        Called when the serial made a connection.
        :return: 
        """
        self.session.log.info('Serial port connected.')

    def connectionLost(self, reason):
        """
        Called if the connection is lost.  If the Connection was
        lost because the connection was disconnected properly,
        then do nothing.  If it lost connection because the
        serial port was lost, then try to reconnect.
        :param reason: 
        :return: 
        """
        self.session.log.info("Lost connection (%s)" % reason)

        # Check if the reason was a good disconnect
        if reason.value.__class__ != twisted.internet.error.ConnectionDone:
            self.session.log.info("Reconnecting in 5 seconds...")
            self.retry = reactor.callLater(5, self.reconnect_attempt)

    def reconnect_attempt(self):
        """
        Used so that checking for disconnects, it does not need to know
        the current configuration.
        :return: 
        """
        # Get the port and baud from the configuration
        port = self.session.config.extra['port']
        baud = self.session.config.extra['baudrate']
        self.reconnect(port, baud)

    def reconnect(self, port, baud):
        """
        Reconnect the serial port.
        :return: 
        """
        self.session.log.info("Try to reconnect")

        # Reset the transport
        self.transport.loseConnection()

        # Create a new serial port
        try:
            self.serialPort = SerialPort(self, port, reactor, baudrate=baud)
        except Exception as e:
            self.session.log.error('Could not open serial port: {0}'.format(e))
            self.session.log.info("Reconnecting in 5 seconds...")
            self.retry = reactor.callLater(5, self.reconnect_attempt)


    def dataReceived(self, data):
        """
        Data received from the serial port.
        :param data: Data received from the serial port.
        :return: 
        """
        payload = {}
        payload["port"] = self.session.config.extra['port']
        payload["baud"] = self.session.config.extra['baudrate']
        try:
            payload["value"] = data.decode('utf-8')
            payload["type"] = "command"
        except:
            payload["value"] = str(data)
            payload["type"] = "binary"

        # Publish WAMP event to all subscribers on topic
        self.session.publish(u"com.rti.data.serial", json.dumps(payload))

        # Add data to the codec
        self.codec.add(data)

    def lineReceived(self, line):
        # Not Used
        self.session.log.info("Serial line RX: {0}".format(line))

    def ensemble_event(self, sender, ens):
        """
        This is called when the codec has a processed ensemble.
        :param sender: Sender of the ensemble.
        :param ens: Ensemble as JSON.
        :return: 
        """
        # publish WAMP event to all subscribers on topic
        self.session.publish(u"com.rti.data.ens", json.dumps(ens, default=lambda o: o.__dict__))

    def send_command(self, cmd):
        """
        Send a command to the serial port.
        :param cmd: Command to send to the serial port.
        :return: 
        """
        self.session.log.info("Serial TX: {0}".format(cmd))
        try:
            self.transport.write((cmd + "\r").encode('ascii', 'ignore'))
        except Exception as e:
            self.session.log.error(str(e))

    def send_break(self, time):
        """
        Send a BREAK to the serial port.
        :param time: Duration of the BREAK.
        :return: 
        """
        self.session.log.info("Serial TX BREAK: {0}".format(str(time)))
        try:
            self.transport.sendBreak()
            #self.serialPort.sendBreak()
        except Exception as e:
            self.session.log.error("send_break Error: " + str(e))


class WampAdcpComponent(ApplicationSession, ReconnectingClientFactory):
    """
    WAMP application component.
    """
    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        print("WAMP ADCP component created")
        self.serialProtocol = None

    def clientConnectionFailed(self, connector, reason):
        print("Client connection failed .. retrying ..")
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        print("Client connection lost .. retrying ..")
        self.retry(connector)

    @inlineCallbacks
    def onJoin(self, details):
        """
        Called to initialize the WAMP ApplicationSession.
        :param details: 
        :return: 
        """
        self.log.info("MyComponent ready! Configuration: {}".format(self.config.extra))

        # Register functions with WAMP
        yield self.register(self.list_serial_ports, u"com.rti.serial.list.get")
        yield self.register(self.reconnect_serial, u"com.rti.serial.reconnect")
        yield self.register(self.send_cmd, u"com.rti.oncmd")
        yield self.register(self.send_break, u"com.rti.onbreak")
        yield self.register(self.set_time, u"com.rti.onsettime")

        self.log.info("WAMP Connection made")

    def reconnect_serial(self, port, baud):
        """
        Reconnect the serial port connection.  This will create a new
        Protocol which will create a new connection.  The new conneciton 
        will get the port and baud rate form the self.config
        :param port: Serial Port as a string.
        :param baud: Baud rate as a string.
        :return: 
        """
        self.log.info("New Serial Connection: " + port + " baud: " + baud)

        # Set the port and baud rate so the Protocol will know when needing to reconnect
        self.config.extra['port'] = port
        self.config.extra['baudrate'] = baud

        # If the protocol has not been created yet
        # Create a new protocol
        # else call reconnect to change the connection
        if not self.serialProtocol:
            self.serialProtocol = WampSerialProtocol(self, port, baud)
        else:
            self.serialProtocol.reconnect(port, baud)

    def send_cmd(self, cmd):
        """
        Send a command to the Protocol.
        :param cmd: Command to send.
        :return: 
        """
        if self.serialProtocol:
            self.serialProtocol.send_command(cmd)

    def send_break(self, duration):
        """
        Send a BREAK to the protocol.
        :param duration: Duration of the BREAK.
        :return: 
        """
        if self.serialProtocol:
            self.serialProtocol.send_break(duration)

    def set_time(self):
        if self.serialProtocol:
            # yyyy/MM/dd,HH:mm:ss
            dt = datetime.datetime.now()
            dt_str = dt.strftime("%Y/%m/%d,%H:%M:%S")
            self.serialProtocol.send_command("STIME " + dt_str)

    def list_serial_ports(self):
        """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = ports
        #for port in ports:
        #    try:
        #        s = serial.Serial(port)
        #        s.close()
        #        result.append(port)
        #        print(port)
        #    except OSError as err:
        #        self.log.error(err)
        #        print(err)
        #        pass
        #    except serial.SerialException as err:
        #        self.log.error(err)
        #        print(err)
        #        pass

        self.publish(u"com.rti.serial.list", json.dumps(result, default=lambda o: o.__dict__))

        return result


if __name__ == '__main__':

    import sys
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--baudrate", type=int, default=115200, choices=[300, 1200, 2400, 4800, 9600, 19200, 57600, 115200, 230400, 460800, 921600],
                        help='Serial port baudrate.')

    parser.add_argument("--port", type=six.text_type, default=u'/dev/tty.usbserial-FT0ED8ZR',
                        help='Serial port to use (e.g. 3 for a COM port on Windows, /dev/ttyATH0 for Arduino Yun, /dev/ttyACM0 for Serial-over-USB on RaspberryPi.')

    parser.add_argument("--web", type=int, default=8000,
                        help='Web port to use for embedded Web server. Use 0 to disable.')

    router_default = environ.get("RTI_ROUTER", u"ws://127.0.0.1:55058/ws")
    parser.add_argument("--router", type=six.text_type, default=router_default,
                        help='WAMP router URL (a WAMP-over-WebSocket endpoint, default: "{}")'.format(router_default))

    parser.add_argument("--realm", type=six.text_type, default=u'realm1',
                        help='WAMP realm to join (default: "realm1")')

    args = parser.parse_args()

    # import Twisted reactor
    if sys.platform == 'win32':
        # on Windows, we need to use the following reactor for serial support
        # http://twistedmatrix.com/trac/ticket/3802
        from twisted.internet import win32eventreactor
        win32eventreactor.install()

        # on Windows, we need port to be an integer
        args.port = int(args.port)

    from twisted.internet import reactor
    print("Using Twisted reactor {0}".format(reactor.__class__))

    # create embedded web server for static files
    if args.web:
        from twisted.web.server import Site
        from twisted.web.static import File
        reactor.listenTCP(args.web, Site(File(".")))

    # run WAMP application component
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner(args.router, args.realm,
                               extra={'port': args.port, 'baudrate': args.baudrate})

    # start the component and the Twisted reactor ..
    runner.run(WampAdcpComponent, auto_reconnect=True)
