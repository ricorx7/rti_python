from Comm.ReadTcpPort import ReadTcpPort


if __name__ == '__main__':

    def process(data):
        print(data)

    tcp = ReadTcpPort()
    tcp.process = process
    tcp.connect('55056')
    print('TCP Reader started')

