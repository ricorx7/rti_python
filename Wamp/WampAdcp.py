###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import six
from os import environ
import json
import glob

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
    def __init__(self, session):
        # Get a reference to Application session
        self.session = session

        port = self.session.config.extra['port']
        baud = self.session.config.extra['baudrate']

        try:
            serialPort = SerialPort(self, port, reactor, baudrate=baud)
        except Exception as e:
            self.session.log.error('Could not open serial port: {0}'.format(e))

        # Setup codec
        self.codec = AdcpCodec()
        self.codec.EnsembleEvent += self.ensemble_event

    def connectionMade(self):
        self.session.log.info('Serial port connected.')

    def connectionLost(self, reason):
        self.session.log.info("Lost connection (%s)" % reason)
        #if reason != twisted.internet.error.ConnectionDone:
        if reason.value.__class__ != twisted.internet.error.ConnectionDone:
            self.session.log.info("Reconnecting in 5 seconds...")
            self.retry = reactor.callLater(5, self.reconnect)

    def reconnect(self):
        self.session.log.info("Try to reconnect")

        port = self.session.config.extra['port']
        baud = self.session.config.extra['baudrate']

        try:
            serialPort = SerialPort(self, port, reactor, baudrate=baud)
        except Exception as e:
            self.session.log.error('Could not open serial port: {0}'.format(e))
            self.session.log.info("Reconnecting in 5 seconds...")
            self.retry = reactor.callLater(5, self.reconnect)


    def dataReceived(self, data):
        payload = {}
        payload["port"] = self.session.config.extra['port']
        payload["baud"] = self.session.config.extra['baudrate']
        try:
            payload["value"] = data.decode('utf-8').strip()
        except:
            payload["value"] = str(data)

        # Publish WAMP event to all subscribers on topic
        self.session.publish(u"com.rti.data.serial", json.dumps(payload))

        # Add data to the codec
        self.codec.add(data)

    def lineReceived(self, line):
        # Not Used
        self.session.log.info("Serial line RX: {0}".format(line))

    def ensemble_event(self, sender, ens):
        # publish WAMP event to all subscribers on topic
        self.session.publish(u"com.rti.data.ens", json.dumps(ens, default=lambda o: o.__dict__))

    def send_command(self, cmd):
        self.session.log.info("Serial TX: {0}".format(cmd))
        try:
            self.transport.write((cmd + "\r").encode('ascii', 'ignore'))
        except Exception as e:
            self.session.log.error(str(e))

    def send_break(self, time):
        self.session.log.info("Serial TX BREAK: {0}".format(str(time)))
        try:
            self.transport.sendBreak()
        except Exception as e:
            self.session.log.error(str(e))


class WampAdcpComponent(ApplicationSession):
    """
    WAMP application component.
    """
    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        print("WAMP ADCP component created")
        self.serialProtocol = None
        self.serialPort = None

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("MyComponent ready! Configuration: {}".format(self.config.extra))

        #yield self.register(self.serialProtocol.send_command, u"com.rti.oncmd")
        #yield self.register(self.serialProtocol.send_break, u"com.rti.onbreak")
        yield self.register(self.list_serial_ports, u"com.rti.serial.list.get")
        yield self.register(self.reconnect_serial, u"com.rti.serial.reconnect")
        yield self.register(self.send_cmd, u"com.rti.oncmd")
        yield self.register(self.send_break, u"com.rti.onbreak")

        port = self.config.extra['port']
        baudrate = self.config.extra['baudrate']
        self.log.info("WAMP Connection made")

        #self.serialProtocol = WampSerialProtocol(self)
        #self.log.info('About to open serial port {0} [{1} baud] ..'.format(port, baudrate))
        #try:
        #    self.serialPort = SerialPort(self.serialProtocol, port, reactor, baudrate=baudrate)
        #except Exception as e:
        #    self.log.error('Could not open serial port: {0}'.format(e))
        #    self.leave()
        #else:
        #    yield self.register(self.serialProtocol.send_command, u"com.rti.oncmd")
        #    yield self.register(self.serialProtocol.send_break, u"com.rti.onbreak")
        #    yield self.register(self.list_serial_ports, u"com.rti.serial.list.get")
        #    yield self.register(self.reconnect_serial, u"com.rti.serial.reconnect")

    def reconnect_serial(self, port, baud):
        self.log.info("New Serial Connection: " + port + " baud: " + baud)

        self.config.extra['port'] = port
        self.config.extra['baudrate'] = baud

        self.serialProtocol = WampSerialProtocol(self)

        #try:
        #    self.serialPort = SerialPort(self.serialProtocol, port, reactor, baudrate=baud)
        #except Exception as e:
        #    self.log.error('Could not open serial port: {0}'.format(e))
        #else:
        #    self.register(self.serialProtocol.send_command, u"com.rti.oncmd")
        #    self.register(self.serialProtocol.send_break, u"com.rti.onbreak")
        #self.log.info("New serial conneciton made: " + port + " baud: " + baud)

    def send_cmd(self, cmd):
        if self.serialProtocol:
            self.serialProtocol.send_command(cmd)

    def send_break(self, duration):
        if self.serialProtocol:
            self.serialProtocol.send_break(duration)

    def list_serial_ports(self, sender):
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
    runner.run(WampAdcpComponent)
