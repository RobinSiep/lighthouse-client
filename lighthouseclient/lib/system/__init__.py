import psutil


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

    def get_memory_used():
        return psutil.virtual_memory().used
