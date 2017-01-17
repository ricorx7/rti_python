
from Ensemble.Ensemble import Ensemble


class WaveEnsemble:
    """
    Ensemble data specific to a wave ensemble.
    This will not need all the data that the entire ensemble will have.
    """

    def __init__(self):
        """
        Initialize the variables.
        """

        """
        Set flag if this data is a vertical ensemble.
        TRUE = Vertical beam ensemble.
        """
        self.is_vertical_sample = False

        """
        WZBM
        Vertical Beam velocity in meters/sec.
        """
        self.vert_beam_vel = []

        """
        WZHS
        Vertical beam height in meters.
        This is the average of all the range tracking values.
        """
        self.vert_beam_height = 0.0

        """
        WPS
        Pressure in meters.
        """
        self.pressure = 0.0

        """
        WTS
        Water temperature in degree fahrenheit.
        """
        self.water_temp = 0.0

        """
        WHG
        Heading in degrees.
        """
        self.heading = 0.0

        """
        WPH
        Pitch in degrees.
        """
        self.pitch = 0.0

        """
        WRL
        Roll in degrees.
        """
        self.roll = 0.0

        """
        WBM
        Beam velocity in m/s.
        [bin, beam]
        """
        self.beam_vel = []

        """
        WTS
        Time stamp in seconds.
        """
        self.time_stamp_seconds = 0.0

        """
        WSHS
        Range Tracking in meters.
        [Beams]
        """
        self.range_tracking = []

        """
        Height source which is derived from the selected height source.
        """
        self.height = 0.0

        """
        Wave sample number.
        A burst will contain x ensembles(samples) in the burst.  This is the number
        of the sample within a burst.
        """
        self.sample_num = 0

        """
        Ensemble number.
        """
        self.ensemble_number = 0

        """
        WUS
        East Velocity data for the given selected bins in m/s.
        [bins]
        """
        self.east_vel = []

        """
        WVS
        North Velocity data for the given selected bins in m/s.
        [bins]
        """
        self.north_vel = []

        """
        WZS
        Vertical velocity data for the given selected bins in m/s.
        """
        self.vertical_vel = []

    def add(self, ens, selected_bins, corr_thresh=0.25):

        # Get the number of beams
        num_beams = 1
        if ens.IsEnsembleData:
            num_beams = ens.EnsembleData.NumBeams

        # Get the number of bins
        num_bins = len(selected_bins)

        # Create enough entries for all the bins or (bins x beams)
        # Initialize with bad values
        for bins in range(num_bins):

            # Vertical Beam velocity
            if ens.IsBeamVelocity and ens.IsCorrelation:
                # Check the correlation against the correlation threshold
                if ens.Correlation[selected_bins[bins], 0] >= corr_thresh:
                    self.vert_beam_vel.append(ens.BeamVelocity[selected_bins[bins], 0])
                else:
                    self.vert_beam_vel.append(Ensemble.BadVelocity)

            # Earth Velocity
            if ens.IsEarthVelocity:
                self.east_vel.append(ens.EarthVelocity[selected_bins[bins], 0])
                self.north_vel.append(ens.EarthVelocity[selected_bins[bins], 1])
                self.vertical_vel.append(ens.EarthVelocity[selected_bins[bins], 2])

            # beam velocity is bin and beams
            bins = []
            for beams in range(num_beams):
                bins.append([Ensemble().BadVelocity])
                self.beam_vel.append(bins)

        if ens.IsRangeTracking:
            self.range_tracking = ens.RangeTracking.Range

