from Comm.ADCP import ADCP

if __name__ == '__main__':
    adcp = ADCP()
    adcp.connect(55057)