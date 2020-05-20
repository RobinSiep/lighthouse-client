import asyncio
import logging
from socket import gethostname

import requests
from netifaces import ifaddresses, interfaces, AF_INET

log = logging.getLogger(__name__)

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
            logging.debug(f"Scanning port {port}")
            try:
                await asyncio.wait_for(conn, self.timeout)
            except (asyncio.TimeoutError, ConnectionRefusedError):
                pass
            except Exception as e:
                log.critical(e, exc_info=True)
            else:
                self.out_queue.put_nowait(port)
            finally:
                self.task_queue.task_done()

    async def task_manager(self, max_port):
        for port in range(1, max_port):
            await self.task_queue.put(port)
        self.scan_completed.set()

    def create_tasks(self):
        for _ in range(self.max_workers):
            yield asyncio.create_task(self.scan_port_from_queue())

    async def complete_tasks(self, tasks):
        await self.scan_completed.wait()
        await self.task_queue.join()

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

    def get_scan_result(self):
        while self.out_queue.qsize():
            yield self.out_queue.get_nowait()

    async def scan(self, max_port=49152):
        self.scan_completed.clear()
        tasks = [asyncio.create_task(self.task_manager(max_port))]
        tasks += list(self.create_tasks())

        log.info("Scanning ports")
        await self.complete_tasks(tasks)

        log.info("Collecting results")
        open_ports = list(self.get_scan_result())

        print(f"open ports: {open_ports}")
        return open_ports
