import argparse

import socketio

from lighthouseclient.lib.system import System
from lighthouseclient.lib.system.disks import get_disks
from lighthouseclient.lib.system.networking import Network


sio = socketio.Client()

parser = argparse.ArgumentParser()
parser.add_argument('destination', type=str,
                    help="the lighthouse-master to connect to")


@sio.event
def connect():
    print("connection established")
    identify()


def identify():
    sio.emit('identify', {
        'name': Network.get_hostname(),
        'internal_ip': Network.get_internal_ip_address(),
        'external_ip': Network.get_external_ip_address()
    })


@sio.event
def sys_info(*args):
    sio.emit('sys_info', {
        'cpu': System.get_cpu_percent(),
        'load_average': System.get_load_average(),
        'cores': System.core_count,
        'memory': System.memory,
        'memory_used': System.get_memory_used(),
        'disks': [disk.__dict__ for disk in get_disks()]
    })


@sio.event
def disconnect():
    print("disconnected from server")


def main():
    args = parser.parse_args()

    sio.connect(
        args.destination,
        headers={
            'User-Agent': "Lighthouse Client"
        }
    )
    sio.wait()


main()
