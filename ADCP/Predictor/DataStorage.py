import math
import json
import os


def calculate_storage_amount(**kwargs):
    """
    Calculate the amount of storage required for the parameter for the deployment.
    Value given in bytes.

    :param CWPBN=: Number of bins.
    :param Beams=: Number of beams.
    :param DeploymentDuration=: Deployment duration.
    :param CEI=: Time between ensembles.
    :param IsE0000001=: Flag if IsE0000001 is enabled.
    :param IsE0000002=: Flag if IsE0000002 is enabled.
    :param IsE0000003=: Flag if IsE0000003 is enabled.
    :param IsE0000004=: Flag if IsE0000004 is enabled.
    :param IsE0000005=: Flag if IsE0000005 is enabled.
    :param IsE0000006=: Flag if IsE0000006 is enabled.
    :param IsE0000007=: Flag if IsE0000007 is enabled.
    :param IsE0000008=: Flag if IsE0000008 is enabled.
    :param IsE0000009=: Flag if IsE0000009 is enabled.
    :param IsE0000010=: Flag if IsE0000010 is enabled.
    :param IsE0000011=: Flag if IsE0000011 is enabled.
    :param IsE0000012=: Flag if IsE0000012 is enabled.
    :param IsE0000013=: Flag if IsE0000013 is enabled.
    :param IsE0000014=: Flag if IsE0000014 is enabled.
    :param IsE0000015=: Flag if IsE0000015 is enabled.
    :return: Number of bytes required for the given deployment.
    """

    # Get the configuration from the json file
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, 'predictor.json')
    try:
        config = json.loads(open(json_file_path).read())
    except Exception as e:
        print("Error opening JSON file", e)
        return 0.0

    return _calculate_storage_amount(kwargs.pop('CWPBN', config['DEFAULT']['CWPBN']),
                                     kwargs.pop('Beams', config['DEFAULT']['Beams']),
                                     kwargs.pop('DeploymentDuration', config['DEFAULT']['DeploymentDuration']),
                                     kwargs.pop('CEI', config['DEFAULT']['CEI']),
                                     kwargs.pop('IsE0000001', config['DEFAULT']['IsE0000001']),
                                     kwargs.pop('IsE0000002', config['DEFAULT']['IsE0000002']),
                                     kwargs.pop('IsE0000003', config['DEFAULT']['IsE0000003']),
                                     kwargs.pop('IsE0000004', config['DEFAULT']['IsE0000004']),
                                     kwargs.pop('IsE0000005', config['DEFAULT']['IsE0000005']),
                                     kwargs.pop('IsE0000006', config['DEFAULT']['IsE0000006']),
                                     kwargs.pop('IsE0000007', config['DEFAULT']['IsE0000007']),
                                     kwargs.pop('IsE0000008', config['DEFAULT']['IsE0000008']),
                                     kwargs.pop('IsE0000009', config['DEFAULT']['IsE0000009']),
                                     kwargs.pop('IsE0000010', config['DEFAULT']['IsE0000010']),
                                     kwargs.pop('IsE0000011', config['DEFAULT']['IsE0000011']),
                                     kwargs.pop('IsE0000012', config['DEFAULT']['IsE0000012']),
                                     kwargs.pop('IsE0000013', config['DEFAULT']['IsE0000013']),
                                     kwargs.pop('IsE0000014', config['DEFAULT']['IsE0000014']),
                                     kwargs.pop('IsE0000015', config['DEFAULT']['IsE0000015']))


def calculate_burst_storage_amount(**kwargs):
    """
    Calculate the amount of storage required for the parameter for the deployment.
    Value given in bytes.

    :param CBI_NumEns: Number of ensembles in the burst.
    :param CWPBN=: Number of bins.
    :param Beams=: Number of beams.
    :param DeploymentDuration=: Deployment duration.
    :param CBI_BurstInterval=: Time between bursts.
    :param IsE0000001=: Flag if IsE0000001 is enabled.
    :param IsE0000002=: Flag if IsE0000002 is enabled.
    :param IsE0000003=: Flag if IsE0000003 is enabled.
    :param IsE0000004=: Flag if IsE0000004 is enabled.
    :param IsE0000005=: Flag if IsE0000005 is enabled.
    :param IsE0000006=: Flag if IsE0000006 is enabled.
    :param IsE0000007=: Flag if IsE0000007 is enabled.
    :param IsE0000008=: Flag if IsE0000008 is enabled.
    :param IsE0000009=: Flag if IsE0000009 is enabled.
    :param IsE0000010=: Flag if IsE0000010 is enabled.
    :param IsE0000011=: Flag if IsE0000011 is enabled.
    :param IsE0000012=: Flag if IsE0000012 is enabled.
    :param IsE0000013=: Flag if IsE0000013 is enabled.
    :param IsE0000014=: Flag if IsE0000014 is enabled.
    :param IsE0000015=: Flag if IsE0000015 is enabled.
    :return: Number of bytes required for the given deployment.
    """

    # Get the configuration from the json file
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, 'predictor.json')
    try:
        config = json.loads(open(json_file_path).read())
    except Exception as e:
        print("Error opening JSON file", e)
        return 0.0

    return _calculate_burst_storage_amount(kwargs.pop('CBI_NumEns', config['DEFAULT']['CBI_NumEns']),
                                           kwargs.pop('CBI_BurstInterval', config['DEFAULT']['CBI_BurstInterval']),
                                           kwargs.pop('CWPBN', config['DEFAULT']['CWPBN']),
                                             kwargs.pop('Beams', config['DEFAULT']['Beams']),
                                             kwargs.pop('DeploymentDuration', config['DEFAULT']['DeploymentDuration']),
                                             kwargs.pop('IsE0000001', config['DEFAULT']['IsE0000001']),
                                             kwargs.pop('IsE0000002', config['DEFAULT']['IsE0000002']),
                                             kwargs.pop('IsE0000003', config['DEFAULT']['IsE0000003']),
                                             kwargs.pop('IsE0000004', config['DEFAULT']['IsE0000004']),
                                             kwargs.pop('IsE0000005', config['DEFAULT']['IsE0000005']),
                                             kwargs.pop('IsE0000006', config['DEFAULT']['IsE0000006']),
                                             kwargs.pop('IsE0000007', config['DEFAULT']['IsE0000007']),
                                             kwargs.pop('IsE0000008', config['DEFAULT']['IsE0000008']),
                                             kwargs.pop('IsE0000009', config['DEFAULT']['IsE0000009']),
                                             kwargs.pop('IsE0000010', config['DEFAULT']['IsE0000010']),
                                             kwargs.pop('IsE0000011', config['DEFAULT']['IsE0000011']),
                                             kwargs.pop('IsE0000012', config['DEFAULT']['IsE0000012']),
                                             kwargs.pop('IsE0000013', config['DEFAULT']['IsE0000013']),
                                             kwargs.pop('IsE0000014', config['DEFAULT']['IsE0000014']),
                                             kwargs.pop('IsE0000015', config['DEFAULT']['IsE0000015']))


def calculate_ensemble_size(**kwargs):
    """
    Calculate the amount of storage required for the parameter for the deployment.
    Value given in bytes.

    :param CWPBN=: Number of bins.
    :param Beams=: Number of beams.
    :param DeploymentDuration=: Deployment duration.
    :param CEI=: Time between ensembles.
    :param IsE0000001=: Flag if IsE0000001 is enabled.
    :param IsE0000002=: Flag if IsE0000002 is enabled.
    :param IsE0000003=: Flag if IsE0000003 is enabled.
    :param IsE0000004=: Flag if IsE0000004 is enabled.
    :param IsE0000005=: Flag if IsE0000005 is enabled.
    :param IsE0000006=: Flag if IsE0000006 is enabled.
    :param IsE0000007=: Flag if IsE0000007 is enabled.
    :param IsE0000008=: Flag if IsE0000008 is enabled.
    :param IsE0000009=: Flag if IsE0000009 is enabled.
    :param IsE0000010=: Flag if IsE0000010 is enabled.
    :param IsE0000011=: Flag if IsE0000011 is enabled.
    :param IsE0000012=: Flag if IsE0000012 is enabled.
    :param IsE0000013=: Flag if IsE0000013 is enabled.
    :param IsE0000014=: Flag if IsE0000014 is enabled.
    :param IsE0000015=: Flag if IsE0000015 is enabled.
    :return: Number of bytes required for the given deployment.
    """

    # Get the configuration from the json file
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, 'predictor.json')
    try:
        config = json.loads(open(json_file_path).read())
    except Exception as e:
        print("Error opening JSON file", e)
        return 0.0

    return _calculate_ensemble_size(kwargs.pop('CWPBN', config['DEFAULT']['CWPBN']),
                                     kwargs.pop('Beams', config['DEFAULT']['Beams']),
                                     kwargs.pop('IsE0000001', config['DEFAULT']['IsE0000001']),
                                     kwargs.pop('IsE0000002', config['DEFAULT']['IsE0000002']),
                                     kwargs.pop('IsE0000003', config['DEFAULT']['IsE0000003']),
                                     kwargs.pop('IsE0000004', config['DEFAULT']['IsE0000004']),
                                     kwargs.pop('IsE0000005', config['DEFAULT']['IsE0000005']),
                                     kwargs.pop('IsE0000006', config['DEFAULT']['IsE0000006']),
                                     kwargs.pop('IsE0000007', config['DEFAULT']['IsE0000007']),
                                     kwargs.pop('IsE0000008', config['DEFAULT']['IsE0000008']),
                                     kwargs.pop('IsE0000009', config['DEFAULT']['IsE0000009']),
                                     kwargs.pop('IsE0000010', config['DEFAULT']['IsE0000010']),
                                     kwargs.pop('IsE0000011', config['DEFAULT']['IsE0000011']),
                                     kwargs.pop('IsE0000012', config['DEFAULT']['IsE0000012']),
                                     kwargs.pop('IsE0000013', config['DEFAULT']['IsE0000013']),
                                     kwargs.pop('IsE0000014', config['DEFAULT']['IsE0000014']),
                                     kwargs.pop('IsE0000015', config['DEFAULT']['IsE0000015']))



def _calculate_storage_amount(_CWPBN_, _Beams_,
                            _DeploymentDuration_, _CEI_,
                            IsE0000001, IsE0000002, IsE0000003,
                            IsE0000004, IsE0000005, IsE0000006,
                            IsE0000007, IsE0000008, IsE0000009,
                            IsE0000010, IsE0000011, IsE0000012,
                            IsE0000013, IsE0000014, IsE0000015):

    """
    Calculate the amount of storage required for the parameter for the deployment.
    Value given in bytes.

    :param _CWPBN_: Number of bins.
    :param _Beams_: Number of beams.
    :param _DeploymentDuration_: Deployment duration.
    :param _CEI_: Time between ensembles.
    :param IsE0000001: Flag if IsE0000001 is enabled.
    :param IsE0000002: Flag if IsE0000002 is enabled.
    :param IsE0000003: Flag if IsE0000003 is enabled.
    :param IsE0000004: Flag if IsE0000004 is enabled.
    :param IsE0000005: Flag if IsE0000005 is enabled.
    :param IsE0000006: Flag if IsE0000006 is enabled.
    :param IsE0000007: Flag if IsE0000007 is enabled.
    :param IsE0000008: Flag if IsE0000008 is enabled.
    :param IsE0000009: Flag if IsE0000009 is enabled.
    :param IsE0000010: Flag if IsE0000010 is enabled.
    :param IsE0000011: Flag if IsE0000011 is enabled.
    :param IsE0000012: Flag if IsE0000012 is enabled.
    :param IsE0000013: Flag if IsE0000013 is enabled.
    :param IsE0000014: Flag if IsE0000014 is enabled.
    :param IsE0000015: Flag if IsE0000015 is enabled.
    :return: Number of bytes required for the given deployment.
    """

    ensembleSize = _calculate_ensemble_size(_CWPBN_, _Beams_,
                                           IsE0000001, IsE0000002,
                                           IsE0000003, IsE0000004,
                                           IsE0000005, IsE0000006,
                                           IsE0000007, IsE0000008,
                                           IsE0000009, IsE0000010,
                                           IsE0000011, IsE0000012,
                                           IsE0000013, IsE0000014,
                                           IsE0000015)

    # Number of Ensembles
    if _CEI_ != 0:
        ensembles = round(_DeploymentDuration_ * 24 * 3600 / _CEI_)
    else:
        ensembles = 0

    return ensembles * ensembleSize


def _calculate_burst_storage_amount(_CBI_NumEns_,
                                    _CBI_BurstInterval_,
                                    _CWPBN_, _Beams_,
                                    _DeploymentDuration_,
                                    IsE0000001, IsE0000002, IsE0000003,
                                    IsE0000004, IsE0000005, IsE0000006,
                                    IsE0000007, IsE0000008, IsE0000009,
                                    IsE0000010, IsE0000011, IsE0000012,
                                    IsE0000013, IsE0000014, IsE0000015):
    """
    Calculate the amount of storage required from the parameter for the burst deployment.
    Value given in bytes.

    :param _CBI_NumEns_: Number of ensembles in the burst.
    :param _CWPBN_: Number of bins.
    :param _Beams_: Number of beams.
    :param _DeploymentDuration_: Deployment duration.
    :param _CEI_: Time between ensembles.
    :param IsE0000001: Flag if IsE0000001 is enabled.
    :param IsE0000002: Flag if IsE0000002 is enabled.
    :param IsE0000003: Flag if IsE0000003 is enabled.
    :param IsE0000004: Flag if IsE0000004 is enabled.
    :param IsE0000005: Flag if IsE0000005 is enabled.
    :param IsE0000006: Flag if IsE0000006 is enabled.
    :param IsE0000007: Flag if IsE0000007 is enabled.
    :param IsE0000008: Flag if IsE0000008 is enabled.
    :param IsE0000009: Flag if IsE0000009 is enabled.
    :param IsE0000010: Flag if IsE0000010 is enabled.
    :param IsE0000011: Flag if IsE0000011 is enabled.
    :param IsE0000012: Flag if IsE0000012 is enabled.
    :param IsE0000013: Flag if IsE0000013 is enabled.
    :param IsE0000014: Flag if IsE0000014 is enabled.
    :param IsE0000015: Flag if IsE0000015 is enabled.
    :return: Number of bytes required for the given waves deployment.
    """

    # Number of bytes per ensemble
    ensemble_size = _calculate_ensemble_size(_CWPBN_, _Beams_, IsE0000001, IsE0000002, IsE0000003, IsE0000004, IsE0000005,
                                   IsE0000006, IsE0000007, IsE0000008, IsE0000009, IsE0000010, IsE0000011, IsE0000012,
                                   IsE0000013, IsE0000014, IsE0000015)

    # Memory per burst
    burst_mem = _CBI_NumEns_ * ensemble_size

    # Get the number of burst per deployment duration
    # Seconds for the deployment duration
    deployment_dur = _DeploymentDuration_ * 3600.0 * 24.0

    # Divide total duration by burst duration to get number of burst in the deployment
    num_bursts = round(deployment_dur / _CBI_BurstInterval_)

    return burst_mem * num_bursts


def _calculate_ensemble_size(_CWPBN_, _Beams_,
                            IsE0000001, IsE0000002, IsE0000003,
                            IsE0000004, IsE0000005, IsE0000006,
                            IsE0000007, IsE0000008, IsE0000009,
                            IsE0000010, IsE0000011, IsE0000012,
                            IsE0000013, IsE0000014, IsE0000015):
    """
    Calculate the number of bytes for the ensemble based off the parameters.
    Value given in bytes.

    :param _CWPBN_: Number of bins.
    :param _Beams_: Number of beams.
    :param IsE0000001: Flag if IsE0000001 is enabled.
    :param IsE0000002: Flag if IsE0000002 is enabled.
    :param IsE0000003: Flag if IsE0000003 is enabled.
    :param IsE0000004: Flag if IsE0000004 is enabled.
    :param IsE0000005: Flag if IsE0000005 is enabled.
    :param IsE0000006: Flag if IsE0000006 is enabled.
    :param IsE0000007: Flag if IsE0000007 is enabled.
    :param IsE0000008: Flag if IsE0000008 is enabled.
    :param IsE0000009: Flag if IsE0000009 is enabled.
    :param IsE0000010: Flag if IsE0000010 is enabled.
    :param IsE0000011: Flag if IsE0000011 is enabled.
    :param IsE0000012: Flag if IsE0000012 is enabled.
    :param IsE0000013: Flag if IsE0000013 is enabled.
    :param IsE0000014: Flag if IsE0000014 is enabled.
    :param IsE0000015: Flag if IsE0000015 is enabled.
    :return: Number of bytes for the ensemble.
    """

    # E0000001
    E0000001 = 0
    if IsE0000001:
        E0000001 = 4 * (_CWPBN_ * _Beams_ + 7)

    # E0000002
    E0000002 = 0
    if IsE0000002:
        E0000002 = 4 * (_CWPBN_ * _Beams_ + 7)

    # E0000003
    E0000003 = 0
    if IsE0000003:
        E0000003 = 4 * (_CWPBN_ * _Beams_ + 7)

    # E0000004
    E0000004 = 0
    if IsE0000004:
        E0000004 = 4 * (_CWPBN_ * _Beams_ + 7)

    # E0000005
    E0000005 = 0
    if IsE0000005:
        E0000005 = 4 * (_CWPBN_ * _Beams_ + 7)

    # E0000006
    E0000006 = 0
    if IsE0000006:
        E0000006 = 4 * (_CWPBN_ * _Beams_ + 7)

    # E0000007
    E0000007 = 0
    if IsE0000007:
        E0000007 = 4 * (_CWPBN_ * _Beams_ + 7)

    #region E0000008
    E0000008 = 0
    if IsE0000008:
        E0000008 = 4 * (23 + 7)

    # E0000009
    E0000009 = 0
    if IsE0000009:
        E0000009 = 4 * (19 + 7)

    #E0000010
    E0000010 = 0
    if IsE0000010:
        E0000010 = 4 * (14 + 15 * _Beams_ + 7)

    # E0000011
    E0000011 = 0
    if IsE0000011:
        E0000011 = 0

    # E0000012
    E0000012 = 0
    if IsE0000012:
        E0000012 = 4 * (23 + 7)

    # E0000013
    E0000013 = 0
    if IsE0000013:
        E0000013 = 4 * (30 + 7)

    # E0000014
    E0000014 = 0
    if IsE0000014:
        E0000014 = 4 * (23 + 7)

    # E0000015
    E0000015 = 0
    if IsE0000015:
        E0000015 = 4 * (8 * _Beams_ + 1 + 7)

    bytes_per_ensemble = E0000001 + E0000002 + E0000003 + E0000004 + E0000005 + E0000006 + E0000007 + E0000008 + E0000009 + E0000010 + E0000011 + E0000012 + E0000013 + E0000014 + E0000015
    checksum = 4    # Checksum
    wrapper = 32    # Header

    return bytes_per_ensemble + checksum + wrapper


def bytes_2_human_readable(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("!!! numberOfBytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 1
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit