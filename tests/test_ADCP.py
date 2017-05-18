from Comm.EnsembleReceiver import EnsembleReceiver

if __name__ == '__main__':
    adcp = EnsembleReceiver()
    adcp.connect(55057)
