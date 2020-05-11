from unittest import TestCase
from unittest.mock import patch

import psutil

from lighthouseclient.lib.system.disks import (
    parse_disk_partition, get_disk_partitions, get_disks, Disk)


class DiskUsageMock:
    def __init__(self, total, used, percent):
        self.total = total
        self.used = used
        self.percent = percent


class TestDiskUsage(TestCase):
    def setUp(self):
        super().setUp()
        self.disk = Disk('/dev/sda1', '/')

    def test_get_usage(self):
        mock = DiskUsageMock(200, 100, 50)
        with patch('psutil.disk_usage', return_value=mock,
                   autospec=True):
            self.assertEqual(self.disk.get_usage(), mock)
            self.assertEqual(self.disk.get_total(), 200)
            self.assertEqual(self.disk.get_used(), 100)
            self.assertEqual(self.disk.get_percent(), 50)


class TestGetDisks(TestCase):
    def test_get_disks(self):
        partitions = psutil.disk_partitions()
        disks = get_disks()

        for i, partition in enumerate(partitions):
            disk = disks[i]
            self.assertIsInstance(disk, Disk)
            self.assertEqual(disk.device, partition.device)
            self.assertEqual(disk.mount_point, partition.mountpoint)


class TestGetDiskPartitions(TestCase):
    def test_get_success(self):
        partitions = psutil.disk_partitions()
        parsed_partitions = get_disk_partitions()

        for i, partition in enumerate(partitions):
            parsed_partition = parsed_partitions[i]
            self.assertEqual(parsed_partition['device'], partition.device)
            self.assertEqual(parsed_partition['mount_point'],
                             partition.mountpoint)


class TestParseDiskPartition(TestCase):
    def test_parse_success(self):
        disk_partition = psutil.disk_partitions()[0]
        parsed_partition = parse_disk_partition(disk_partition)
        self.assertEqual(parsed_partition['device'], disk_partition.device)
        self.assertEqual(parsed_partition['mount_point'],
                         disk_partition.mountpoint)

    def test_parse_unsuccessful(self):
        with self.assertRaises(ValueError):
            parse_disk_partition(None)
