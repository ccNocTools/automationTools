
"""Wrapper containing commands that will be invoked during ssh sessions. Each operating
system that will require ssh will require its own class with appropriate functions
"""


class CiscoNexusCommands:

    """Cisco NX-os command used to confirm the presence of a specific mac address. Function
    requires a single argument: mac_address
    @precondition: mac_address
    """
    def find_mac_address(mac_address):
        return "show mac address-table | include {}".format(mac_address)

    """Cisco NX-os command used to determine if a specified interface is a trunk port
    Requires a single argument: interface
    """
    def is_interface_trunk(interface):
        return "show running-config interface {} | begin trunk".format(interface)

    """Cisco NX-os command used to determine the ip address of the trunk port
    requires a single argument: interface
    """
    def neighbor_interface_detail(interface):
        return "show cdp neighbor interface {} detail".format(interface)

