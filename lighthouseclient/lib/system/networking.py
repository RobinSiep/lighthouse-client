from socket import gethostbyname, gethostname

import requests

EXTERNAL_IP_SERVICE = 'https://api.ipify.org'


class Network:
    @staticmethod
    def get_hostname():
        return gethostname()

    @staticmethod
    def get_internal_ip_address():
        # Rough implementation, results may differ by platform
        return gethostbyname(Network.get_hostname())

    @staticmethod
    def get_external_ip_address():
        return requests.get(EXTERNAL_IP_SERVICE).text
