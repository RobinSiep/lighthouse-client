import argparse
import asyncio

import socketio

from lighthouseclient.lib.exceptions import AuthenticationException
from lighthouseclient.lib.oauth import OAuthClient
from lighthouseclient.lib.system import System
from lighthouseclient.lib.system.disks import get_disks
from lighthouseclient.lib.system.networking import Network

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()

parser = argparse.ArgumentParser()
parser.add_argument('destination', type=str,
                    help="the lighthouse-master to connect to")
parser.add_argument('client_id', type=str,
                    help="OAuth client id")
parser.add_argument('client_secret', type=str,
                    help="OAuth client secret")
parser.add_argument('--interval', type=int, default=3,
                    help="Interval between each emit of system info")
args = parser.parse_args()


@sio.event
async def connect():
    print("connection established")
    await identify()


async def identify():
    await sio.emit('identify', {
        'name': Network.get_hostname(),
        'internal_ip': Network.get_internal_ip_address(),
        'external_ip': Network.get_external_ip_address(),
        'mac_address': System.get_mac_address()
    })


@sio.event
async def sys_info():
    await sio.emit('sys_info', {
        'cpu': System.get_cpu_percent(),
        'load_average': System.get_load_average(),
        'cores': System.core_count,
        'memory': System.memory,
        'memory_used': System.get_memory_used(),
        'disks': [disk.__dict__ for disk in get_disks()]
    })

    # We constantly want to be emitting sys_info
    await sio.sleep(args.interval)
    await sys_info()


@sio.event
def disconnect():
    print("disconnected from server")


async def main():
    try:
        access_token = OAuthClient(
            args.destination,
            args.client_id,
            args.client_secret
        ).get_new_access_token()
    except AuthenticationException:
        print("Something went wrong authentication to Lighthouse. "
              "Please verify your credentials")
        return

    await sio.connect(
        args.destination,
        headers={
            'User-Agent': "Lighthouse Client",
            'Authorization': f"Bearer {access_token}"
        }
    )
    await sio.wait()


loop.run_until_complete(main())
