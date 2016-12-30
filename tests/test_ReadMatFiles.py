from os import walk
import pprint
import scipy.io

import configparser
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('../settings.ini')

filepath = filepath = settings.get('WavesProjectSection', 'CaptureFilePath')
#filepath += "D00002.mat"


f = []
for (dirpath, dirnames, filenames) in walk(filepath):
    f.extend(filenames)
    break  # Stop on first directory in path

# Setup pretty printing for dictionary
pp = pprint.PrettyPrinter(indent=4)

# Print all the values in every file
for i in range(len(f)):
    mat = scipy.io.loadmat(filepath + filenames[i])
    pp.pprint(mat)


