import psutil
import re
import uuid


class System:
    core_count = psutil.cpu_count()
    memory = psutil.virtual_memory().total

    @staticmethod
    def get_cpu_percent():
        return psutil.cpu_percent()

    @staticmethod
    def get_load_average():
        return[x / System.core_count * 100 for x in
               psutil.getloadavg()]

    @staticmethod
    def get_memory_used():
        return psutil.virtual_memory().used

    @staticmethod
    def get_mac_address():
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))
