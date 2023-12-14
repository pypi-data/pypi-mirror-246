# coding: utf-8

"""
This is the Main library for the 2.4 GHz band
by Vladimir Fadeev, Dmitrii Boldovsky, Alina Chudaeva, Marat Azizov

"""
from operator import itemgetter
from math import exp as Exp

"""
Signal Strength 	Required for
-30 dBm	Amazing	Max achievable signal strength. The client can only be a few feet from the AP to achieve this. 
            Not typical or desirable in the real world.	N/A
-67 dBm	Very Good	Minimum signal strength for applications that require very reliable, timely delivery of data packets.	
            VoIP/VoWiFi, streaming video
-70 dBm	Okay	Minimum signal strength for reliable packet delivery.	
            Email, web
-80 dBm	Not Good	Minimum signal strength for basic connectivity. Packet delivery may be unreliable.	N/A
-90 dBm	Unusable	Approaching or drowning in the noise floor. Any functionality is highly unlikely.	N/A
"""
MIN_RSSI = -95


def rssi_weigt_calc(cpe_rssi, rssi_fit_coeffs):
    weigt = sum([coeff * (cpe_rssi ** (len(rssi_fit_coeffs) - idx))
                 for idx, coeff in enumerate(rssi_fit_coeffs, 1)])
    if weigt < 0:
        return 0
    else:
        return weigt


def ACI60(radar_channel, data):
    """
    * This function is applicable to 2.4 GHz devices Only! *

    Inputs:
        radar_channel: int
            The Wi-Fi channel of the radar
        data: list of dictionaries
            JSON like data about radar's environment
        rssi_threshold: float
            Threshold in dBm below which RSSI should be counted in formulas
        min_rssi_aci: float
            Threshold in dBm below which device should be excluded from data
    Otputs: 
        IF: float
            Summarized interference factor

    Calculates ACI (Adjascent Channels Interference) impact.

    Standards:  802.11 standard (according to the example below)
                 = 4 for 802.11 a/b/g/n
                 = 3 for 802.11 a/b/g
                 = 2 for 802.11 a/b/
                 = 1 for 802.11  /a
    
    Previous Interference range (IR):
    IR40 = (13.26, 9.21, 7.59, 4.69, 3.84, 0.0)
    (based on Z. Feng and Y. Yang, "How Much Improvement Can We Get From Partially Overlapped Channels?," 
    2008 IEEE Wireless Communications and Networking Conference, 
    Las Vegas, NV, 2008, pp. 2957-2962. )

    IR means maximum distance that the two devices can affect each other (in meters) in this paper.

    New IR was published in 
     - Mishra, A., Shrivastava, V., Banerjee, S. and Arbaugh, W., 2006, June. Partially overlapped channels not considered harmful. 
        In Proceedings of the joint international conference on Measurement and modeling of computer systems (pp. 63-74).

     - V. Shrivastava, S. Rayanchu, J. Yoon, and S. Banerjee, “802.11n under the microscope,” 
        Internet Measurement Conference ’08, 2008. 

     - Mi P., Wang X. Improved channel assignment for WLANs by exploiting partially overlapped channels 
        with novel CIR-based user number estimation 
        //2012 IEEE International Conference on Communications (ICC). – IEEE, 2012. – С. 6591-6595.


    """

    interference_range = (1.0, 0.8, 0.55, 0.35, 0.05)

    if len(list(data)) == 0:
        return 0

    interference_factor = 0
    for cpe in data:

        cpe_rssi = cpe["rssi"]
        if cpe_rssi < MIN_RSSI:
            continue

        cpe_channel = cpe["channel"]
        channel_diff = abs(radar_channel - cpe_channel)
        if channel_diff == 0:
            continue

        if channel_diff >= 5:
            continue

        if cpe.get("associated_devices", None) == 0:
            continue

        interference_range_weight = interference_range[channel_diff]

        """ The following RSSI coefficients are obtained from our experiments 12.09.2020 """
        rssi_fit_coeffs = [-7.13598341e-06, -1.77048688e-03, -1.48576633e-01, -3.27969580e+00]
        rssi_weight = rssi_weigt_calc(cpe_rssi, rssi_fit_coeffs)
        interference_factor += interference_range_weight * (1 - rssi_weight)

    return interference_factor


def CCI60(data, remove_radar=True):
    """CCI60(data)
    Function returns Co-Channel interference factor for channel Ch. 
    Co-channel interference  is one of the two contributors into the 
    overall interference on channel Ch.
    Example:
        data = [{"channel": .., "rssi": .., "bandwidth": .., "standard": .., "type": "R" or "A"}, ...]

    Note: data must not include Radar!

    Fitting function:
    y = Ae^(-B(Ncpe + 1)), 
        where 1 means considered Radar, and Ncpe - weighted by RSSI values number of CPEs that are not considered Radar.
    Exponent coefficients A and B are selected based on CCI experiments (February - March 2020).
    """

    data = list(filter(lambda x: x["rssi"] >= MIN_RSSI and x.get("associated_devices", None) != 0, data))

    A = 1.13566054
    B = 0.1239393

    if len(data) == 0:
        if remove_radar:
            return 1.0
        else:
            return A

    rssis = [x["rssi"] for x in data]

    """ The following RSSI coefficients are obtained from our experiments 12.09.2020 """
    rssi_fit_coeffs = [-2.14672155e-05, - 4.93400956e-03, - 3.80038510e-01, - 9.09719285e+00]
    rssi_weighted_cpes_num = sum([(1 - rssi_weigt_calc(cpe_rssi, rssi_fit_coeffs)) for cpe_rssi in rssis])

    if remove_radar:
        out = A * Exp(-B * (rssi_weighted_cpes_num + 1))
    else:
        out = A * Exp(-B * rssi_weighted_cpes_num)

    return out


def channel_quality(channel, data, remove_radar=True):
    """
    Inputs:
        channel: int
            The Wi-Fi channel of the radar
        data: list of dictionaries
            JSON like data about radar's environment
            E.g. [{"channel": .., "rssi": .., "bandwidth": .., 
                  "standard": .., "type": "R" or "A"}, ...]
        remove_radar: boolean
            exclude or include radar in calculation
        rssi_threshold: int
            The threshold after which RSSI should be taken into account
    Outputs:
        res: float
            The certain channel's quality parameter 

    Returns Channel Quality value for specified channel
    """
    data = [cpe for cpe in data if isinstance(cpe["channel"], int) and cpe["channel"] >= 1]

    # always handle extenders as co-channel interference
    for cpe in data:
        if cpe["type"] == "E":
            cpe["channel"] = channel

    if remove_radar:
        data = list(filter(lambda cpe: cpe.get("type") != "R", data))

    adj_data = list(filter(lambda x: channel != x["channel"], data))
    co_data = list(filter(lambda x: channel == x["channel"], data))

    # ACI
    if len(adj_data) != 0:
        aci_if = ACI60(channel, adj_data)
    else:
        aci_if = 0.0

    # CCI
    if len(co_data) != 0:
        cci_cq = CCI60(co_data, remove_radar=remove_radar)
    else:
        cci_cq = 1.0

    # Resulting value
    res = cci_cq / (1 + aci_if)
    if res > 1.0:
        res = 1.0

    return res


def greedy_calc(radar, environment):
    """
    Inputs:
        radar: dict
            Information about radar
        environment: list of dictionaries
            JSON like data about radar's environment
            E.g. [{"channel": .., "rssi": .., "bandwidth": .., 
                  "standard": .., "type": "R" or "A"}, ...]
    Outputs:
        best_chan: int
            Proposed channel
        best_qual: float
            Proposed channel quality 

    Greedy algorithm to select the best channel for certain radar. 
    """

    ch_quals = [channel_quality(chan, environment)
                for chan in range(1, radar["upper_channel"] + 1)]
    best_chan, best_qual = max(enumerate(ch_quals), key=itemgetter(1))
    best_chan = best_chan + 1
    return best_chan, best_qual


if __name__ == '__main__':
    pass
