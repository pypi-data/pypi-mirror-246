# Introduction

This project contains several tools for Wi-Fi optimization (both 2.4GHz and 5GHz) such as:
- functions for channel quality calculation;
- greedy optimization algorithms; 
- mass optimization algorithms.

# Installation

To install the last verified version run the following:

```sh
$ pip3 install wifi_utils --index http://pypi.axlocal/ --trusted-host pypi.axlocal
```

To install the certain version just specify it:

```sh
$ pip3 install wifi_utils==0.3.0rc24 --index http://pypi.axlocal/ --trusted-host pypi.axlocal
```

# How to use? (examples) 

## 1. Channel quality calculation

To calculate the current channel quality at the certain channel in **2.4GHz** frequency band use the following expression:

```python
import baseG2 as G2

# Considered channel (int):
channel = 1 
# Information about radar's environment
environment = [{"channel": 1,
                "bandwidth": 20,
                "rssi": -50,
                "type": "A"},
                
               {"channel": 11,
               "bandwidth": 20,
               "rssi": -86,
               "type": "A"}]

current_qual = G2.channel_quality(channel, environment) # returns float 
print(current_qual)

>>> 0.9145768466546006

```
This function can also accept the additional arguments:

- remove_radar (```bool```): 
    - if radar should be excluded from the calculations: ```True``` (*default*); 
    - if radar should not be excluded from the calculations: ```False```.
-  rssi_threshold (```int```): the value bellow which RSSI should be taken into account (*default*: ```MIN_RSSI``` means RSSI is not considered). 


To calculate the current channel quality at the certain channel in **5GHz** frequency band use the following expression:

```python
import baseG5 as G5

# Considered channel (int):
channel = 36 

#Considered radar's bandwidth
bandwidth = 80

# Information about radar's environment
environment = [{"channel": 36,
                "bandwidth": 40,
                "rssi": -50,
                "type": "A"},
                
               {"channel": 40,
               "bandwidth": 80,
               "rssi": -86,
               "type": "A"}]

current_qual = G5.channel_quality(channel, environment, bandwidth) # returns float 
print(current_qual)

>>> 0.7830149853634231

```

This function can also accept the additional argument:
- remove_radar (```bool```): 
  - if radar should be excluded from the calculations: ```True``` (*default*); 
  - if not: ```False```.


The description of the required fields in the ```environment``` is presented below (tab. 1):

**Tab. 1.** *Required field of "environment" variable.*


| Name        | Type           | Description  |
| ------------- |:-------------:| :-----|
| channel | ```int``` | Operating Wi-Fi channel of the interfering device.|
| bandwidth | ```int``` | Operating bandwidth (in MHz) of the interfering device.|
| rssi | ```int```| RSSI between radar and interfering device.|
| type | ```str``` | Who is the interfering device: alien ("A"), friend ("F"), radar ("R"). |

One optional field is added in ```wifi_utils==0.3.0rc21```:
- ```associated_devices``` (```int```): number of associated devices (default ```None```).

If the value of this field is equal to 0, the devices does not communicate with anyone and therefore can be excluded from the consideration.  

## 2. Greedy optimization algorithm

To calculate possible channel quality for certain radar without concerning about impacts to another radars use the following:

- for 2.4 GHz

```python
import baseG2 as G2

# Information about radar
radar = {"channel":  1, "upper_channel": 13}
# Information about radar's environment
environment = [{"channel": 1,
                "bandwidth": 20,
                "rssi": -50,
                "type": "A"},
                
               {"channel": 11,
               "bandwidth": 20,
               "rssi": -86,
               "type": "A"}]

best_chan, best_qual = G2.greedy_calc(radar, environment)
print(best_chan)
print(best_qual)

>>> 6
    1.0
```

The dictionary ```radar``` should contain at least ```"upper_channel"``` field which means the maximum possible Wi-Fi channel.

- for 5GHz

```python
import baseG5 as G5

# Information about radar
radar = {"channel":  36, "bandwidth": 80, "possible_channels": [36, 40, 44, 48, 149, 157, 165]}
# Information about radar's environment
environment = [{"channel": 36, 
                "bandwidth": 40,
                "rssi": -50,
                "type": "A"},
                
                {"channel": 40,
                "bandwidth": 80,
                "rssi": -86,
                "type": "A"}]

best_chan, best_qual = G5.greedy_calc(radar, environment)
print(best_chan)
print(best_qual)

>>> 149
    1.0 
```

The dictionary ```radar``` should contain at least:
- ```"bandwidth"``` (**int**): operating radar's bandwidth;
- ```"possible_channels"``` (**list** of **int**s): possible channels for operation.


In both cases (2.4GHz and 5GHz) the function ```greedy_calc``` returns:
- ```best_chan``` (**int**): the best of possible channels;
- ```best_qual``` (**float**): the best of possible channel qualities (from 0 to 1; 1 means no interference).

Moreover, the bandwidth selection is available for 5GHz:

```python
import baseG5 as G5

# Information about radar
radar = {"channel":  36, "bandwidth": 80, "possible_channels": [36, 40, 44, 48, 149, 157, 165]}
# Information about radar's environment
environment = [{"channel": 36, 
                "bandwidth": 40,
                "rssi": -50,
                "type": "A"},
                
                {"channel": 40,
                "bandwidth": 80,
                "rssi": -86,
                "type": "A"}]

best_chan, best_qual, best_bw = G5.greedy_calc(radar, environment, change_bw=True)
print(best_chan)
print(best_qual)
print(best_bw)

>>> 149
    1.0
    80 
```

The function ``greedy_calc()`` with defined `True` `change_bw` argument returns:
- ```best_chan``` (**int**): the best of possible channels;
- ```best_qual``` (**float**): the best of possible channel qualities (from 0 to 1; 1 means no interference).
- ``best_bw`` (**int**): the best of possible bandwidths.

One optional argument is added in ```wifi_utils==0.3.0rc23``` for 5GHz:
   -  ``country`` (**str**): country name (or region in case of Europe) for possible channels validation

Set of available country names: {'Australia', 'Bahrain', 'Brazil', 'Canada', 'China', 'Europe', 'India', 'Indonesia', 'Israel', 'Japan', 'Korea',
 'New Zealand',
 'Russia',
 'Singapore',
 'South Africa',
 'Taiwan',
 'Turkey',
 'USA',
 'Vietnam'}
    

## 3. "Brute Force": optimal mass optimization algorithm

The main idea of the "Brute Force algorithm" is to select the best channel combination from **all the possible** combinations. 

Complexity of this algorithm is <img src="https://i.upmath.me/svg/%20O(N%5Em)%20" alt=" O(N^m) " /> where <img src="https://i.upmath.me/svg/N" alt="N" /> is the number of radars in cluster, and <img src="https://i.upmath.me/svg/m" alt="m" /> is the maximum number of the possible channels (13 in most of systems)

The order of procedures is presented in figure 1.

<img src="https://habrastorage.org/webt/ds/in/xx/dsinxxaysfy-0k4i8z17afa8d2y.png" width="200"/>

*Fig. 1. Block-scheme of the Brute Force algorithm.*

To find the optimal channel combination for certain cluster use the following:

- for 2.4GHz

```python
import BruteForceG2 as BFG2

# List of radars:
radars_l = [{"cpeid": "00259E-48575443D6CBD39C",
            "channel": 1,
            "upper_channel": 13},
            
            {"cpeid": "00259E-48575443D6CBD39D",
            "channel": 6,
            "upper_channel": 13}]
            
# List which contains information about environments
devices_l = [{"radar_cpeid": "00259E-48575443D6CBD39C",
              "dev_cpeid": "00259E-48575443D6CBD39D",
              "channel": 6,
              "rssi": -56,
              "channel_width": 20},
              
              {"radar_cpeid": "00259E-48575443D6CBD39D",
              "dev_cpeid": "00259E-48575443D6CBD39C",
              "channel": 1,
              "rssi": -56,
              "channel_width": 20},
              
              {"radar_cpeid": "00259E-48575443D6CBD39D",
              "dev_cpeid": "",
              "channel": 6,
              "rssi": -78,
              "channel_width": 20}]
              
results_l = BFG2.possible_channels_quality(radars_l, devices_l, dict_out=True)
print(results_l)


>>> [{'cpeid': '00259E-48575443D6CBD39C', 'qual_possible': 1.0, 'channel_possible': 1}, 
     {'cpeid': '00259E-48575443D6CBD39D', 'qual_possible': 1.0, 'channel_possible': 11}]
```

- for 5GHz

```python
import BruteForceG5 as BFG5

# List of radars:
radars_l = [{'cpeid': '001095-14B7F887C74E',
            'channel': 36,
            'bandwidth': 40, 
	    'possible_channels': [36,40,44,48,52,56,60,64,149,153,157,161]},
			
            {'cpeid': '001095-B42A0EE13276',
            'channel': 36,
            'bandwidth': 40,
      	    'possible_channels': [36,40,44,48,52,56,60,64,149,153,157,161]}]
              	
# List which contains information about environments
devices_l = [{'radar_cpeid': '001095-14B7F887C74E', 
             'dev_cpeid': '001095-B42A0EE13276', 
             'channel': 36, 
             'rssi': -55, 
             'channel_width': 40},
             
             {'radar_cpeid': '001095-14B7F887C74E',
             'dev_cpeid': '', 
             'channel': 149, 
             'rssi': -53,
             'channel_width': 40},
             
             {'radar_cpeid': '001095-B42A0EE13276',
             'dev_cpeid': '001095-14B7F887C74E',
             'channel': 36,
             'rssi': -55,
             'channel_width': 40},
             
             {'radar_cpeid': '001095-B42A0EE13276',
             'dev_cpeid': '',
             'channel': 40,
             'rssi': -53,
             'channel_width': 80}]
              
results_l = BFG5.run(radars_l, devices_l, dict_out=True)
print(results_l)

>>> [{'cpeid': '001095-14B7F887C74E', 'qual_possible': 1, 'channel_possible': 36},
     {'cpeid': '001095-B42A0EE13276', 'qual_possible': 1, 'channel_possible': 60}]
```

> **NOTE**:
>
>The option to select optimal bandwidth is not implemented in the current version of the library.

### Inputs:

The argument ```dict_out=True``` is required for ```dict``` output (by default ```dict_out=False``` for backward compatibility with old versions of considered library).

The required fields of each dictionary in ```radars_l``` are presented below (tab. 3 and tab. 4).

**Tab. 3.** *Required fields in radars dictionary for 2.4GHz.*

| Name        | Type           | Description  |
| ------------- |:-------------:| :-----|
| cpeid | ```str``` | Radar's CPE ID |
| channel | ```int``` | Radar's operating Wi-Fi channel |
| upper_channel | ```int``` | The largest of possible radar's Wi-Fi channels |

**Tab. 4.** *Required fields in radars dictionary for 5GHz.*

| Name        | Type           | Description  |
| ------------- |:-------------:| :-----|
| cpeid | ```str``` | Radar's CPE ID |
| channel | ```int``` | Radar's operating Wi-Fi channel |
| bandwidth | ```int``` | Operating channel bandwidth (in MHz) |
| possible_channels | ```list``` of ```int```-s | Possible channels to operate (country and vendor based) |

The required fields of each dictionary in ```devices_l``` are also presented below (tab. 5).

**Tab. 5.** *Required fields in devices dictionary.*

| Name        | Type           | Description  |
| ------------- |:-------------:| :-----|
| radar_cpeid | ```str``` | Radar's CPE ID which have detected considered device |
| dev_cpeid | ```str``` | Considered device's CPE ID |
| channel | ```int``` | Considered device's operating Wi-Fi channel |
| channel_width | ```int``` | Considered device's operating bandwidth (in MHz) |
| rssi | ```int``` | RSSI between radar and considered device|


### Outputs:

This function returns ```list``` of ```dict```-s with the following fields, where position of the tuple corresponds to the position of radar in ```radars_l``` (tab. 6).

**Tab. 6.** *Variables in returned dictionaries.*

| Field        | Type           | Description  |
| ------------- |:-------------:| :-----|
| cpeid | ```str``` | CPE' id|
| qual_possible | ```float``` | Possible channel quality |
| channel_possible | ```int``` | Proposed channel |


If the old versions of library is used the function will return ```list``` of ```tuples```. 

Each ```tuple``` contains the following information (tab. 7):

**Tab. 7.** *Variables in returned tuples.*

| Position        | Type           | Description  |
| ------------- |:-------------:| :-----|
| 0 | ```str``` | CPE' id|
| 1 | ```float``` | Possible channel quality |
| 2 | ```int``` | Proposed channel |

> **WARNING:**
>
> This algorithm cannot be applied to clusters larger than 7 radars due to its complexity.

## 4. "Pre-estimated Brute Force": sub-optimal mass optimization algorithm

The main purpose of this algorithm is to reduce the number of calculations.

This algorithm is implemented in several steps:
1. Calculate qualities on all of the possible channels for each radar based on information about their environments;
2. Select top of the best channels;
3. Make combinations based on remained channels;
4. Calculate channel qualities based on these combinations;
5. Select the best combination.

Complexity of this algorithm is <img src="https://i.upmath.me/svg/%20O(N%5En)%20" alt=" O(N^n) " /> where <img src="https://i.upmath.me/svg/N" alt="N" /> is the number of radars in cluster, and <img src="https://i.upmath.me/svg/n" alt="n" /> is the number of channels in the selecting top.

The block-scheme of the considered algorithm is presented in figure 2.

<img src="https://habrastorage.org/webt/lj/je/gp/ljjegpgdb0fny31ui_ld6llc3p0.png" width="550"/>

*Fig. 2. Block-scheme of the Pre-estimated Brute Force algorithm.*

To find the quasi-optimal (but faster) optimization solution for up to 10 radars per one cluster use the following:

- for 2.4Ghz

```python
import BruteForceG2 as BFG2

# List of radars:
radars_l = [{"cpeid": "00259E-48575443D6CBD39C",
            "channel": 1, 
            "upper_channel": 13,
            "qual_current": 1.0},
            
            {"cpeid": "00259E-48575443D6CBD39D",
            "channel": 6,
            "upper_channel": 13,
            "qual_current": 0.8}]
            
# List which contains information about environments
devices_l = [{"radar_cpeid": "00259E-48575443D6CBD39C",
              "dev_cpeid": "00259E-48575443D6CBD39D",
              "channel": 6,
              "rssi": -56,
              "channel_width": 20},
              
              {"radar_cpeid": "00259E-48575443D6CBD39D",
              "dev_cpeid": "00259E-48575443D6CBD39C",
              "channel": 1,
              "rssi": -56,
              "channel_width": 20},
              
              {"radar_cpeid": "00259E-48575443D6CBD39D",
              "dev_cpeid": "",
              "channel": 6,
              "rssi": -78,
              "channel_width": 20}]
              
results_l = BFG2.possible_channels_quality(radars_l, devices_l,
                                    what_cmbs="channel quality based", dict_out=True)
print(results_l)

>>> [{'cpeid': '00259E-48575443D6CBD39C', 'qual_possible': 1.0, 'channel_possible': 1}, 
     {'cpeid': '00259E-48575443D6CBD39D', 'qual_possible': 1.0, 'channel_possible': 11}]
```

- for 5GHz

```python
import BruteForceG5 as BFG5

# List of radars:
radars_l = [{'cpeid': '001095-14B7F887C74E',
            'channel': 36,
            'bandwidth': 40, 
	    'possible_channels': [36,40,44,48,52,56,60,64,149,153,157,161],
            'qual_current': 0.7},
			
            {'cpeid': '001095-B42A0EE13276',
            'channel': 36,
            'bandwidth': 40,
      	    'possible_channels': [36,40,44,48,52,56,60,64,149,153,157,161],
            'qual_current': 0.73}]
              	
# List which contains information about environments
devices_l = [{'radar_cpeid': '001095-14B7F887C74E', 
             'dev_cpeid': '001095-B42A0EE13276', 
             'channel': 36, 
             'rssi': -55, 
             'channel_width': 40},
             
             {'radar_cpeid': '001095-14B7F887C74E',
             'dev_cpeid': '', 
             'channel': 149, 
             'rssi': -53,
             'channel_width': 40},
             
             {'radar_cpeid': '001095-B42A0EE13276',
             'dev_cpeid': '001095-14B7F887C74E',
             'channel': 36,
             'rssi': -55,
             'channel_width': 40},
             
             {'radar_cpeid': '001095-B42A0EE13276',
             'dev_cpeid': '',
             'channel': 40,
             'rssi': -53,
             'channel_width': 80}]
              
results_l = BFG5.run(radars_l, devices_l, what_cmbs = 'channel quality based', dict_out=True)
print(results_l)

>>> [{'cpeid': '001095-14B7F887C74E',
      'qual_possible': 1.0,
      'channel_possible': 36},
     {'cpeid': '001095-B42A0EE13276',
      'qual_possible': 1.0,
      'channel_possible': 60}]
```
> **NOTE**:
>
>The option to select optimal bandwidth is not implemented in the current version of the library.


### Inputs:

The argument ```dict_out=True``` is required for ```dict``` output (by default ```dict_out=False``` for backward compatibility with old versions of considered library).

#### 2.4GHz:
- see **tab 3.** and **tab. 5**;
- ```"qual_current"``` field (in ```radars_l```): this field means current channel quality.

#### 5GHz:

- see **tab 4.** and **tab. 5**;
- ```"qual_current"``` field (in ```radars_l```): this field means current channel quality.

### Outputs:

See **tab. 6** (and tab. 7 for old versions).

> **WARNING:**
>
> This algorithm cannot be applied to  clusters larger than 10 radars due to its complexity.

## 5. "Meta Greedy" : fast and naive optimization algorithm

The main purpose of this algorithm is to process any sizes of clusters.

The main idea can be formulated as follows:

1. Sort radars by channel qualities (from the worst to the best).  
2. Apply greedy optimization for each of them.
3. Change channel if quality improvement is possible and save it in ```devices_l```.
4. Repeat this several times.

The block-scheme is presented in figure 3.

<img src="https://habrastorage.org/webt/gt/lt/91/gtlt91hdjpk9viwnvhqlulnhko8.png" width="500"/>

*Fig. 3. Block scheme of the Meta Greedy algorithm.*

To implement the fastest mass optimization implementation with no limits to number of radars use the following:

- for 2.4GHz

```python
import MetaGreedy as MG

# List of radars:
radars_l = [{"cpeid": "00259E-48575443D6CBD39C",
            "channel": 1,
            "upper_channel": 13,
            "qual_current": 1.0},
            
            {"cpeid": "00259E-48575443D6CBD39D",
            "channel": 6,
            "upper_channel": 13,
            "qual_current": 0.8}]
            
# List which contains information about environments
devices_l = [{"radar_cpeid": "00259E-48575443D6CBD39C",
              "dev_cpeid": "00259E-48575443D6CBD39D",
              "channel": 6,
              "rssi": -56,
              "channel_width": 20},
              
              {"radar_cpeid": "00259E-48575443D6CBD39D",
              "dev_cpeid": "00259E-48575443D6CBD39C",
              "channel": 1,
              "rssi": -56,
              "channel_width": 20},
              
              {"radar_cpeid": "00259E-48575443D6CBD39D",
              "dev_cpeid": "",
              "channel": 6,
              "rssi": -78,
              "channel_width": 20}]
              
results_l = MG.run(radars_l, devices_l, dict_out=True)
print(results_l)

>>> [{'cpeid': '00259E-48575443D6CBD39D', 'qual_possible': 1.0, 'channel_possible': 11}, 
     {'cpeid': '00259E-48575443D6CBD39C', 'qual_possible': 1.0, 'channel_possible': 1}]
```

- for 5GHz

```python
import MetaGreedy as MG

# List of radars:
radars_l = [{'cpeid': '001095-14B7F887C74E',
            'channel': 36,
            'bandwidth': 40, 
	    'possible_channels': [36,40,44,48,52,56,60,64,149,153,157,161],
            'qual_current': 0.7},
			
            {'cpeid': '001095-B42A0EE13276',
            'channel': 36,
            'bandwidth': 40,
      	    'possible_channels': [36,40,44,48,52,56,60,64,149,153,157,161],
            'qual_current': 0.73}]
              	
# List which contains information about environments
devices_l = [{'radar_cpeid': '001095-14B7F887C74E', 
             'dev_cpeid': '001095-B42A0EE13276', 
             'channel': 36, 
             'rssi': -55, 
             'channel_width': 40},
             
             {'radar_cpeid': '001095-14B7F887C74E',
             'dev_cpeid': '', 
             'channel': 149, 
             'rssi': -53,
             'channel_width': 40},
             
             {'radar_cpeid': '001095-B42A0EE13276',
             'dev_cpeid': '001095-14B7F887C74E',
             'channel': 36,
             'rssi': -55,
             'channel_width': 40},
             
             {'radar_cpeid': '001095-B42A0EE13276',
             'dev_cpeid': '',
             'channel': 40,
             'rssi': -53,
             'channel_width': 80}]
              
results_l = MG.run(radars_l, devices_l, use_5G=True, dict_out=True)
print(results_l)

>>> [{'cpeid': '001095-14B7F887C74E',
      'qual_possible': 1.0,
      'channel_possible': 52},
     {'cpeid': '001095-B42A0EE13276',
      'qual_possible': 1.0,
      'channel_possible': 149}]
```
> **NOTE**:
>
>The option to select optimal bandwidth is not implemented in the current version of the library.

### Inputs:

The argument ```dict_out=True``` is required for ```dict``` output (by default ```dict_out=False``` for backward compatibility with old versions of considered library).

#### 2.4GHz:
- see **tab 3.** and **tab. 5**;
- ```"qual_current"``` field (in ```radars_l```): this field means current channel quality.

#### 5GHz:

- see **tab 4.** and **tab. 5**;
- ```"qual_current"``` field (in ```radars_l```): this field means current channel quality.

### Outputs:

See **tab. 6** (and tab. 7 for old versions).