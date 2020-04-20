import argparse

import socketio

from lighthouseclient.lib.oauth import OAuthClient
from lighthouseclient.lib.system import System
from lighthouseclient.lib.system.disks import get_disks
from lighthouseclient.lib.system.networking import Network


sio = socketio.Client()

parser = argparse.ArgumentParser()
parser.add_argument('destination', type=str,
                    help="the lighthouse-master to connect to")
parser.add_argument('client_id', type=str,
                    help="OAuth client id")
parser.add_argument('client_secret', type=str,
                    help="OAuth client secret")


@sio.event
def connect():
    print("connection established")
    identify()


def identify():
    sio.emit('identify', {
        'name': Network.get_hostname(),
        'internal_ip': Network.get_internal_ip_address(),
        'external_ip': Network.get_external_ip_address(),
        'mac_address': System.get_mac_address()
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
    access_token = OAuthClient(
        args.destination,
        args.client_id,
        args.client_secret
    ).get_new_access_token()

    sio.connect(
        args.destination,
        headers={
            'User-Agent': "Lighthouse Client",
            'Authorization': f"Bearer {access_token}"
        }
    )
    sio.wait()


main()
