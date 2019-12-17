import argparse
from socket import gethostbyname, gethostname

import psutil
import requests
import socketio

EXTERNAL_IP_SERVICE = 'https://api.ipify.org'

sio = socketio.Client()

parser = argparse.ArgumentParser()
parser.add_argument('destination', type=str,
                    help="the lighthouse-master to connect to")


@sio.event
def connect():
    print('connection established')
    identify()


def identify():
    hostname = gethostname()
    # Rough implementation, results may differ by platform
    internal_ip_address = gethostbyname(hostname)

    sio.emit('identify', {
        'name': hostname,
        'internal_ip': internal_ip_address,
        'external_ip': requests.get(EXTERNAL_IP_SERVICE).text
    })


@sio.event
def sys_info(_):
    cores = psutil.cpu_count()
    load_avg = [x / psutil.cpu_count() * 100 for x in
                psutil.getloadavg()]
    memory = psutil.virtual_memory()
    return {
        'cpu': psutil.cpu_percent(),
        'load_average': load_avg,
        'cores': cores,
        'memory': memory.total,
        'memory_used': memory.used,
        'disks': get_disks_info()
    }


def get_disks_info():
    partitions_with_disk_usage = []

    for partition in get_disk_partitions():
        disk_usage = psutil.disk_usage(partition['mount_point'])
        partition['usage'] = {
            'total': disk_usage.total,
            'used': disk_usage.used,
            'percent': disk_usage.percent
        }
        partitions_with_disk_usage.append(partition)

    return partitions_with_disk_usage


def get_disk_partitions():
    return [parse_disk_partition(partition) for partition in
            psutil.disk_partitions()]


def parse_disk_partition(partition):
    return {
        'device': partition.device,
        'mount_point': partition.mountpoint
    }


@sio.event
def disconnect():
    print('disconnected from server')


def main():
    args = parser.parse_args()

    sio.connect(args.destination)
    sio.wait()


main()
