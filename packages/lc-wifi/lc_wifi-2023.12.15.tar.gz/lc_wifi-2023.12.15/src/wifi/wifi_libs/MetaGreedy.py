from baseG2 import channel_quality as channel_quality_2g
from baseG5 import channel_quality as channel_quality_5g

from baseG2 import greedy_calc as greedy_calc_2g
from baseG5 import greedy_calc as greedy_calc_5g

ITER_NUM = 1000


def run(radars_l, devices_l, use_5G=False, dict_out=False):
    """
    Inputs:
        radars_l: list of dictionaries
                  Contains JSON like data about radars
        devices_l: list of dictionaries
                  Contains JSON like data about devices around radars
    Outputs:
        results_l: list of tuples
                Contains tuples consisting of radar's CPE ID, channel quality value and 
                the channel from the best selected combination
    """
    for radar in radars_l:
        if radar.get("qual_current") is None:
            radar.update({"qual_current": 0.0})
        if radar.get("qual_possible") is None:
            radar.update({"qual_possible": 0.0})

    for _ in range(ITER_NUM):
        radars_l = sorted(radars_l, key=lambda radar: radar["qual_current"])
        for radar in radars_l:

            environment = [{"channel": device['channel'],
                            "rssi": device['rssi'],
                            "bandwidth": device['channel_width'],
                            "type": 'A'} for device in devices_l
                           if device['radar_cpeid'] == radar['cpeid']]
            """ Greedy part """
            if use_5G:
                best_chan, best_qual = greedy_calc_5g(radar, environment)
            else:
                best_chan, best_qual = greedy_calc_2g(radar, environment)

            """ Check the quality (better or not) """
            current_qual = radar.get("qual_current", 0.0)
            if current_qual >= best_qual:
                continue

            """ Keep the optimization information """
            radar["qual_current"] = best_qual
            radar["channel"] = best_chan
            for device in devices_l:
                if device["dev_cpeid"] == radar["cpeid"]:
                    device["channel"] = best_chan

    """ Save the last optimized quality """
    for radar in radars_l:
        environment = [{"channel": device['channel'],
                        "rssi": device['rssi'],
                        "bandwidth": device['channel_width'],
                        "type": 'A'} for device in devices_l
                       if device['radar_cpeid'] == radar['cpeid']]
        if use_5G:
            radar["qual_possible"] = channel_quality_5g(radar["channel"], environment,
                                                        radar["bandwidth"])
        else:
            radar["qual_possible"] = channel_quality_2g(radar["channel"], environment)

    if dict_out:
        out = [{"cpeid": radar["cpeid"],
                "qual_possible": round(radar["qual_possible"], 8),
                "channel_possible": radar["channel"]}
               for radar in radars_l]
    else:
        out = [(radar["cpeid"], round(radar["qual_possible"], 8), radar["channel"])
               for radar in radars_l]
    return out
