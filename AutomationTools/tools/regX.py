

class CiscoNexusRegX:

    def filter_interface():
        return '(?<=F\s\s\s\sF\s\s).*'

    def filter_vlan():
        return '(?<=\*\s)\d+'

    def filter_neighbor_address():
        return '(?<=Address:\s).*'


class SNMPCiscoIOSRegX:

    def filter_OID_snmp_output(mac_address):
        mac_address_edit = mac_address.upper().replace('.', '').replace(':', '')
        return "[0-9-'.']+( = Hex-STRING: {}{} {}{} {}{} {}{} {}{} {}{})".format(
            *mac_address_edit)

    def filter_bridge_port(mac_address_oid):
        mac_address_oid_edit = mac_address_oid.replace('.', '').replace(':', '')
        li = []
        for x in range(0, len(mac_address_oid_edit), 2):
            li.append(mac_address_oid_edit[x] + mac_address_oid_edit[x + 1])
        hex_to_dec = []
        for i in li:
            hex_to_dec.append(int(i, 16))
        return "(?<={}\.{}\.{}\.{}\.{}\.{} = INTEGER: )".format(*hex_to_dec) + "\w+"

    def filter_ifindex(bridge_port_number):
        return "(?<=." + bridge_port_number + "\s=\sINTEGER:\s)\d+"

    def filter_index(ifindex_value):
        return "(?<=." + ifindex_value + "\s=\sSTRING:\s)\S+"

    def filter_trunk_value(ifindex_value):
        return "(?<=." + ifindex_value + "\s=\sINTEGER:\s)\d+"
