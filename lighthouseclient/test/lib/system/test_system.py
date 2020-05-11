from unittest import TestCase
from unittest.mock import patch

from lighthouseclient.lib.system import System


class TestGetCpuPercent(TestCase):
    @patch('psutil.cpu_percent', return_value=44, autospec=True)
    def test_correct_percent(self, mock):
        from lighthouseclient.lib.system import System
        self.assertEqual(System.get_cpu_percent(), 44)
        self.assertNotEqual(System.get_cpu_percent(), 45)


class TestGetLoadAverage(TestCase):
    @patch('psutil.getloadavg', return_value=[20, 25, 50], autospec=True)
    def test_load_average(self, mock_2):
        System.core_count = 4
        average_percent = [x / 4 * 100 for x in [20, 25, 50]]
        self.assertEqual(System.get_load_average(), average_percent)


class TestMemoryUsed(TestCase):
    def test_correct_memory_used(self):
        class MockMemory:
            used = 100

        with patch('psutil.virtual_memory', return_value=MockMemory(),
                   autospec=True):
            self.assertEqual(System.get_memory_used(), 100)
