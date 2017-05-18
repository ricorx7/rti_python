from Comm.ReadTcpPort import ReadTcpPort


if __name__ == '__main__':
    tcp = ReadTcpPort()
    tcp.connect('55056')

