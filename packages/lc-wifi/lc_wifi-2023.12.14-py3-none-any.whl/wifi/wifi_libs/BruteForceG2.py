import itertools
from math import ceil
from baseG2 import channel_quality

""" Brute Force 2.4 GHz """


def criterion_func(list_l):
    """
    Inputs: 
        list_l: list of floats
            List with channel qualities for each radar
    Outputs:
        (sum_l - var): float
            Sum of channel qualities minus variance of the sequence (like regularization)

    Used in build-in max() function as the 'key' field.
    NOTE THAT: if channel qualities are distributed more or less uniformly, 
               this function is not required. Just max(target_list, key=sum) is sufficient.  
    """

    if not isinstance(list_l, list):
        list_l = list(list_l)

    l = len(list_l)
    sum_l = sum(list_l)
    mean = sum_l / l
    var = sum((i - mean) ** 2 for i in list_l) / l
    return sum_l - var


def estimate_environment(radars_l, devices_l):
    """
    Inputs:
        radars_l: list of dictionaries
            Contains JSON like data about radars
        devices_l: list of dictionaries
            Contains JSON like data about devices around radars
    Outputs:
        channelq_d: dict
            Contains channel as a key and channel quality as values

    Contains channel qualities for each channel from 1 to 13 
            based on information about devices that are not radars
    """

    radars_cpeid = [radar["cpeid"] for radar in radars_l]
    aliens = list(filter(lambda device: device["dev_cpeid"]
                                        not in radars_cpeid, devices_l))
    aliens_proc = [{"channel": device['channel'],
                    "rssi": device['rssi'],
                    "bandwidth": device['channel_width'],
                    "radar_cpeid": device['radar_cpeid'],
                    "type": 'A'}
                   for device in aliens]

    channelq_l = []
    for radar in radars_l:
        radar_data = list(filter(lambda device:
                                 device["radar_cpeid"] == radar["cpeid"], aliens_proc))
        radarq_l = [channel_quality(chan, radar_data)
                    for chan in range(1, radar["upper_channel"] + 1)]
        channelq_l.append(radarq_l)

    return channelq_l


def get_combs(radars_l, devices_l=None, what_cmbs='all'):
    """
    Inputs:
        radars_l: list of dictionaries
            Contains JSON like data about radars
        devices_l: list of dictionaries
            Contains JSON like data about devices around radars
        what_cmbs : str
            Option for combinations selections (TODO: change name, make int?)
            Possible states:
                'all': means all possible channels combination
                'orthogonality based': means only ortogonal combinations
                'channel quality based': top N channel combination 
                    based on pre-estimated channel qualities
    Outputs:
        combs_l: list of tuples
            Contains all of the required combinations between radars' channels

    Returns all required combinations from channels_l. 
    """

    channels_l = [[chan for chan in range(1, radar['upper_channel'] + 1)]
                  for radar in radars_l]  # ranges of the channels for each radar

    if (what_cmbs == 'all'):

        # Form all possible combinations: N = N_radars^N_channels
        combs_l = list(itertools.product(*channels_l))

    elif what_cmbs == 'channel quality based':

        # Estimate channel quality of each channel based on environment (aliens)
        channels_quality = estimate_environment(radars_l, devices_l)

        best_chans = []
        for idx_r, radar in enumerate(radars_l):

            cq_i = channels_quality[idx_r]
            top = ceil(radar["upper_channel"] / 3)
            top_chans = sorted(range(len(cq_i)), key=lambda i: cq_i[i])[-top:]
            top_chans = [ch + 1 for ch in top_chans]
            top_quals = sorted(cq_i)[-top:]
            top_d = {chan: qual for chan, qual in zip(top_chans, top_quals)}

            cur_q = radar.get('qual_current', 0.0)
            if cur_q == None:
                cur_q = 0.0

            better_chans_r = [chan for chan, qual
                              in top_d.items() if qual > cur_q]

            if len(better_chans_r) == 0:
                best_chans.append([radar["channel"]])
                continue

            best_chans.append(better_chans_r)

        combs_l = list(itertools.product(*best_chans))

    return combs_l


def setup_channels(radars_l, devices_l, comb):
    """
    Inputs:
        radars_l: list of dictionaries
            Contains JSON like data about radars
        devices_l: list of dictionaries
            Contains JSON like data about devices around radars
        comb: tuple of ints
            Contains certain combination of channels
    Outputs:
        radars_l: list of dictionaries
            'channel' field of each radar is updated
        devices_l: list of dictionaries
            'channel' field of each devices, which is also radar, is updated 

    Changes 'channel' field where it is required.
    """

    for index, radar in enumerate(radars_l):
        # setup radar
        radar['channel'] = comb[index]
        # setup devices which are radar 
        radar_cpeid = radar['cpeid']
        for device in devices_l:
            if device['dev_cpeid'] == radar_cpeid:
                device['channel'] = comb[index]
    return radars_l, devices_l


# TODO: should be renamed (just run() maybe)
def possible_channels_quality(radars_l, devices_l, what_cmbs='all', dict_out=False):
    """
    Inputs:
        radars_l: list of dictionaries
            Contains JSON like data about radars
        devices_l: list of dictionaries
            Contains JSON like data about devices around radars
        what_cmbs : str
            Option for combinations selections (TOD: change name, make int?)
            Possible states:
                'all': means all possible channels combination
                'channel quality based': top N channel combination 
                    based on pre-estimated channel qualities
    Outputs:
        results_l: list of tuples
            Contains tuples consisting of radar's CPE ID, channel quality value and 
            the channel from the best selected combination

    Calulates all of the possible channel qualities for each radar; 
    selects best channel combination.

    Example:
        In:
            radars_l.append({'cpeid': pCPEID,
                               'channel': int(pCHANNEL),
                               'upper_channel': radar_upper_channel2,
                               'qual_current': pQUAL_CURRENT,
                               'target_channel': pTARGET_CHANNEL})

            devices_l.append({'radar_cpeid': pRADAR_CPEID,
                                'dev_cpeid': pDEV_CPEID,
                                'channel': int(pDEV_CHANNEL),
                                'rssi': int(pDEV_RSSI),
                                'channel_width': int(str(pDEV_CHANNEL_WIDTH).replace("MHz","").replace(" ","")),
                                'standard': st})
        Out:
            [(cpeid, qual_possible, target_channel),...]
    """

    results_l = []
    if len(radars_l) > 0 and len(devices_l) > 0:
        # All possible combinations of the radars' channels
        if what_cmbs == 'all':
            combs_l = get_combs(radars_l)
        elif what_cmbs == 'channel quality based':
            combs_l = get_combs(radars_l, devices_l, what_cmbs=what_cmbs)
        # TODO: else case

        quality_l = []  # it will be list of lists
        # where each inner list corresponds to certain channels combination
        quality_l_append = quality_l.append  # to reduce function calls

        for comb in combs_l:
            radars_l, devices_l = setup_channels(radars_l, devices_l, comb)

            # Radar's channel quality calculation loop
            radar_quality = []  # list of channel quality values for each radar
            radar_quality_append = radar_quality.append
            for radar in radars_l:
                cq_data = [{"channel": device['channel'],
                            "rssi": device['rssi'],
                            "bandwidth": device['channel_width'],
                            "type": 'A'} for device in devices_l
                           if device['radar_cpeid'] == radar['cpeid']]

                channelq = channel_quality(radar['channel'], cq_data, remove_radar=True)
                radar_quality_append(channelq)

            quality_l_append(radar_quality)

        # Select maximum CQ value and add necessary information into the list
        max_quality = max(quality_l, key=criterion_func)
        qual_idx = quality_l.index(max_quality)
        for index, radar in enumerate(radars_l):
            # The list that relates to the corresponding to globaly maximum CQ value combination 
            best_channel = combs_l[qual_idx][index]
            qp_o = round(max_quality[index], 8)
            if dict_out:
                results_l.append({"cpeid": radar["cpeid"],
                                  "qual_possible": qp_o,
                                  "channel_possible": best_channel})
            else:
                results_l.append((radar['cpeid'], qp_o, best_channel))
    return results_l
