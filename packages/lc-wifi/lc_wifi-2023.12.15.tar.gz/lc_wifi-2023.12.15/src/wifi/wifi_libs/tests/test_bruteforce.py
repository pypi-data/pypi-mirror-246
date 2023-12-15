import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from BruteForceG2 import possible_channels_quality

"""
The exposition of the test:
  Three radars.
  They see each other.
  The first has four alien devices: 2, 2, 7, 8 WiFi channels.
  The second has two alien devices: 3, 5 WiFi channels.
  The third has no alien devices.
"""

listRadars = [{'cpeid': '001095-14B7F887C74E', 'channel': 1, 'upper_channel': 13, 'qual_current': 0.13431986290961834,
               'target_channel': 13},
              {'cpeid': '001095-B42A0EE13276', 'channel': 1, 'upper_channel': 11, 'qual_current': 0.3279201891941372,
               'target_channel': 3},
              {'cpeid': '001095-48003378DC9C', 'channel': 1, 'upper_channel': 11, 'qual_current': 0.21535009107090458,
               'target_channel': 6}]
listDevices = [{'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '001095-B42A0EE13276', 'channel': 1, 'rssi': -73,
                'channel_width': 20, 'standard': 4},
               {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '001095-48003378DC9C', 'channel': 1, 'rssi': -73,
                'channel_width': 20, 'standard': 4},
               {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '001095-14B7F887C74E', 'channel': 1, 'rssi': -73,
                'channel_width': 20, 'standard': 4},
               {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '001095-48003378DC9C', 'channel': 1, 'rssi': -73,
                'channel_width': 20, 'standard': 4},
               {'radar_cpeid': '001095-48003378DC9C', 'dev_cpeid': '001095-14B7F887C74E', 'channel': 1, 'rssi': -73,
                'channel_width': 20, 'standard': 4},
               {'radar_cpeid': '001095-48003378DC9C', 'dev_cpeid': '001095-B42A0EE13276', 'channel': 1, 'rssi': -73,
                'channel_width': 20, 'standard': 4},
               {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 2, 'rssi': -73, 'channel_width': 20,
                'standard': 4},
               {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 2, 'rssi': -73, 'channel_width': 20,
                'standard': 4},
               {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 7, 'rssi': -73, 'channel_width': 20,
                'standard': 4},
               {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 8, 'rssi': -73, 'channel_width': 20,
                'standard': 4},
               {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '', 'channel': 3, 'rssi': -73, 'channel_width': 20,
                'standard': 4},
               {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '', 'channel': 5, 'rssi': -73, 'channel_width': 20,
                'standard': 4}, ]


class TestBruteForce(unittest.TestCase):


    def test_possible_channels_quality(self):
        """ test checks """

        data = [('001095-14B7F887C74E', 0.99539593, 13), ('001095-B42A0EE13276', 0.99083406, 9),
                ('001095-48003378DC9C', 1.0, 1)]
        res = possible_channels_quality(listRadars, listDevices)
        self.assertEqual(res, data)

        data = [('001095-14B7F887C74E', 0.99083406, 13), ('001095-B42A0EE13276', 0.95820428, 9),
                ('001095-48003378DC9C', 0.96261592, 9)]
        res = possible_channels_quality(listRadars, listDevices, what_cmbs='channel quality based')
        self.assertEqual(res, data)


if __name__ == '__main__':
    unittest.main()
