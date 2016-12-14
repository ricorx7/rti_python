#!/usr/bin/env python
"""Log splitter for Rowe Technology DVL/ADCP ensemble files.

"""

def export_ensembles(infile):
    """Read a Rowe DVL/ADCP ensemble file (.ENS)

    """
    with open(infile, 'rb') as f:
        raw = f.read() # reads entire file. There's probably a smarter option.
        delimiter = '\x80'* 16  # look for first 16 bytes of header
        return raw.split(delimiter)


def export_ensembles_as_mat_files(infile, number_of_ensembles=9):
    """Read a Rowe DVL/ADCP ensemble file (.ENS) and write several ensembles
    out as separate MATLAB files (.MAT).

    """
    with open(infile, 'rb') as f:
        raw = f.read() # reads entire file. There's probably a smarter option.
        delimiter = '\x80'* 16  # look for first 16 bytes of header
        ensembles = raw.split(delimiter)[2:2 + number_of_ensembles]
        # line above discards any data before first header and any data
        # past specified number_of_ensembles
        for ensemble_number, ensemble in enumerate(ensembles):
            with open('{0}.mat'.format(ensemble_number), 'wb') as outfile:
                outfile.write(ensemble[16:-4])  # discard header & checksum