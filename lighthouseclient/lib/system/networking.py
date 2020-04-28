from socket import gethostname

import requests
from netifaces import ifaddresses, interfaces, AF_INET

EXTERNAL_IP_SERVICE = 'https://api.ipify.org'


class Network:
    @staticmethod
    def get_hostname():
        return gethostname()

    @staticmethod
    def get_network_interface(interface_name):
        try:
            interface = ifaddresses(interface_name)[AF_INET][0]
            interface['name'] = interface_name
            return interface
        except KeyError as e:
            offending_key = e.args[0]
            if offending_key == AF_INET:
                raise KeyError("No AF_INET found in interface")
            raise e

    @staticmethod
    def get_network_interfaces():
        network_interfaces = []
        for interface_name in interfaces():
            try:
                network_interfaces.append(
                    Network.get_network_interface(interface_name)
                )
            except KeyError:
                pass

        return network_interfaces

    @staticmethod
    def get_external_ip_address():
        return requests.get(EXTERNAL_IP_SERVICE).text
