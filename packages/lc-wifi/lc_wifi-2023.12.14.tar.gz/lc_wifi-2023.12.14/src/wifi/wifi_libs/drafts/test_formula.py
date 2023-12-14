from G2Base_AM import channel_quality 

cq_data = [ {"channel": 1, 
            "rssi": -87, 
            "bandwidth": 20,
            "type": 'A'},

            {"channel": 11, 
            "rssi": -87, 
            "bandwidth": 20,
            "type": 'A'},

            {"channel": 9, 
            "rssi": -87, 
            "bandwidth": 20,
            "type": 'A'},

            {"channel": 13, 
            "rssi": -65, 
            "bandwidth": 20,
            "type": 'A'},

            {"channel": 1, 
            "rssi": -75, 
            "bandwidth": 20,
            "type": 'A'},

            {"channel": 13, 
            "rssi": -68, 
            "bandwidth": 20,
            "type": 'A'},

    		{"channel": 13, 
            "rssi": -78, 
            "bandwidth": 20,
            "type": 'A'},

        	{"channel": 11, 
            "rssi": -75, 
            "bandwidth": 20,
            "type": 'A'},

            {"channel": 10, 
            "rssi": -85, 
            "bandwidth": 20,
            "type": 'A'},

        	{"channel": 1, 
            "rssi": -78, 
            "bandwidth": 20,
            "type": 'A'},

            {"channel": 1, 
            "rssi": -87, 
            "bandwidth": 20,
            "type": 'A'},

            {"channel": 11, 
            "rssi": -87, 
            "bandwidth": 20,
            "type": 'A'},]


a = [ round(channel_quality(channel, cq_data, remove_radar=True), 2) for channel in range(1, 13)]
print(a)