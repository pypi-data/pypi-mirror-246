#!/usr/bin/env python
# coding: utf-8
"""
Created on Fri Jun  1 17:16:15 2018
Edited on Thu May 28 2020

@authors: D, Vladimir Fadeev
"""
import ch_5G as ch_5G
from math import exp as Exp

RSSI_LIMIT = -95
USABLE_BW = (20, 40, 80)


class EmptyPossibleChannels(Exception):
    """Exception raised if no possible channels.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def channel_quality(ch, data, bw, rch, remove_radar=True):
    """
    This function counts channel quality

    :param ch: int - channel Radar operating on
    :param data: List[dict] - in format
        [{"channel": 42, "rssi": -119, "standard": 4, "type": "R" or "A"}, ..],
        where "channel": channel device operating on, rssi - value of RSSI,
        type: "R" for Radar, "A" for Alien
    :param bw: int - Radar's bandwidth
    :param remove_radar: bool - should be or should not be removed radar from calculations
    :return: ch_q: float - channel quality
    """

    if remove_radar:
        data = list(filter(lambda cpe: cpe.get("type") != "R", data))

    data = list(filter(lambda cpe: cpe.get("associated_devices", None) != 0, data))

    if len(data) == 0:
        return 1.0

    P0 = -46  # dBm (RSSI at the reference distance (1m))

    if bw != 20:
        ch = ch_5G.ch_map[bw].get(ch, ch)

    data = list(filter(lambda x: x["rssi"] >= RSSI_LIMIT, data))
    if len(data) == 0:
        return 1.0

    ch_q_l = []
    for datum in data:
        # consider extenders presence on all channels, because they mirror the cpe
        # and keep other values as announced
        mirror = False
        if datum.get('type') == 'E' and datum.get('channel') == rch:
            mirror = True
        cpe_ch = ch if mirror else datum.get('channel')
        cpe_bw = datum.get('bandwidth')

        if cpe_bw not in (20, 40, 80, 160):
            cpe_bw = 40

        if cpe_bw != 20:
            """ 1) Get from ch_5G module the ch_map dictionary. 
                2) Get from ch_map dictionary related to bandwidth sub-dictionary. 
                3) Get from this sub-dictionary channel according to mapping rule 
                (if there is no result, get will return the same channel). """

            map_d = ch_5G.ch_map[cpe_bw]
            cpe_ch = map_d.get(cpe_ch, cpe_ch)

        IF = ch_5G.IF_5G[ch].get(cpe_ch, 0.0)
        if IF == 0.5:
            """ quasi-ACI case """
            cpe_rssi = datum.get('rssi')
            IF = IF * (10 ** ((cpe_rssi - P0) / 10))
        ch_q_l.append(IF)

    A = 1.13566054
    B = 0.1239393

    if remove_radar:
        ch_q = A * Exp(-B * (sum(ch_q_l) + 1))
    else:
        ch_q = A * Exp(-B * (sum(ch_q_l)))

    if ch_q > 1.0:
        return 1.0

    return ch_q


def greedy_calc(radar, environment, country=None, change_bw=False):

    """
    Inputs:
        radar: dict
            Information about radar
        environment: list of dictionaries
            JSON like data about radar's environment
            E.g. [{"channel": .., "rssi": .., "bandwidth": ..,
                  "standard": .., "type": "R" or "A"}, ...]
        country: str
            Country name (for possible channels validation)
        change_bw: bool
            Is it possible or not to change current band width
    Outputs:
        best_chan: int
            Proposed channel
        best_qual: float
            Proposed channel quality
        best_bw: int
            Proposed band width (if change_bw=True)

    Greedy algorithm to select the best channel for certain radar and change band width if this is reasonable.
    """

    if change_bw:
        best_chan, best_qual, best_bw = bw_select(radar, environment, country)
        return best_chan, best_qual, best_bw
    else:
        best_chan, best_qual = channel_quality_greedy_calc(radar, environment, country)
        return best_chan, best_qual


def channel_quality_greedy_calc(radar, environment, country):
    """
    Inputs:
        radar: dict
            Information about radar
        environment: list of dictionaries
            JSON like data about radar's environment
            E.g. [{"channel": .., "rssi": .., "bandwidth": .., 
                  "standard": .., "type": "R" or "A"}, ...]
    Otputs: 
        best_chan: int
            Proposed channel
        best_qual: float
            Proposed channel quality 

    Greedy algorithm to select the best channel for certain radar. 
    """

    if len(radar["possible_channels"]) == 0:
        raise ValueError("Empty list of possible channels!")

    if country is not None:
        if country in ch_5G.country_available_channels.keys():
            available_channels = ch_5G.country_available_channels.get(country)
            possible_channels = [ch for ch in radar["possible_channels"] if ch in available_channels]

            """ Check: is list of possible channels empty or not """
            if len(possible_channels) == 0:
                raise RuntimeError("All of the possible channels are forbidden for selected country (%s)!"
                                   "List of possible channels (received from device): %s"
                                   % (str(country), str(radar["possible_channels"])))
        else:
            raise ValueError("Unknown or undefined country: %s" % str(country))
    else:
        possible_channels = radar["possible_channels"]

    ch_quals = {chan: channel_quality(chan, environment, radar["bandwidth"], radar["radio_chan"])
                for chan in possible_channels}

    """ Avoid selection of channels which are rejected in certain countries """
    if country is not None:
        channels_l = sorted(ch_quals, key=ch_quals.get, reverse=True)
        for chan in channels_l:
            """ Get the true channel (frequency) """
            if radar["bandwidth"] > 20:
                mapped_chan = ch_5G.ch_map[radar["bandwidth"]].get(chan, chan)
            else:
                mapped_chan = chan
            """ Check this channel """
            if mapped_chan in ch_5G.country_available_channels.get(country):
                best_chan = chan
                break
            else:
                continue
        else:
            raise EmptyPossibleChannels("All of the possible channels are forbidden for selected country (%s) "
                                        "and selected bandwidwh (%d MHz)! "
                                        "List of possible channels (received from device): %s"
                                        % (str(country), radar["bandwidth"], str(radar["possible_channels"])))
    else:
        best_chan = max(ch_quals, key=ch_quals.get)

    best_qual = ch_quals[best_chan]

    return best_chan, best_qual


def bw_select(radar, environment, country):
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
        best_bw: int
            Proposed bandwidth

    Greedy algorithm to select the best channel and the best bandwidth for certain radar. 
    """

    """ Keep the current state of the bandwidth """
    current_bw = radar["bandwidth"]

    bw_qual = {}
    bw_qual_chan = {}

    global USABLE_BW

    """ Iterate by different bandwidths """
    if radar.get('possible_bandwidths', False):
        USABLE_BW = tuple(radar['possible_bandwidths'])
    for bw in USABLE_BW:
        radar["bandwidth"] = bw
        try:
            best_chan, best_qual = channel_quality_greedy_calc(radar, environment, country)
        except EmptyPossibleChannels:
            # At least current bandwidth should stay...
            continue

        bw_qual.update({bw: best_qual})
        bw_qual_chan.update({bw: {"best_chan": best_chan,
                                  "best_qual": best_qual}})

    best_bw = sorted(bw_qual, key=bw_qual.get, reverse=False)[-1]
    best_chan = bw_qual_chan[best_bw]["best_chan"]
    best_qual = bw_qual_chan[best_bw]["best_qual"]

    """ If proposed bandwidth is larger than current, it is good.
    However, if is not, the additional checks should be done. """

    radar["bandwidth"] = current_bw
    if best_bw < current_bw:
        bw_diff = current_bw / best_bw

        current_best_chan, current_best_qual = channel_quality_greedy_calc(radar, environment, country)
        diff_qual = best_qual / current_best_qual

        """ We suggest that bandwidth decreasing is reasonable 
        only if proportional channel quality increasing is possible """

        if diff_qual > bw_diff:
            return best_chan, best_qual, best_bw
        else:
            return current_best_chan, current_best_qual, current_bw

    return best_chan, best_qual, best_bw
