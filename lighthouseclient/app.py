import argparse
import asyncio

from lighthouseclient import sio
from lighthouseclient.lib.exceptions import AuthenticationException
from lighthouseclient.lib.oauth import OAuthClient
from lighthouseclient.lib.system import System
from lighthouseclient.lib.system.disks import get_disks
from lighthouseclient.lib.system.networking import Network
from lighthouseclient.machine import *  # noqa
from lighthouseclient.network import *  # noqa

loop = asyncio.get_event_loop()

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

oauth_client = OAuthClient(
    args.destination,
    args.client_id,
    args.client_secret
)

sys_info_task = None


@sio.event
async def connect():
    print("connection established")
    await identify()


async def identify():
    await sio.emit('identify', {
        'name': Network.get_hostname(),
        'network_interfaces': Network.get_network_interfaces(),
        'external_ip': Network.get_external_ip_address(),
        'mac_address': System.get_mac_address()
    })


@sio.event
async def sys_info():
    global sys_info_task
    sys_info_task = asyncio.create_task(start_sys_info_sync())


async def start_sys_info_sync():
    # We constantly want to be emitting sys_info
    while True:
        await emit_sys_info()
        await sio.sleep(args.interval)


async def emit_sys_info():
    await sio.emit('sys_info', {
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
    cancel_sys_info_task()


def cancel_sys_info_task():
    try:
        sys_info_task.cancel()
    except AttributeError:
        # No sys_info_task currently
        pass


async def reconnect(access_token):
    await sio.disconnect()
    cancel_sys_info_task()
    await sio.sleep(3)
    await connect_to_lighthouse(access_token)


async def connect_to_lighthouse(access_token):
    await sio.connect(
        args.destination,
        headers={
            'User-Agent': "Lighthouse Client",
            'Authorization': f"Bearer {access_token}"
        }
    )


async def main():
    try:
        access_token = await oauth_client.get_new_access_token(reconnect)
    except AuthenticationException:
        print("Something went wrong authentication to Lighthouse. "
              "Please verify your credentials")
        return

    await connect_to_lighthouse(access_token)
    while True:
        await sio.wait()

loop.run_until_complete(main())
