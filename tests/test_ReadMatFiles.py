import scipy.io

import configparser
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('../settings.ini')

filepath = settings.get('SerialServerSection', 'WaveCaptureFilePath')
filepath += "D00007.mat"

#for code in map(ord, 'txt '):
#    print(code)
#print('txt '.encode('utf-8'))

mat = scipy.io.loadmat(filepath)

print(mat)