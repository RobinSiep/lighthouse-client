import psutil


class Disk:
    def __init__(self, device, mount_point):
        self.device = device
        self.mount_point = mount_point

    def get_usage(self):
        return psutil.disk_usage(self.mount_point)

    def get_total(self):
        return self.get_usage().total

    def get_used(self):
        return self.get_usage().used

    def get_percent(self):
        return self.get_usage().percent

    @property
    def __dict__(self):
        return {
            'device': self.device,
            'mount_point': self.mount_point,
            'total': self.get_total(),
            'used': self.get_used(),
            'percent': self.get_percent()
        }


def get_disks():
    return [Disk(**partition) for partition in get_disk_partitions()]


def get_disk_partitions():
    return [parse_disk_partition(partition) for partition in
            psutil.disk_partitions()]


def parse_disk_partition(partition):
    try:
        return {
            'device': partition.device,
            'mount_point': partition.mountpoint
        }
    except AttributeError:
        raise ValueError("Given disk partition is invalid or malformatted")
