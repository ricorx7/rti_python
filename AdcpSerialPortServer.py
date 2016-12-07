'''Connect through TCP to receive serial data.  This will
allow multiple TCP connections to one serial port.'''

from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.internet.serialport import SerialPort
import threading

class SerialDevice(basic.LineReceiver):
    """
    Serial device that will send data to
    all the TCP clients connected
    """
    def __init__(self, factory, tcp_server):
        self.factory = factory
        self.tcp_server = tcp_server

    def connectionMade(self):
        """
        Connect the serial port
        """
        print('Serial Connection made!')

    def connectionLost(self, reason):
        """
        Disconnect the serial port
        """
        #self.factory.clients.remove(self)
        print('Serial Connection lost')

    def dataReceived(self, data):
        """Send data to all the clients
        connected on the TCP port
        """
        #print("Response: {0}", format(data))
        for c in self.tcp_server.factory.clients:
            c.transport.write(data)
            #c.sendLine(data)

    def lineReceived(self, line):
        print('Serial line received: ', line)

    def rawDataReceived(self, data):
        print('Serial Raw Data received: ', data)


class SerialTcpProtocol(basic.LineReceiver):
    """
    Create TCP Connections for user that
    want to get serial data
    """

    def __init__(self, factory, comm_port, baud):
        self.factory = factory

        # Create a Serial Port device to read in serial data
        self.serial_port = SerialPort(SerialDevice(self, self), comm_port, reactor, baudrate=baud)
        print('Serial Port started')

    def resetSerialConnection(self, comm_port, baud):
        """
        Reset the Serial Port device to read in serial data
        """
        self.serial_port = SerialPort(SerialDevice(self, self), comm_port, reactor, baudrate=baud)
        print('Serial Port Restarted')

    def connectionMade(self):
        """
        Add TCP connections
        """
        self.factory.clients.add(self)
        print('TCP Connection made')

    def connectionLost(self, reason):
        """
        Disconnect TCP Connections
        """
        self.factory.clients.remove(self)
        print('TCP Connection lost')

    def dataReceived(self, data):
        """
        Receive data from the TCP port and send the data to the serial port
        """

        cmd = data.decode("ascii")

        if "BREAK" in cmd:
            self.serial_port.sendBreak()
            print('Hardware BREAK')
        if "RECONNECT" in cmd:
            self.reconnect(cmd)
        else:
            self.serial_port.writeSomeData(data)

        source = str(self.transport.getPeer())
        print(source + " - " + 'TCP data received: ' + cmd)

    def lineReceived(self, line):
        print('TCP line received: ', line)
        #for c in self.factory.clients:
            #source = u"<{}> ".format(self.transport.getHost()).encode("ascii")
            #c.sendLine(source + line)
            #print('line received: ', line)

    def rawDataReceived(self, data):
        print('TCP Raw data received: ', data)

    def reconnect(self, cmd):
        """
        Decode the RECONNECT command to configure a new serial port.
        """
        params = cmd.split(',')
        if len(params) < 3:
            print('Missing parameters to command: ' + cmd)
            return

        comm_port = params[1]
        try:
            baud = int(params[2])
        except:
            print('Baud rate must be an integer')
            return


        # Reset the serial port
        self.resetSerialConnection(comm_port, baud)
        print("Reconnect Serial to: " + comm_port + " baud: " + baud)


class AdcpFactory(protocol.Factory):
    """
    Create a serial connection and allow
    TCP clients to view the data
    """
    def __init__(self, comm_port, baud):
        self.clients = set()
        self.serial_comm_port = comm_port
        self.serial_baud = baud

    def buildProtocol(self, addr):
        return SerialTcpProtocol(self, self.serial_comm_port, self.serial_baud)


class AdcpSerialPortServer():
    """
    Create a serial connection and allow TCP
    clients to view the data
    """
    def __init__(self, port, comm_port, baud):
        self.port = "tcp:" + port       # TCP Port
        self.comm_port = comm_port      # Serial Port
        self.baud = baud                # Baud Rate

        # Set the TCP port to output ADCP data
        endpoints.serverFromString(reactor, self.port).listen(AdcpFactory(self.comm_port, self.baud))
        print("Serial port connected on", self.comm_port)
        print("TCP Port open on ", self.port)
        
        #reactor.run()
        # Run the reactor in a thread
        self.thread = threading.Thread(name='AdcpSerialPort', target=reactor.run, args=(False,)).start()

    def close(self):
        """
        Close the thread to the server
        """
        reactor.stop()
        for t in threading.enumerate():
            if t.getName() == 'AdcpSerialPort':
                t.join()
                print("Stop the ADP serial port thread")

# Set the PORT to output ADCP data
#endpoints.serverFromString(reactor, "tcp:55056").listen(AdcpFactory('/dev/cu.usbserial-FTYNODPO', 115200))
#reactor.run()
