import asyncio
from unittest import TestCase
from unittest.mock import patch

from lighthouseclient.lib.system.networking import PortScanner
from lighthouseclient.test import async_run_loop


class TestPortScannerScan(TestCase):
    @async_run_loop
    async def test_scan_success(self):
        with patch('asyncio.open_connection', new=lambda host, port:
                   open_connection_mock(host, port, [80, 500, 501])):
            open_ports = await PortScanner().scan(500)

        self.assertIn(80, open_ports)
        self.assertIn(500, open_ports)
        self.assertNotIn(501, open_ports)
        self.assertEqual(len(open_ports), 2)


async def open_connection_mock(host, port, open_ports):
    if port in open_ports:
        return
    else:
        raise asyncio.TimeoutError()
