from django.test import TestCase

from .locateHostOnNetwork import FindDevice, SnmpToAccessPort


class locateHostTestCase(TestCase):

    com_str = snmp_version = password = username = mac_address = host = None

    def setup(self):
        host = input("Host: ")
        mac_address = input("Mac Address: ")
        username = input("Username: ")
        password = input("Password: ")
        snmp_version = "2c"
        com_str = input("Community String: ")

    def find_device(self):
        fd = FindDevice(host, mac_address, username, password)
        fd_result = fd.locate_vlan_for_mac_address()
        next_hop_host = fd_result[0]
        print(next_hop_host)
        vlan = fd.locate_vlan_for_mac_address()[1]
        print(vlan)

    def snmp_to_access_port(self):
        stap = SnmpToAccessPort(snmp_version, com_str, mac_address, vlan, next_hop_host)
        is_trunk = True
        while is_trunk:
            bridge_port = stap.get_bridge_port()
            if_index = stap.get_ifindex(bridge_port)
            interface = stap.get_interface(if_index)
            is_trunk = stap.is_interface_trunk(if_index)
            print (interface, is_trunk)
