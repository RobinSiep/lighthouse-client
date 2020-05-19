import asyncio
from socket import gethostname

import requests
from netifaces import ifaddresses, interfaces, AF_INET

EXTERNAL_IP_SERVICE = 'https://api.ipify.org'


class Network:
    @staticmethod
    def get_hostname():
        return gethostname()

    @staticmethod
    def get_network_interface(interface_name):
        try:
            interface = ifaddresses(interface_name)[AF_INET][0]
            interface['name'] = interface_name
            return interface
        except KeyError as e:
            offending_key = e.args[0]
            if offending_key == AF_INET:
                raise KeyError("No AF_INET found in interface")
            raise e

    @staticmethod
    def get_network_interfaces():
        network_interfaces = []
        for interface_name in interfaces():
            try:
                network_interfaces.append(
                    Network.get_network_interface(interface_name)
                )
            except KeyError:
                pass

        return network_interfaces

    @staticmethod
    def get_external_ip_address():
        return requests.get(EXTERNAL_IP_SERVICE).text


class PortScanner:
    host = '127.0.0.1'
    max_workers = 200

    task_queue = asyncio.Queue(maxsize=max_workers)
    out_queue = asyncio.Queue()
    scan_completed = asyncio.Event()

    def __init__(self, timeout=0.1):
        self.timeout = timeout

    async def scan_port_from_queue(self):
        while True:
            port = await self.task_queue.get()
            conn = asyncio.open_connection(self.host, port)
            try:
                await asyncio.wait_for(conn, self.timeout)
            except asyncio.TimeoutError:
                pass
            else:
                self.out_queue.put_nowait(port)
            finally:
                self.task_queue.task_done()

    async def task_manager(self, max_port):
        for port in range(1, max_port):
            await self.task_queue.put(port)
        self.scan_completed.set()

    async def scan(self, max_port=49152):
        self.scan_completed.clear()
        tasks = [asyncio.create_task(self.task_manager(max_port))]

        for _ in range(self.max_workers):
            tasks.append(asyncio.create_task(self.scan_port_from_queue()))

        await self.scan_completed.wait()
        await self.task_queue.join()

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        open_ports = []
        while self.out_queue.qsize():
            open_ports.append(self.out_queue.get_nowait())

        return open_ports
