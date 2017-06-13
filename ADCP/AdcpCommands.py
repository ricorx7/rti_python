from enum import Enum


class eCWPBB_TransmitPulseType(Enum):
    """
    Enum used to select the different transmit pulse types.
    """

    """
    (0) Non-Coded Narrowband.
     Provides long range profiles at the expense of variance.
     Not recommended for use with bin size less than the default
     bin size.

     Long Range but noisy data.  Usually take multiple pings and average
     them together.

     |---------------------------------|~
     |       o  o             o o      |  ~
     |     o      o          o    o    |    ~
     |   o           o     o        o  |      ~
     | o               o o            o|        ~
                Pulse Transmit             Receive Signal
               100% Carrier Cycle            Amplitude
     |-------------Bin Size------------|
     |-----------Transmit Length-------|
    """
    NARROWBAND = 0

    """
    /// (1) Coded Broadband.
    /// Typically 15% less range than narrow band but has greatly reduced
    /// variance (depending on lag length).
    /// Used in conjunction with CWPBP for small bins.
    /// 
    /// Shorter Range but clean data.
    /// 
    /// Broaband signal is a signal with modulation(phase changes).
    /// 
    /// |--|               |--|~
    /// |  |               |  |  ~
    /// |  |               |  |    ~     
    /// |  |               |  |      ~      ~    ~
    /// |  |_______________|  |        ~~~~~  ~~~  ~~
    /// 
    /// |----Lag Length----|
    /// 
    /// Lag Length or bin size, which ever is greater.
    /// 
    /// |---------------------------------------------------------| 
    /// |       o  o             o o         o o          o o     |
    /// |     o      o          o    o      o    o       o    o   |
    /// |   o           o     o        o   o       o    o       o |
    /// | o               o o            o           o o         o| 
    ///                                  |
    ///                             Phase Change
    /// |-----------------------Coded Element---------------------|
    /// 
    ///                        2 Carrier cycles
    ///                           BandWidth = 50%   
    ///                     BandWidth = 1 / # carrier cycles
    ///                        
    /// NB BandWidth: # carrier cycles in the pulse.
    /// BB BandWidth: # carrier cycles within a coded element.
    /// 
    /// 
    /// But with just 2 pulses it is not a lot of energy in the water.  Which limits the 
    /// profile range.  So more coded elements are put in the water to fill the gap between
    /// the lag length.  The group of coded elements for the first pulse are then repeated 
    /// a second time for the second pulse.  
    /// 
    /// 
    /// ||--||--|--|--|--||--||--|--|--|--|~
    /// ||  ||  |  |  |  ||  ||  |  |  |  |  ~
    /// || 0|| 1| 1| 0| 1|| 0|| 1| 1| 0| 1|    ~     
    /// ||  ||  |  |  |  ||  ||  |  |  |  |      ~      ~    ~
    /// ||  ||  |  |  |  ||  ||  |  |  |  |      ~~~~~  ~~~  ~~
    /// |-- Lag Length --|     
    /// 
    /// Wait for both groups of coded elements are sent out before looking at the receive data.  Then check the correlation between the 2 coded element groups.
    /// 
    /// Coded element groups are created with a pseudo random generator.
    /// BT uses M Sequence to generate the random code.  Bottom Track has a hard target so correlation is 100%. M Sequence good with 100% correlation.
    /// WP uses Barker Code to generate the random code.  Water Profile pulses interfere with each other so correlation is 50%.  So Barker Code is better to use.
    /// 
    /// Broadband             o 
    ///                     o   o
    ///                    o     o
    ///                   o       o
    ///                  o         o
    ///                 o           o
    ///        o o     o             o     o o
    ///  o o  o   o   o               o   o   o   o o
    /// o   o      o o                 o o     o o    o
    /// 
    /// Narrowband            o
    ///                      o o
    ///                     o   o
    ///                 o  o     o  o 
    ///                o oo       oo o
    /// 
    /// |------------------Frequency -----------------|
    /// 
    """
    BROADBAND = 1

    """
    /// (2) Non-Coded Pulse-To-Pulse.
    /// Narrowband and provides ultra low variance for small bin sizes.
    /// Non-coded has slightly higher variance than the coded
    /// transmit without the annoying autocorrelation side peaks.
    /// 
    /// Shallow water where blank can effect the measurement.  Measurements
    /// that need to be close to the instrument.  
    /// 
    /// Non-coded elements will work better because coded elements in small bins cause variance.
    /// 
    /// Normal processing will send out at least 2 pulses before processing the
    /// return information.  In shallower water, the return of the shallow depths would
    /// be lost.  In Pulse-to-Pulse, the First pulse is sent and then immediately listened
    /// to so it can see the shallower depths.  It then send out another pulse and the listens
    /// immediately.  The to pulses should have the same return to get good correlation (100%).
    /// But if the water is moving to fast, the pulses will not match and the correlation will
    /// be low.  
    /// 
    /// By processing earlier we can also have a smaller blank.  
    /// 
    /// One drawback is you can only receive data for the length of the lag.  After the lag, the
    /// next pulse will be sent out.  This limits the profile range.
    /// 
    /// PtoP 1st Bin Pos = Blank + (Xmt + BinSize)/2
    /// BB   1st Bin Pos = Blank + (Xmt + BinSize + Lag)/2
    /// 
    /// Xmt is the pulse.
    /// The lag is the length(time) needed to wait for both pulses to transmitted.
    /// 
    /// All the data (bins) processed within the lag length should have a 100%
    /// correlation.  Anything beyond the lag length will also include the second pulse
    /// and cause the correlation to drop to at least 50%.  The bins can still be seen but
    /// the data will not be as reliable.
    /// 
    /// |----|~         |----|~
    /// |    |  ~       |    |  ~
    /// |    |    ~     |    |    ~ 
    /// |    |      ~   |    |      ~
    /// |    |        ~ |    |        ~
    /// Pulse 1        Pulse 2
    ///      |BIN|.|BIN|......|BIN|
    ///      |-  100% -||-  50%  -|
    ///          Correlation
    /// 
    /// For Non-Coded PtoP, within the Pulse is a signal at the bandwidth.
    /// For BB PtoP, within the Pulse is a coded element (signal with modulation(phase changes)).
    /// 
    """
    NONCODED_PULSE_TO_PULSE = 2

    """
    /// (3) Broadband Pulse-To-Pulse. (no ambuguity resolver).
    /// Provides ultra low variance for small bin sizes.  Coded 
    /// has slightly lower variance than the non-coded transmit.
    /// 
    /// Shallow water where blank can effect the measurement.  Measurements
    /// that need to be close to the instrument.
    /// 
    /// Coded elements in small bins cause variance due to side peaks so not as good for really small bins sizes.
    /// 
    """
    BROADBAND_PULSE_TO_PULSE = 3

    """
    /// (4) Non Coded Broadband Pulse-To-Pulse. (no ambuguity resolver).
    /// Narrowband and provides ultra low variance for small bin sizes.  Coded 
    /// has slightly lower variance than the non-coded transmit.
    """
    NONCODED_BROADBAND_PULSE_TO_PULSE = 4

    """
    /// Broadband with ambuguity resolver ping.
    /// Used in conjunction with CWPBP.
    /// 
    /// Make lower variance measurements at a higher velocity.
    /// 
    /// Ambiguity Resolver is not perfect.
    /// 
    ///     / \         / \        */ \         / \
    ///    /  \       /   \       /   \       /   \
    ///   /   \    0/     \     /     \     /     \
    ///  /    \   /       \   /       \   /       \
    /// /     \ /         \/         \ /         \
    ///        |          |
    ///      -0.21m/s   0.21m/s 
    ///        | 1 Cycle  | 
    /// 
    /// 
    /// 
    /// Figure out how many times it went around the cycle.
    /// 
    /// * = 0.21(at least 1 cycle) + 0.18(mostly towards the top) = 0.39m/s
    /// 
    """
    BROADBAND_AMBIGUITY_RESOLVER = 5

    """
    /// Broadband pulse to pulse with ambiguity resolver ping.
    /// Used in conjunction with CWPAP.
    """
    BROADBAND_P2P_AMBIGUITY_RESOLVER = 6


class eCBTBB_Mode(Enum):
    """
    Bottom Track Mode.
    """

    """
    (0) Narrowband Long Range
    """
    NARROWBAND_LONG_RANGE = 0

    """
    (1) Coded Broadband Transmit.
    """
    BROADBAND_CODED = 1

    """
    (2) Broadband Non-coded Transmit.
    """
    BROADBAND_NON_CODED = 2

    """
    (3) NA.
    """
    NA_3 = 3

    """
    (4) Broadband Non-coded Pulse to Pulse
    """
    BROADBAND_NON_CODED_P2P = 4

    """
    (5) NA.
    """
    NA_5 = 5

    """
    (6) NA.
    """
    NA_6 = 6

    """
    (7) Auto switch between Narrowband, Broadband Non-Coded and Broadband Non-Coded Pulse to Pulse.
    """
    AUTO_SWITCH_NARROWBAND_BB_NONCODED_BB_NONCODED_P2P = 7

