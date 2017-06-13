import math
import json
import os
import ADCP.AdcpCommands
import ADCP.Predictor.Range


def calculate_power(**kwargs):
    """
    :param CEI=: Time between ensembles in seconds.
    :param DeploymentDuration=: Deployment length in days.
    :param Beams=: Number of beams for this configuration.
    :param SystemFrequency=: System frequency for this configuration.
    :param CWPON=: Flag if Water Profile is turned on.
    :param CWPBL=: WP Blank in meters.
    :param CWPBS=: WP bin size in meters.
    :param CWPBN=: Number of bins.
    :param CWPBB_LagLength=: WP lag length in meters.
    :param CWPBB=: WP broadband or narrowband.
    :param CWPP=: Number of pings to average.
    :param CWPTBP=: Time between each ping in the average.
    :param CBTON=: Is Bottom Track turned on.
    :param CBTBB=: BT broadband or narrowband.
    :param BeamAngle=: Beam angle in degrees. Default 20 degrees.
    :param SpeedOfSound=: Speed of sound in m/s.  Default 1490m/s
    :param SystemBootPower=: The amount of power required to boot the ADCP in watts.
    :param SystemWakeupTime=: The amount of time to boot the ADCP in seconds.
    :param SystemInitPower=: The amount of power required to initialize the ADCP in watts.
    :param SystemInitTime=: The amount of time to initialize the ADCP in seconds.
    :param BroadbandPower=: Flag if using Broadband power.
    :param SystemSavePower=: The amount of power required to save on the ADCP in watts.
    :param SystemSaveTime=: The amount of time to save on the ADCP in seconds.
    :param SystemSleepPower=: The amount to power required to make the ADCP sleep in watts.
    :param BeamDiameter=: The beam diameter in meters.
    :param CyclesPerElement=: Cycles per element.
    :param CBI=: Flag if we are using Burst Mode pinging.
    :param CBI_NumEns: Number of ensemble in a burst.
    :return: The amount of power required based of the deployment parameters.
    """

    # Get the configuration from the json file
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, 'predictor.json')
    try:
        config = json.loads(open(json_file_path).read())
    except Exception as e:
        print("Error opening predictor.JSON file", e)
        return 0.0

    return _calculate_power( kwargs.pop('CEI', config['DEFAULT']['CEI']),
                            kwargs.pop('DeploymentDuration', config['DEFAULT']['DeploymentDuration']),
                            kwargs.pop('Beams', config['DEFAULT']['Beams']),
                            kwargs.pop('SystemFrequency', config['DEFAULT']['SystemFrequency']),
                            kwargs.pop('CWPON', config['DEFAULT']['CWPON']),
                            kwargs.pop('CWPBL', config['DEFAULT']['CWPBL']),
                            kwargs.pop('CWPBS', config['DEFAULT']['CWPBS']),
                            kwargs.pop('CWPBN', config['DEFAULT']['CWPBN']),
                            kwargs.pop('CWPBB_LagLength', config['DEFAULT']['CWPBB_LagLength']),
                            kwargs.pop('CWPBB', config['DEFAULT']['CWPBB']),
                            kwargs.pop('CWPP', config['DEFAULT']['CWPP']),
                            kwargs.pop('CWPTBP', config['DEFAULT']['CWPTBP']),
                            kwargs.pop('CBTON', config['DEFAULT']['CBTON']),
                            kwargs.pop('CBTBB', config['DEFAULT']['CBTBB']),
                            kwargs.pop('BeamAngle', config["BeamAngle"]),
                            kwargs.pop('SpeedOfSound', config["SpeedOfSound"]),
                            kwargs.pop('SystemBootPower', config["SystemBootPower"]),
                            kwargs.pop('SystemWakeUpTime', config["SystemWakeupTime"]),
                            kwargs.pop('SystemInitPower', config["SystemInitPower"]),
                            kwargs.pop('SystemInitTime', config["SystemInitTime"]),
                            kwargs.pop('BroadbandPower', config["BroadbandPower"]),
                            kwargs.pop('SystemSavePower', config["SystemSavePower"]),
                            kwargs.pop('SystemSaveTime', config["SystemSaveTime"]),
                            kwargs.pop('SystemSleepPower', config["SystemSleepPower"]),
                            kwargs.pop('BeamDiameter', config["BeamDiameter"]),
                            kwargs.pop('CyclesPerElement', config["CyclesPerElement"]))


def calculate_burst_power(**kwargs):
    """
    Calcualte power for a waves burst deployment.  This calculation will calculate power for a single burst.
    Then determine how many bursts are in the deployment.  Then calculate based off the power for a single
    burst and the number of burst to calculate the overall power.

    :param CEI=: Time between ensembles in seconds.
    :param DeploymentDuration=: Deployment length in days.
    :param Beams=: Number of beams for this configuration.
    :param SystemFrequency=: System frequency for this configuration.
    :param CWPON=: Flag if Water Profile is turned on.
    :param CWPBL=: WP Blank in meters.
    :param CWPBS=: WP bin size in meters.
    :param CWPBN=: Number of bins.
    :param CWPBB_LagLength=: WP lag length in meters.
    :param CWPBB=: WP broadband or narrowband.
    :param CWPP=: Number of pings to average.
    :param CWPTBP=: Time between each ping in the average.
    :param CBTON=: Is Bottom Track turned on.
    :param CBTBB=: BT broadband or narrowband.
    :param BeamAngle=: Beam angle in degrees. Default 20 degrees.
    :param SpeedOfSound=: Speed of sound in m/s.  Default 1490m/s
    :param SystemBootPower=: The amount of power required to boot the ADCP in watts.
    :param SystemWakeupTime=: The amount of time to boot the ADCP in seconds.
    :param SystemInitPower=: The amount of power required to initialize the ADCP in watts.
    :param SystemInitTime=: The amount of time to initialize the ADCP in seconds.
    :param BroadbandPower=: Flag if using Broadband power.
    :param SystemSavePower=: The amount of power required to save on the ADCP in watts.
    :param SystemSaveTime=: The amount of time to save on the ADCP in seconds.
    :param SystemSleepPower=: The amount to power required to make the ADCP sleep in watts.
    :param BeamDiameter=: The beam diameter in meters.
    :param CyclesPerElement=: Cycles per element.
    :param CBI=: Flag if we are using Burst Mode pinging.
    :param CBI_NumEns: Number of ensemble in a burst.
    :param CBI_BurstInterval: The length of time in seconds for a burst.
    :return: The amount of power required based of the deployment parameters.
    """

    # Get the configuration from the json file
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, 'predictor.json')
    try:
        config = json.loads(open(json_file_path).read())
    except Exception as e:
        print("Error opening predictor.JSON file", e)
        return 0.0

    return _calculate_burst_power(kwargs.pop('CEI', config['DEFAULT']['CEI']),
                                  kwargs.pop('DeploymentDuration', config['DEFAULT']['DeploymentDuration']),
                                  kwargs.pop('Beams', config['DEFAULT']['Beams']),
                                  kwargs.pop('SystemFrequency', config['DEFAULT']['SystemFrequency']),
                                  kwargs.pop('CWPON', config['DEFAULT']['CWPON']),
                                  kwargs.pop('CWPBL', config['DEFAULT']['CWPBL']),
                                  kwargs.pop('CWPBS', config['DEFAULT']['CWPBS']),
                                  kwargs.pop('CWPBN', config['DEFAULT']['CWPBN']),
                                  kwargs.pop('CWPBB_LagLength', config['DEFAULT']['CWPBB_LagLength']),
                                  kwargs.pop('CWPBB', config['DEFAULT']['CWPBB']),
                                  kwargs.pop('CWPP', config['DEFAULT']['CWPP']),
                                  kwargs.pop('CWPTBP', config['DEFAULT']['CWPTBP']),
                                  kwargs.pop('CBTON', config['DEFAULT']['CBTON']),
                                  kwargs.pop('CBTBB', config['DEFAULT']['CBTBB']),
                                  kwargs.pop('BeamAngle', config["BeamAngle"]),
                                  kwargs.pop('SpeedOfSound', config["SpeedOfSound"]),
                                  kwargs.pop('SystemBootPower', config["SystemBootPower"]),
                                  kwargs.pop('SystemWakeUpTime', config["SystemWakeupTime"]),
                                  kwargs.pop('SystemInitPower', config["SystemInitPower"]),
                                  kwargs.pop('SystemInitTime', config["SystemInitTime"]),
                                  kwargs.pop('BroadbandPower', config["BroadbandPower"]),
                                  kwargs.pop('SystemSavePower', config["SystemSavePower"]),
                                  kwargs.pop('SystemSaveTime', config["SystemSaveTime"]),
                                  kwargs.pop('SystemSleepPower', config["SystemSleepPower"]),
                                  kwargs.pop('BeamDiameter', config["BeamDiameter"]),
                                  kwargs.pop('CyclesPerElement', config["CyclesPerElement"]),
                                  kwargs.pop('CBI', config["DEFAULT"]["CBI"]),
                                  kwargs.pop('CBI_BurstInterval', config["DEFAULT"]["CBI_BurstInterval"]),
                                  kwargs.pop('CBI_NumEns', config["DEFAULT"]["CBI_NumEns"]))


def calculate_number_batteries(**kwargs):
    """
    Calculate the number of batteries based off the power usage and deployment duration.  This will also take into
    account the derate of the battery.

    :param PowerUsage=: Power usage for the deployment in watt/hr
    :param DeploymentDuration=: Length of the deployment in days.
    :param BatteryCapacity=: Total battery capactiy for a single battery in watt/hr
    :param BatteryDerate=: Derate of the battery in watt/hr
    :param BatterySelf_discharge=: Self discharge of the battery over a year in watt/hr
    :return:
    """

    # Get the configuration from the json file
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, 'predictor.json')
    try:
        config = json.loads(open(json_file_path).read())
    except Exception as e:
        print("Error opening predictor.JSON file", e)
        return 0.0
    
    return _calculate_number_batteries(kwargs.pop('PowerUsage', 0.0),
                                       kwargs.pop('DeploymentDuration', config['DEFAULT']['DeploymentDuration']),
                                       kwargs.pop('BatteryCapacity', config['DEFAULT']['BatteryCapacity']),
                                       kwargs.pop('BatteryDerate', config['DEFAULT']['BatteryDerate']),
                                       kwargs.pop('BatterySelfDischarge', config['DEFAULT']['BatterySelfDischarge']))


def _calculate_power(_cei_, _deployment_duration_, _beams_, _system_frequency_,
                   _cwpon_, _cwpbl_, _cwpbs_, _cwpbn_, _cwpbb_lag_length_, _cwpbb_transmit_pulse_type_,
                   _cwpp_, _cwptbp_,
                   _cbton_, _cbtbb_transmit_pulse_type_,
                   _beam_angle_, _speed_of_sound_,
                   _system_boot_power_, _system_wakeup_time_, _system_init_power_, _system_init_time_,
                   _broadband_power_, _system_save_power_, _system_save_time_, _system_sleep_power_,
                   _beam_diameter_, _cycles_per_element_, _is_burst_=False, _ensembles_per_burst_=0):
    """
    Calculate the power using based off the deployment parameters.  This will give the total power consumed
    of an ADCP for the given parameters.  You can then divide this by the battery total to get the number
    batteries required for a deployment.

    All values with underscores before and after the name are given variables by the user.  All caps
    variables are given by the JSON configuration.  All other variables are calculated.

    :param _cei_: Time between ensembles in seconds.
    :param _deployment_duration_: Deployment length in days.
    :param _beams_: Number of beams for this configuration.
    :param _system_frequency_: System frequency for this configuration.
    :param _cwpon_: Flag if Water Profile is turned on.
    :param _cwpbl_: WP Blank in meters.
    :param _cwpbs_: WP bin size in meters.
    :param _cwpbn_: Number of bins.
    :param _cwpbb_lag_length_: WP lag length in meters.
    :param _cwpbb_transmit_pulse_type_: WP broadband or narrowband.
    :param _cwpp_: Number of pings to average.
    :param _cwptbp_: Time between each ping in the average.
    :param _cbton_: Is Bottom Track turned on.
    :param _cbtbb_transmit_pulse_type_: BT broadband or narrowband.
    :param _beam_angle_: Beam angle in degrees. Default 20 degrees.
    :param _speed_of_sound_: Speed of sound in m/s.  Default 1490m/s
    :param _system_boot_power_: The amount of power required to boot the ADCP in watts.
    :param _system_wakeup_time_: The amount of time to boot the ADCP in seconds.
    :param _system_init_power_: The amount of power required to initialize the ADCP in watts.
    :param _system_init_time_: The amount of time to initialize the ADCP in seconds.
    :param _broadband_power_: Flag if using Broadband power.
    :param _system_save_power_: The amount of power required to save on the ADCP in watts.
    :param _system_save_time_: The amount of time to save on the ADCP in seconds.
    :param _system_sleep_power_: The amount to power required to make the ADCP sleep in watts.
    :param _beam_diameter_: The beam diameter in meters.
    :param _cycles_per_element_: Cycles per element.
    :param _is_burst_: Flag if we are using Burst Mode pinging.
    :param _ensembles_per_burst_: Number of ensemble in a burst.
    :return: The amount of power required based of the deployment parameters.
    """

    # Get the configuration from the json file
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, 'predictor.json')

    try:
        config = json.loads(open(json_file_path).read())
    except Exception as e:
        print("Error opening predictor.JSON file", e)
        return 0.0

    # Get the configuration from the json file
    config = json.loads(open(json_file_path).read())


    # Number of Ensembles
    # Check for divide by 0
    num_ensembles = 0
    if _cei_ == 0:
        num_ensembles = 0
    else:
        # Convert deployment duration to seconds
        # Then divide by time per ensemble which is in seconds
        num_ensembles = round((_deployment_duration_ * 24.0 * 3600.0) / _cei_)

    # If this is a burst, then give the power for a burst.
    if _is_burst_:
        num_ensembles = _ensembles_per_burst_


    # Wakeups  (Question about CEI)
    wakeups = 1
    if _cei_ > 1.0:
        if _cwptbp_ > 1.0:
            wakeups = num_ensembles * _cwpp_
        else:
            wakeups = num_ensembles


    # Bottom Track Pings
    bottom_track_pings = 0.0
    if _cbton_:
        value = _cwpp_ / 10.0
        if value < 1:
            bottom_track_pings = num_ensembles
        else:
            bottom_track_pings = round(_cwpp_ / 10.0) * num_ensembles


    # Bottom Track Time
    bottom_track_range = ADCP.Predictor.Range._calculate_predicted_range(_cwpon_, _cwpbb_transmit_pulse_type_, _cwpbs_, _cwpbn_, _cwpbl_, _cbton_, _cbtbb_transmit_pulse_type_, _system_frequency_, _beam_diameter_, _cycles_per_element_, _beam_angle_, _speed_of_sound_, _cwpbb_lag_length_, _broadband_power_)[0]
    bottom_track_time = 0.0015 * bottom_track_range


    # Transmit Power Bottom Track
    # double beam_xmt_power_bottom_track = XmtW_1200000 + XmtW_600000 + XmtW_300000 + XmtW_150000 + XmtW_75000 + XmtW_38000;
    beam_xmt_power_bottom_track = 0.0;
    # 1200khz
    if _system_frequency_ > config["DEFAULT"]["1200000"]["FREQ"]:
        beam_xmt_power_bottom_track = config["DEFAULT"]["1200000"]["XMIT_W"]

    # 600khz
    if (_system_frequency_ > config["DEFAULT"]["600000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["1200000"]["FREQ"]):
        beam_xmt_power_bottom_track = config["DEFAULT"]["600000"]["XMIT_W"]

    # 300khz
    if (_system_frequency_ > config["DEFAULT"]["300000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["600000"]["FREQ"]):
        beam_xmt_power_bottom_track = config["DEFAULT"]["300000"]["XMIT_W"]

    # 150khz
    if (_system_frequency_ > config["DEFAULT"]["150000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["300000"]["FREQ"]):
        beam_xmt_power_bottom_track = config["DEFAULT"]["150000"]["XMIT_W"]

    # 75khz
    if (_system_frequency_ > config["DEFAULT"]["75000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["150000"]["FREQ"]):
        beam_xmt_power_bottom_track = config["DEFAULT"]["75000"]["XMIT_W"]

    # 38khz
    if (_system_frequency_ > config["DEFAULT"]["38000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["75000"]["FREQ"]):
        beam_xmt_power_bottom_track = config["DEFAULT"]["38000"]["XMIT_W"]


    # Bottom Track Transmit Power
    bt_transmit_power = bottom_track_pings * 0.2 * (bottom_track_time * beam_xmt_power_bottom_track * _beams_) / 3600.0


    # Bottom Track Receiver Power
    freq_mult = 1
    if _system_frequency_ > 600000.0:
        freq_mult = 2

    bt_receive_power = bottom_track_pings * (bottom_track_time * _system_boot_power_) / 3600.0 * freq_mult


    # Wakeup Power
    wakeup_power = wakeups * _system_wakeup_time_ * _system_boot_power_ / 3600.0


    # Init Power
    init_power = wakeups * _system_init_power_ * _system_init_time_ / 3600.0


    # Sample Rate
    sum_sampling = 0.0

    if _system_frequency_ > config["DEFAULT"]["1200000"]["FREQ"]:                                                                           # 1200khz
        sum_sampling += config["DEFAULT"]["1200000"]["SAMPLING"] * config["DEFAULT"]["1200000"]["CPE"] / _cycles_per_element_
    elif (_system_frequency_ > config["DEFAULT"]["600000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["1200000"]["FREQ"]):        # 600khz
        sum_sampling += config["DEFAULT"]["600000"]["SAMPLING"] * config["DEFAULT"]["600000"]["CPE"] / _cycles_per_element_
    elif (_system_frequency_ > config["DEFAULT"]["300000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["600000"]["FREQ"]):         # 300khz
        sum_sampling += config["DEFAULT"]["300000"]["SAMPLING"] * config["DEFAULT"]["300000"]["CPE"] / _cycles_per_element_
    elif (_system_frequency_ > config["DEFAULT"]["150000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["300000"]["FREQ"]):         # 150khz
        sum_sampling += config["DEFAULT"]["150000"]["SAMPLING"] * config["DEFAULT"]["150000"]["CPE"] / _cycles_per_element_
    elif (_system_frequency_ > config["DEFAULT"]["75000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["150000"]["FREQ"]):          # 75khz
        sum_sampling += config["DEFAULT"]["75000"]["SAMPLING"] * config["DEFAULT"]["75000"]["CPE"] / _cycles_per_element_
    elif (_system_frequency_ > config["DEFAULT"]["38000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["75000"]["FREQ"]):           # 38khz
        sum_sampling += config["DEFAULT"]["38000"]["SAMPLING"] * config["DEFAULT"]["38000"]["CPE"] / _cycles_per_element_

    sample_rate = _system_frequency_ * sum_sampling


    # Meters Per Sample
    # Check for divide by 0
    meters_per_sample = 0
    if sample_rate == 0:
        meters_per_sample = 0.0
    else:
        meters_per_sample = math.cos(_beam_angle_ / 180.0 * math.pi) * _speed_of_sound_ / 2.0 / sample_rate


    # Bin Samples
    # Check for divide by 0
    bin_samples = 0
    if meters_per_sample == 0:
        bin_samples = 0;
    else:
        bin_samples = math.trunc(_cwpbs_ / meters_per_sample)


    # Bin Time
    bin_time = 1
    # Check for divide by 0
    if sample_rate == 0:
        bin_time = 0
    else:
        bin_time = bin_samples / sample_rate


    # Lag Samples
    # Check for divide by 0
    lag_samples = 0
    if meters_per_sample == 0:
        lag_samples = 0
    else:
        lag_samples = 2 * math.trunc((math.trunc(_cwpbb_lag_length_ / meters_per_sample) + 1.0) / 2.0)


    # Code Repeats
    code_repeats = 0;
    # Check for divide by 0
    if lag_samples == 0:
        code_repeats = 0

    # Cased BinSamples and LagSamples to double because Truncate only takes doubles
    # Make the result of Truncate an int
    if (math.trunc(bin_samples / lag_samples)) + 1.0 < 2.0:
        code_repeats = 2
    else:
        code_repeats = (math.trunc(bin_samples / lag_samples)) + 1


    # Lag Time
    # Check for divide by 0
    lag_time = 0.0
    if sample_rate == 0:
        lag_time = 0.0
    else:
        lag_time = lag_samples / sample_rate


    # Transmit Code Time
    transmit_code_time = 1
    # If using Broadband
    if _cwpbb_transmit_pulse_type_ == ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value:
        if code_repeats < 3:
            transmit_code_time = 2.0 * bin_time
        else:
            transmit_code_time = code_repeats * lag_time
    else:
        if _cwpbb_transmit_pulse_type_ == ADCP.AdcpCommands.eCWPBB_TransmitPulseType.NARROWBAND.value:
            transmit_code_time = bin_time
        else:
            transmit_code_time = 2.0 * bin_time


    # Transmit Scale
    xmt_scale = 0.0
    if _cwpbb_transmit_pulse_type_ == ADCP.AdcpCommands.eCWPBB_TransmitPulseType.NARROWBAND.value:          # Checck if NB
        xmt_scale = 1.0
    else:
        # Check for bad value
        if lag_samples == 0:
            xmt_scale = 0.0

    # Check which Broadband power is used
    if _broadband_power_:
        xmt_scale = (lag_samples - 1.0) / lag_samples
    else:
        xmt_scale = 1.0 / lag_samples


    # Transmit Watt
    # Get the sum of all the selected XmtW
    sum_xmt_w = 0.0;

    if _system_frequency_ > config["DEFAULT"]["1200000"]["FREQ"]:                                                                       # 1200khz
        sum_xmt_w = config["DEFAULT"]["1200000"]["XMIT_W"]
    if (_system_frequency_ > config["DEFAULT"]["600000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["1200000"]["FREQ"]):      # 600khz
        sum_xmt_w = config["DEFAULT"]["600000"]["XMIT_W"]
    if (_system_frequency_ > config["DEFAULT"]["300000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["600000"]["FREQ"]):       # 300khz
        sum_xmt_w = config["DEFAULT"]["300000"]["XMIT_W"]
    if (_system_frequency_ > config["DEFAULT"]["150000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["300000"]["FREQ"]):       # 150khz
        sum_xmt_w = config["DEFAULT"]["150000"]["XMIT_W"]
    if (_system_frequency_ > config["DEFAULT"]["75000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["150000"]["FREQ"]):        # 75khz
        sum_xmt_w = config["DEFAULT"]["75000"]["XMIT_W"]
    if (_system_frequency_ > config["DEFAULT"]["38000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["75000"]["FREQ"]):         # 38khz
        sum_xmt_w = config["DEFAULT"]["38000"]["XMIT_W"]


    # Beam Transmit Power Profile
    beam_xmt_power_profile = xmt_scale * sum_xmt_w


    # Transmit Power
    transmit_power = (transmit_code_time * beam_xmt_power_profile * _beams_ * num_ensembles * _cwpp_) / 3600.0


    # Time Between Pings
    time_between_pings = 0.0
    # Check for divide by 0
    if sample_rate == 0:
        time_between_pings = 0
    elif _cwpp_ == 1:
        # If there is only 1 ping, then there is no time between pings.
        time_between_pings = 0
    elif _cwpbn_ * bin_samples / sample_rate > _cwptbp_:
        time_between_pings = _cwpbn_ * bin_samples / sample_rate
    else:
        time_between_pings = _cwptbp_


    # Receive Time
    receive_time = 0.0
    # Check for divide by 0
    if sample_rate == 0:
        receive_time = time_between_pings
    elif _cwpp_ == 1: # If only 1 ping
        receive_time = _cwpbn_ * bin_samples / sample_rate
    elif time_between_pings > 1.0: # Or CWPP > 1 and Time Between Pings is greater 1, sleeping between pings
        # Sleep between pings
        receive_time = _cwpbn_ * bin_samples / sample_rate
    else:
        # No sleeping between pings
        receive_time = time_between_pings


    # Receive Power
    system_rcv_power = 3.80
    if _beams_ == 4:
        system_rcv_power = 3.8 # 1200khz 4Beam system test result
    elif _beams_ == 5:
        system_rcv_power = 4.30 # 600 / 600khz 5Beam system test result
    elif _beams_ >= 7:
        system_rcv_power = 5.00 # 300 / 1200khz 8Beam system test result, 7Beam taken from waves model

    receive_power = 0.0
    freq_mult_rcv_pwr = 1
    if _system_frequency_ > 700000.0:
        freq_mult_rcv_pwr = 2

    receive_power = (receive_time * system_rcv_power * num_ensembles * _cwpp_) / 3600.0 * freq_mult_rcv_pwr


    # Save Power
    save_power = (wakeups * _system_save_power_ * _system_save_time_) / 3600.0


    # Sleep Power
    sleep_power = _system_sleep_power_ * _deployment_duration_ * 24.0


    # Transmit Voltage
    # Sum up the Xmt Voltage
    sum_xmt_v = 0.0

    if _system_frequency_ > config["DEFAULT"]["1200000"]["FREQ"]:                                                                           # 1200khz
        sum_xmt_v = config["DEFAULT"]["1200000"]["XMIT_V"]
    elif (_system_frequency_ > config["DEFAULT"]["600000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["1200000"]["FREQ"]):        # 600khz
        sum_xmt_v = sum_xmt_v = config["DEFAULT"]["600000"]["XMIT_V"]
    elif (_system_frequency_ > config["DEFAULT"]["300000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["600000"]["FREQ"]):         # 300khz
        sum_xmt_v = sum_xmt_v = config["DEFAULT"]["300000"]["XMIT_V"]
    elif (_system_frequency_ > config["DEFAULT"]["150000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["300000"]["FREQ"]):         # 150khz
        sum_xmt_v = sum_xmt_v = config["DEFAULT"]["150000"]["XMIT_V"]
    elif (_system_frequency_ > config["DEFAULT"]["75000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["150000"]["FREQ"]):          # 75khz
        sum_xmt_v = sum_xmt_v = config["DEFAULT"]["75000"]["XMIT_V"]
    elif (_system_frequency_ > config["DEFAULT"]["38000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["75000"]["FREQ"]):           # 38khz
        sum_xmt_v = sum_xmt_v = config["DEFAULT"]["38000"]["XMIT_V"]


    # Leakage
    # Sum up the Leakage
    sum_leakage_ua = 0.0;

    if _system_frequency_ > config["DEFAULT"]["1200000"]["FREQ"]:                                                                           # 1200khz
        sum_leakage_ua = 3.0 * math.sqrt(2.0 * 0.000001 * config["DEFAULT"]["1200000"]["UF"] * config["DEFAULT"]["1200000"]["XMIT_V"])
    if (_system_frequency_ > config["DEFAULT"]["600000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["1200000"]["FREQ"]):          # 600khz
        sum_leakage_ua = 3.0 * math.sqrt(2.0 * 0.000001 * config["DEFAULT"]["600000"]["UF"] * config["DEFAULT"]["600000"]["XMIT_V"])
    if (_system_frequency_ > config["DEFAULT"]["300000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["600000"]["FREQ"]):           # 300khz
        sum_leakage_ua = 3.0 * math.sqrt(2.0 * 0.000001 * config["DEFAULT"]["300000"]["UF"] * config["DEFAULT"]["300000"]["XMIT_V"])
    if (_system_frequency_ > config["DEFAULT"]["150000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["300000"]["FREQ"]):           # 150khz
        sum_leakage_ua = 3.0 * math.sqrt(2.0 * 0.000001 * config["DEFAULT"]["150000"]["UF"] * config["DEFAULT"]["150000"]["XMIT_V"])
    if (_system_frequency_ > config["DEFAULT"]["75000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["150000"]["FREQ"]):            # 75khz
        sum_leakage_ua = 3.0 * math.sqrt(2.0 * 0.000001 * config["DEFAULT"]["75000"]["UF"] * config["DEFAULT"]["75000"]["XMIT_V"])
    if (_system_frequency_ > config["DEFAULT"]["38000"]["FREQ"]) and (_system_frequency_ < config["DEFAULT"]["75000"]["FREQ"]):             # 38khz
        sum_leakage_ua = 3.0 * math.sqrt(2.0 * 0.000001 * config["DEFAULT"]["38000"]["UF"] * config["DEFAULT"]["38000"]["XMIT_V"])


    # Cap Charge Power
    cap_charge_power = 0.03 * (bt_transmit_power + transmit_power) + 1.3 * _deployment_duration_ * 24.0 * sum_xmt_v * 0.000001 * sum_leakage_ua


    return bt_transmit_power + bt_receive_power + wakeup_power + init_power + transmit_power + receive_power + save_power + sleep_power + cap_charge_power



def _calculate_burst_power(_cei_, _deployment_duration_, _beams_, _system_frequency_,
                           _cwpon_, _cwpbl_, _cwpbs_, _cwpbn_, _cwpbb_lag_length_, _cwpbb_transmit_pulse_type_,
                           _cwpp_, _cwptbp_,
                           _cbton_, _cbtbb_transmit_pulse_type_,
                           _beam_angle_, _speed_of_sound_,
                           _system_boot_power_, _system_wakeup_time_, _system_init_power_, _system_init_time_,
                           _broadband_power_, _system_save_power_, _system_save_time_, _system_sleep_power_,
                           _beam_diameter_, _cycles_per_element_, _is_burst_=True, _burst_interval_=3600, _ensembles_per_burst_=4096):
    """
    Calcualte power for a waves burst deployment.  This calculation will calculate power for a single burst.
    Then determine how many bursts are in the deployment.  Then calculate based off the power for a single
    burst and the number of burst to calculate the overall power.

    Calculate the power using based off the deployment parameters.  This will give the total power consumed
    of an ADCP for the given parameters.  You can then divide this by the battery total to get the number
    batteries required for a deployment.

    All values with underscores before and after the name are given variables by the user.  All caps
    variables are given by the JSON configuration.  All other variables are calculated.

    :param _cei_: Time between ensembles in seconds.
    :param _deployment_duration_: Deployment length in days.
    :param _beams_: Number of beams for this configuration.
    :param _system_frequency_: System frequency for this configuration.
    :param _cwpon_: Flag if Water Profile is turned on.
    :param _cwpbl_: WP Blank in meters.
    :param _cwpbs_: WP bin size in meters.
    :param _cwpbn_: Number of bins.
    :param _cwpbb_lag_length_: WP lag length in meters.
    :param _cwpbb_transmit_pulse_type_: WP broadband or narrowband.
    :param _cwpp_: Number of pings to average.
    :param _cwptbp_: Time between each ping in the average.
    :param _cbton_: Is Bottom Track turned on.
    :param _cbtbb_transmit_pulse_type_: BT broadband or narrowband.
    :param _beam_angle_: Beam angle in degrees. Default 20 degrees.
    :param _speed_of_sound_: Speed of sound in m/s.  Default 1490m/s
    :param _system_boot_power_: The amount of power required to boot the ADCP in watts.
    :param _system_wakeup_time_: The amount of time to boot the ADCP in seconds.
    :param _system_init_power_: The amount of power required to initialize the ADCP in watts.
    :param _system_init_time_: The amount of time to initialize the ADCP in seconds.
    :param _broadband_power_: Flag if using Broadband power.
    :param _system_save_power_: The amount of power required to save on the ADCP in watts.
    :param _system_save_time_: The amount of time to save on the ADCP in seconds.
    :param _system_sleep_power_: The amount to power required to make the ADCP sleep in watts.
    :param _beam_diameter_: The beam diameter in meters.
    :param _cycles_per_element_: Cycles per element.
    :param _is_burst_: Flag if we are using Burst Mode pinging.
    :param _ensembles_per_burst_: Number of ensemble in a burst.
    :param _burst_interval_: The length of time in seconds of a burst.
    :return: The amount of power required based of the deployment parameters.
    """

    # Calculate the amount it takes to do 1 burst
    # Set the deployment duration to 1 day
    burst_pwr = _calculate_power(_cei_,
                                 1,                                                      # Set the duration to 1 day
                                _beams_, _system_frequency_,
                                _cwpon_, _cwpbl_, _cwpbs_, _cwpbn_,
                                _cwpbb_lag_length_, _cwpbb_transmit_pulse_type_,
                                _cwpp_, _cwptbp_,
                                _cbton_, _cbtbb_transmit_pulse_type_,
                                _beam_angle_,
                                _speed_of_sound_,
                                _system_boot_power_,
                                _system_wakeup_time_,
                                _system_init_power_,
                                _system_init_time_,
                                _broadband_power_,
                                _system_save_power_,
                                _system_save_time_,
                                _system_sleep_power_,
                                _beam_diameter_,
                                _cycles_per_element_,
                                _is_burst_, _ensembles_per_burst_)

    # Get the number of burst per deployment duration
    deployment_dur = _deployment_duration_ * 3600 * 24
    num_burst = round(deployment_dur / _burst_interval_)

    return burst_pwr * num_burst


def _calculate_number_batteries(_power_usage_, _deployment_duration, _battery_capacity_, _battery_derate_, _battery_self_discharge_):
    """
    Calculate the number of batteries based off the power usage and deployment duration.  This will also take into
    account the derate of the battery.
    :param _power_usage_: Power usage for the deployment in watt/hr
    :param _deployment_duration: Length of the deployment in days.
    :param _battery_capacity_: Total battery capactiy for a single battery in watt/hr
    :param _battery_derate_: Derate of the battery in watt/hr
    :param _battery_self_discharge_: Self discharge of the battery over a year in watt/hr
    :return:
    """

    # Current battery power available from a single battery
    battery_pwr = _battery_capacity_ * _battery_derate_ - _battery_self_discharge_ * _deployment_duration / 365.0

    return _power_usage_ / battery_pwr