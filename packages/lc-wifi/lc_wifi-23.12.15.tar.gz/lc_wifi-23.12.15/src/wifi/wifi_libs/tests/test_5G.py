import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
from baseG5 import channel_quality, greedy_calc
import BruteForceG5 as BFG5

radars_l = [{'cpeid': '001095-14B7F887C74E', 'channel': 36, 'bandwidth': 40,
             'possible_channels': [36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161]},
            {'cpeid': '001095-B42A0EE13276', 'channel': 36, 'bandwidth': 40,
             'possible_channels': [36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161]},
            {'cpeid': '001095-48003378DC9C', 'channel': 36, 'bandwidth': 40,
             'possible_channels': [36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161]}]

devices_l = [{'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '001095-B42A0EE13276', 'channel': 36, 'rssi': -73,
              'channel_width': 40},
             {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '001095-48003378DC9C', 'channel': 36, 'rssi': -73,
              'channel_width': 40},
             {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '001095-14B7F887C74E', 'channel': 36, 'rssi': -73,
              'channel_width': 40},
             {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '001095-48003378DC9C', 'channel': 36, 'rssi': -73,
              'channel_width': 40},
             {'radar_cpeid': '001095-48003378DC9C', 'dev_cpeid': '001095-14B7F887C74E', 'channel': 36, 'rssi': -73,
              'channel_width': 40},
             {'radar_cpeid': '001095-48003378DC9C', 'dev_cpeid': '001095-B42A0EE13276', 'channel': 36, 'rssi': -73,
              'channel_width': 40},
             {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 149, 'rssi': -53, 'channel_width': 40},
             {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 157, 'rssi': -73, 'channel_width': 20},
             {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 44, 'rssi': -46, 'channel_width': 20},
             {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 36, 'rssi': -93, 'channel_width': 80},
             {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '', 'channel': 161, 'rssi': -103, 'channel_width': 40},
             {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '', 'channel': 40, 'rssi': -53, 'channel_width': 40}, ]


class TestBase(unittest.TestCase):
    def test_channel_quality(self):
        """ test checks channel quality calculation """

        # No devices, just radar
        self.assertEqual(channel_quality(48, [], 40), 1.0)

        data = [{"channel": 36, "rssi": -46, "bandwidth": 40, "type": None},
                {"channel": 40, "rssi": -78, "bandwidth": 80, "type": None},
                {"channel": 44, "rssi": -46, "bandwidth": 20, "type": None},
                {"channel": 161, "rssi": -46, "bandwidth": 20, "type": None},
                {"channel": 159, "rssi": -46, "bandwidth": 40, "type": None}]

        self.assertEqual(channel_quality(48, data, 40), 0.7359647210343864)

    def test_greedy_calc(self):
        radar = radars_l[0]
        environment = [dev for dev in devices_l if dev['radar_cpeid'] == radar["cpeid"]]

        best_chan, best_qual = greedy_calc(radar, environment)
        self.assertEqual((best_chan, best_qual), (52, 0.9429948149941849))

    def test_bw_select(self):
        radar = radars_l[0]
        environment = [dev for dev in devices_l if dev['radar_cpeid'] == radar["cpeid"]]

        best_chan, best_qual, best_bw = greedy_calc(radar, environment, change_bw=True)
        self.assertEqual((best_chan, best_qual, best_bw), (60, 1.0, 40))


class TestBruteForce(unittest.TestCase):
    def test_BF_5G_run(self):
        self.assertEqual(BFG5.run(radars_l, devices_l),
                         [('001095-14B7F887C74E', 1., 52),
                          ('001095-B42A0EE13276', 1., 149),
                          ('001095-48003378DC9C', 1., 36)])

        self.assertEqual(BFG5.run(radars_l, devices_l, what_cmbs='channel quality based'),
                         [('001095-14B7F887C74E', 1.0, 52),
                          ('001095-B42A0EE13276', 0.99070674, 44),
                          ('001095-48003378DC9C', 1.0, 36)])


if __name__ == '__main__':
    unittest.main()
