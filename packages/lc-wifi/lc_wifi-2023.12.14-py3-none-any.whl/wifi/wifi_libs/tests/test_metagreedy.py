import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import MetaGreedy as MetaG

listRadars_2 = [{'cpeid': '001095-14B7F887C74E', 'channel': 1, 'upper_channel': 13, 'qual_current': 0.13431986290961834,
                 'target_channel': 13},
                {'cpeid': '001095-B42A0EE13276', 'channel': 1, 'upper_channel': 11, 'qual_current': 0.3279201891941372,
                 'target_channel': 3},
                {'cpeid': '001095-48003378DC9C', 'channel': 1, 'upper_channel': 11, 'qual_current': 0.21535009107090458,
                 'target_channel': 6}]
listDevices_2 = [{'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '001095-B42A0EE13276', 'channel': 1, 'rssi': -73,
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

listRadars_5 = [{'cpeid': '001095-14B7F887C74E', 'channel': 36, 'bandwidth': 40,
                 'possible_channels': [36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161]},
                {'cpeid': '001095-B42A0EE13276', 'channel': 36, 'bandwidth': 40,
                 'possible_channels': [36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161]},
                {'cpeid': '001095-48003378DC9C', 'channel': 36, 'bandwidth': 40,
                 'possible_channels': [36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161]}]

listDevices_5 = [{'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '001095-B42A0EE13276', 'channel': 36, 'rssi': -73,
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
                 {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 149, 'rssi': -53,
                  'channel_width': 40},
                 {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 157, 'rssi': -73,
                  'channel_width': 20},
                 {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 44, 'rssi': -46,
                  'channel_width': 20},
                 {'radar_cpeid': '001095-14B7F887C74E', 'dev_cpeid': '', 'channel': 36, 'rssi': -93,
                  'channel_width': 80},
                 {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '', 'channel': 161, 'rssi': -103,
                  'channel_width': 40},
                 {'radar_cpeid': '001095-B42A0EE13276', 'dev_cpeid': '', 'channel': 40, 'rssi': -53,
                  'channel_width': 40}, ]


class TestMetaGreedy(unittest.TestCase):
    def test_run(self):
        data_2 = [('001095-B42A0EE13276', 0.96431743, 10),
                  ('001095-14B7F887C74E', 0.96863787, 13),
                  ('001095-48003378DC9C', 0.99539593, 6)]
        res = MetaG.run(listRadars_2, listDevices_2)
        self.assertEqual(res, data_2)

        data_5 = [('001095-14B7F887C74E', 1, 52),
                  ('001095-B42A0EE13276', 1, 60),
                  ('001095-48003378DC9C', 1, 36)]
        res = MetaG.run(listRadars_5, listDevices_5, use_5G=True)
        self.assertEqual(res, data_5)


if __name__ == '__main__':
    unittest.main()
