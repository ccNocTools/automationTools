

class CiscoIOSSNMP:

    def get_mac_interface(snmp_version, community_string, vlan, host):
        # return "snmpwalk", "-v" "{}", "-c" "{}" "@" "{}", "{}", ".1.3.6.1.2.1.17.4.3.1.1".format(
            # snmp_version, community_string, vlan, host)
        return "snmpwalk", "-v" + snmp_version, "-c", community_string + "@" + vlan, host,\
            ".1.3.6.1.2.1.17.4.3.1.1"

    def bridge_port(snmp_version, community_string, vlan, host):
        return "snmpwalk", "-v" + snmp_version, "-c", community_string + "@" + vlan, host,\
            ".1.3.6.1.2.1.17.4.3.1.2"

    def get_ifindex_value(snmp_version, community_string, vlan, host):
        return "snmpwalk", "-v" + snmp_version, "-c", community_string + "@" + vlan, host,\
            ".1.3.6.1.2.1.17.1.4.1.2"

    def get_if_index(snmp_version, community_string, vlan, host):
        return "snmpwalk", "-v" + snmp_version, "-c", community_string + "@" + vlan, host,\
            ".1.3.6.1.2.1.2.2.1.2"

    def get_trunk(snmp_version, community_string, vlan, host):
        return "snmpwalk", "-v" + snmp_version, "-c", community_string + "@" + vlan, host,\
            ".1.3.6.1.4.1.9.9.46.1.6.1.1.14"
