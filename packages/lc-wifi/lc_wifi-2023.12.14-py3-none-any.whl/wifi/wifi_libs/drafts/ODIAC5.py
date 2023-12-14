#!/usr/bin/env python
# coding: utf-8
"""
Created on Fri Jun  1 17:16:15 2018

@author: D
"""
import pprint 
from datetime import datetime
from G5Rus import *

def computeQualityCoefficients(channels,others, arrayWithChannelsAndRSSI):
    result = []
    # array which will contain Ch Quality Coefficients
    for i in channels:
        result.append([int(i),channel_quality(int(i), arrayWithChannelsAndRSSI, iw_dict)])
    for i in others:
        if not type(i) is list:
            result.append([int(i), 0.000])
    return result

def FriendsRadarCoefficients(data,others_russia):
    #others_russia = [[96,0.000],[100,0.000],[102,0.000],[104, 0.000],[106,0.000],[108,0.000],[110,0.000],[112,0.000],[114,0.000],[116,0.000],[118,0.000],[120,0.000],[122,0.000],[124,0.000],[126,0.000],[128,0.000]]
    res = {}
    for k,v in data.items():
        midres = computeQualityCoefficients(iw_dict.keys(),others_russia,v)
        res["%s"%k] = {}
        radar_ch = list(filter(lambda x : x['type'] == 'R', v))[0]['channel']
        res["%s"%k]['radar_channel'] = radar_ch
        res["%s"%k]['radar_curr_qual'] = list(filter(lambda x : x[0] == radar_ch, midres))[0][1]
    return res

def ChangeChRadar(defRadar,NeighbourInCluster,data,radar,friends,koeff,arrBestChannels,interval,others_russia):
    future_result = {}
    midd_result = {}
    #'1':{'radar_curr_qual':0, 'radar_channel':0},'2':{'radar_curr_qual':0, 'radar_channel':0}, 'current_radar': radar}
    for movement_ch in arrBestChannels[0:interval]:
        data[0][0] = movement_ch
        result = []
        r = None
        for channel in iw_dict.keys():
            if(channel == movement_ch):
                r = channel_quality(channel, data,iw_dict)
                radar_curr_qual = r
        radar_channel = movement_ch

        defRadar[0] = movement_ch+1
        new_friends = FriendsRadarCoefficients(NeighbourInCluster,others_russia)
        if radar_curr_qual > radar['radar_curr_qual']:
            for fr_r_index in new_friends.keys():
                if new_friends[fr_r_index]['radar_curr_qual'] >= friends[fr_r_index]['radar_curr_qual']:# and (friends[fr_r_index]['radar_channel'] == new_friends[fr_r_index]['radar_channel']):
                    if abs(new_friends[fr_r_index]['radar_curr_qual'] - friends[fr_r_index]['radar_curr_qual']) > koeff/100 or abs(new_friends[fr_r_index]['radar_curr_qual'] - friends[fr_r_index]['radar_curr_qual']) == 0:
                        if 'current_radar' in midd_result.keys():
                            if radar_curr_qual > midd_result['radar_curr_qual']:
                                midd_result['current_radar']= radar_channel
                                midd_result['radar_curr_qual'] = radar_curr_qual
                        else:
                            midd_result['current_radar']= radar_channel
                            midd_result['radar_curr_qual'] = radar_curr_qual

                        midd_result["%s"%fr_r_index] = {}
                        midd_result["%s"%fr_r_index]['radar_curr_qual'] = 0
                        midd_result["%s"%fr_r_index]['radar_channel'] = 0
                        if midd_result["%s"%fr_r_index]['radar_curr_qual'] < new_friends[fr_r_index]['radar_curr_qual']:
                            midd_result["%s"%fr_r_index]['radar_channel'] = new_friends[fr_r_index]['radar_channel']
                            midd_result["%s"%fr_r_index]['radar_curr_qual'] = new_friends[fr_r_index]['radar_curr_qual']
                        else:
                            midd_result["%s"%fr_r_index]['radar_channel'] = new_friends[fr_r_index]['radar_channel']
                            midd_result["%s"%fr_r_index]['radar_curr_qual'] = new_friends[fr_r_index]['radar_curr_qual']
                        midd_result["%s"%fr_r_index]['radar_channel'] = new_friends[fr_r_index]['radar_channel']
                        midd_result["%s"%fr_r_index]['radar_curr_qual'] = new_friends[fr_r_index]['radar_curr_qual']
        else:
            midd_result = friends
            midd_result['current_radar'] = radar['radar_channel']
            midd_result['radar_curr_qual'] = radar['radar_curr_qual']



    return midd_result    

def main(listRadars,listDevices):
    others_russia = [96,100,102,104,106,108,110,112,114,116,118,120,122,124,126,128]
    UpperChannel = 165
    PossibleChannels = iw_dict.keys()
    forProbedChInd = 0;
    others_russia = [[96,0.000],[100,0.000],[102,0.000],[104, 0.000],[106,0.000],[108,0.000],[110,0.000],[112,0.000],[114,0.000],[116,0.000],[118,0.000],[120,0.000],[122,0.000],[124,0.000],[126,0.000],[128,0.000]]

    listResult = []#(cpeid, qual_possible, target_channel)
    for i in listRadars:
        i['type'] = 'R'
        i['rssi'] = 0
        defRadar = {
            'channel':i['channel'],
            'rssi': 0,
            'bandwidth': 20,
            'standard': 4,
            'type':'F',
            'ftype': 'R'
            }
        NeighbourInCluster = {}
        for j in listRadars:
            if j['cpeid']!=i['cpeid']:
                if not NeighbourInCluster.get(j['cpeid']):
                    NeighbourInCluster[j['cpeid']] = []
                for neighbour in listDevices:
                    if neighbour.get('radar_cpeid') == j['cpeid']:
                        NeighbourInCluster[j['cpeid']].append(
                            {
                            'channel': neighbour['channel'],
                            'rssi': neighbour['rssi'],
                            'bandwidth': neighbour['channel_width'],
                            'standard': neighbour['standard'],
                            'type': 'F',
                            'ftype': 'F'
                            }
                        )
                NeighbourInCluster[j['cpeid']].append(defRadar)
                NeighbourInCluster[j['cpeid']].append({'channel':j['channel'],'rssi': 0, 'bandwidth': 20, 'standard':4, 'type':'R', 'ftype': 'F'})

                j['type'] = 'F'
                j['rssi'] = neighbour['rssi']
                j['bandwidth'] = 20
                j['standard'] = 4
        CurentQualities = bubble_sort(computeQualityCoefficients(iw_dict.keys(),others_russia,listRadars))
        bestchannels = [i[0] for i in sorted(CurentQualities,key=lambda x: x[1], reverse=True)]
        interval = 5
        koeff=10
        channel = list(filter(lambda x : x['type'] == 'R', listRadars))[0]['channel']
        radar = {
        'radar_channel': channel,
        'radar_curr_qual': list(filter(lambda x : x[0] == channel, CurentQualities))[0][1],
        }
        friends = FriendsRadarCoefficients(NeighbourInCluster,others_russia)
        changes = ChangeChRadar(defRadar,NeighbourInCluster,listRadars,radar,friends,koeff,bestchannels, interval,others_russia)
    
        res = {
        'current_radar_sutuation': radar,
        'friends_current_situation': friends,
        'future_situation': changes
        }
        #if we want to move all radars 
        #i['channel']=res['future_situation']['current_radar']
        
        for ind in listDevices:
            if not res['future_situation'].get(ind['dev_cpeid']):
                continue
            else:
                if ind['radar_cpeid'] == i['cpeid'] and res['future_situation'].get(ind['dev_cpeid']):
                    ind['channel'] = res['future_situation'][ind['dev_cpeid']]['radar_channel'] 

        listResult.append((i['cpeid'], round(res['future_situation']['radar_curr_qual'],8),res['future_situation']['current_radar']))


    
    return listResult


if __name__ == "__main__":
    listRadars = [{
    'cpeid': '001095-B42A0E557015', 
    'channel': 40, 
    'upper_channel': 165, 
    'qual_current': 0.1640074227973831, 
    'target_channel': 32
    }, 
    {
    'cpeid': '6C2E85-AC3B778E001A', 
    'channel': 44, 
    'upper_channel': 165, 
    'qual_current': 0.0005871402634457763, 
    'target_channel': 36
    }
    ]
    listDevices = [
    {
    'radar_cpeid': '001095-B42A0E557015', 
    'dev_cpeid': '6C2E85-AC3B778E001A', 
    'channel': 44, 
    'rssi': -63, 
    'channel_width': 20, 
    'standard': 4
    }, 
    {
    'radar_cpeid': '6C2E85-AC3B778E001A', 
    'dev_cpeid': '001095-B42A0E557015', 
    'channel': 40, 
    'rssi': -77, 
    'channel_width': 20, 
    'standard': 3
    }, 
    {
    'radar_cpeid': '6C2E85-AC3B778E001A', 
    'dev_cpeid': '6C2E85-AC3B778E002B', 
    'channel': 52, 
    'rssi': -84, 
    'channel_width': 80, 
    'standard': 4
    }, 
    {
    'radar_cpeid': '6C2E85-AC3B778E001A', 
    'dev_cpeid': '6C2E85-AC3B778E003B', 
    'channel': 52, 
    'rssi': -64, 
    'channel_width': 80, 
    'standard': 4
    }, 
    ]
    start_time = datetime.now()
    print(main(listRadars,listDevices))
    end_time = datetime.now()
    print('Time: {}'.format(end_time - start_time))
