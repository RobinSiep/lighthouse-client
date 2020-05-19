import re
from subprocess import call

from lighthouseclient import sio
from lighthouseclient.lib.system.networking import PortScanner

MAC_ADDRESS_PATTERN = '[0-9A-F]{2}([-:]?)[0-9A-F]{2}(\\1[0-9A-F]{2}){4}$'


@sio.event
def send_wake_on_LAN_packet(recipient_mac):
    if not re.match(MAC_ADDRESS_PATTERN, recipient_mac):
        raise ValueError("recipient_mac is not a valid MAC address.")
    call(('wakeonlan', recipient_mac))


@sio.event
async def emit_ports():
    print('called')
    test = await PortScanner().scan()
    print('done')
    return test
