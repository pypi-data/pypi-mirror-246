import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
from baseG2 import channel_quality, MIN_RSSI


class TestExample(unittest.TestCase):

    def test_channel_quality(self):
        """ test checks channel quality calculation """

        # No devices, just radar
        self.assertEqual(channel_quality(1, []), 1.0)
        # No devices, no radar
        self.assertEqual(channel_quality(1, [], remove_radar=False), 1.0)

        data = [{"channel": 1, "rssi": -46, "bandwidth": 20, "type": None},
                {"channel": 1, "rssi": -78, "bandwidth": 20, "type": None},
                {"channel": 4, "rssi": -46, "bandwidth": 20, "type": None},
                {"channel": 5, "rssi": -46, "bandwidth": 20, "type": None}]

        self.assertEqual(channel_quality(1, data), 0.716661532873579)
        self.assertEqual(channel_quality(1, data, remove_radar=False), 0.8112229866176992)


if __name__ == '__main__':
    unittest.main()
