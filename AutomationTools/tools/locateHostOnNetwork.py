import subprocess
import paramiko
import socket
import re
from .regX import CiscoNexusRegX, SNMPCiscoIOSRegX
from .sshCommands import CiscoNexusCommands
from .snmpCommands import CiscoIOSSNMP


class FindDevice:

    def __init__(self, host, mac_address, username, password):
        self.mac_address = mac_address
        self.username = username
        self.host = host
        self.password = password
        self.client = paramiko.SSHClient()
        self.cisco_command = CiscoNexusCommands
        self.regx = CiscoNexusRegX

    """If you do not know the vlan on the port that your device is plugged into
    we need to ssh into the switch and evaluate the mac address table no good way
    to do this with snmp
    """
    def locate_vlan_for_mac_address(self):

        try:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.host, 22, self.username, self.password)
            stdin, stdout, stderr = self.client.exec_command(self.cisco_command.find_mac_address(
                                                             self.mac_address))
            # print (stdout)

            if stdout:
                for line in stdout.readlines():
                    interface = re.search(self.regx.filter_interface(), line)  # grab interface name
                    vlan = re.search(self.regx.filter_vlan(), line)  # grab vlan
                stdin, stdout, stderr = self.client.exec_command(self.cisco_command.
                                                                 is_interface_trunk(
                                                                  interface.group()))

                """If the above statement results in stdout != None than it is indeed a
                trunk port if stdout == None then the interface is in access mode
                """
                if stdout:
                    stdin, stdout, stderr = self.client.exec_command(self.cisco_command.
                                                                     neighbor_interface_detail(
                                                                      interface.group()))
                    for line in stdout.readlines():
                        next_switch = re.search(self.regx.filter_neighbor_address(), line)
                        try:
                            if next_switch.group():
                                break
                        except:
                            pass
                    if next_switch.group():
                        return next_switch.group(), vlan.group()
                    else:
                        return "Failed to locate next hop!"
                else:
                    return "Access port found"
            else:
                return "{} not found at {}".format(self.mac_address, self.host)
        except paramiko.AuthenticationException:
            return ''.join(["Bad credentials! failed to connect to ", self.host])
        except (paramiko.SSHException, socket.error) as socket_error:
            return socket_error, ''.join(["Port may be disable or host is down! ", self.host])
        except:
            return "ass"
        self.client.close()


"""From Step 1, the MAC address is:
        17.4.3.1.1.0.0.12.7.172.8 = Hex: 00 00 0C 07 AC 08
    From Step 2, the bridge port tells that the MAC address belongs to bridge port number 13:
        17.4.3.1.2.0.0.12.7.172.8 = 13
    From Step 3, the bridge port number 13 has ifIndex number 2:
        17.1.4.1.2.13 = 2
    From Step 4, the ifIndex 2 corresponds to port Fast Ethernet 0/1:
    ifMIB.ifMIBObjects.ifXTable.ifXEntry.ifName.2 = Fa0/1

    step 5, determine if the port is trunk or access
"""


class SnmpToAccessPort:

    def __init__(self, snmp_version, community_string, mac_address, vlan_id, host):
        self.snmp_version = snmp_version
        self.community_string = community_string
        self.mac_address = mac_address
        self.vlan_id = vlan_id
        self.host = host
        self.snmp = CiscoIOSSNMP
        self.regx = SNMPCiscoIOSRegX

    """snmpwalk -c public@1 crumpy .1.3.6.1.2.1.17.4.3.1.1

    function does little more than provide confirmation that the
    mac address is present and to convert the mac to decimal

    17.4.3.1.1.0.0.12.7.172.8 =  Hex: 00 00 0C 07 AC 08
    17.4.3.1.1.0.1.2.27.80.145 =  Hex: 00 01 02 1B 50 91
    17.4.3.1.1.0.1.3.72.77.90 =  Hex: 00 01 03 48 4D 5A
    17.4.3.1.1.0.1.3.72.221.191 =  Hex: 00 01 03 48 DD BF
    ...
    Note: Provide the appropriate VLAN number after the community string. In this example, it is
    VLAN1.
    """
    def get_mac_interface(self):

        interface_oid = re.search(str(self.regx.filter_OID_snmp_output(self.mac_address)),
                                  str(subprocess.run(self.snmp.get_mac_interface(
                                           self.snmp_version, self.community_string, self.vlan_id,
                                           self.host), stdout=subprocess.PIPE)))
        if interface_oid:
            return interface_oid.group()
        else:
            return "mac not found via snmp"

    """The command lists all MAC addresses that have been
    learned on all ports that belong to VLAN 1.
    Issue this command to determine the bridge port number for VLAN 1:

        snmpwalk -c public@1 crumpy .1.3.6.1.2.1.17.4.3.1.2

    17.4.3.1.2.0.0.12.7.172.8 = 13
    17.4.3.1.2.0.1.2.27.80.128 = 13
    17.4.3.1.2.0.1.2.27.80.145 = 13
    17.4.3.1.2.0.1.2.163.145.225 = 13
    ...
    """
    def get_bridge_port(self):

        interface = re.search(str(self.regx.filter_bridge_port(self.mac_address)),
                              str(subprocess.run(self.snmp.bridge_port(
                                  self.snmp_version, self.community_string, self.vlan_id,
                                  self.host), stdout=subprocess.PIPE)))
        if interface:
            return interface.group()
        else:
            return "mac not found"

    """Note: VLAN 1 is dot1dTpFdbPort , or .1.3.6.1.2.1.17.4.3.1.2.
    Issue this command to map the bridge port to the ifIndex, OID .1.3.6.1.2.1.2.2.1.1:
        snmpwalk -c public@1 crumpy .1.3.6.1.2.1.17.1.4.1.2

    17.1.4.1.2.13 = 2
    17.1.4.1.2.14 = 3
    17.1.4.1.2.15 = 4
    17.1.4.1.2.16 = 5
    This command queries the dot1dBasePortIfIndex, which has OID .1.3.6.1.2.1.17.1.4.1.2.
    """
    def get_ifindex(self, bridge_port_value):

        ifindex = re.search(str(self.regx.filter_ifindex(bridge_port_value)),
                            str(subprocess.run(self.snmp.get_ifindex_value(
                                self.snmp_version, self.community_string, self.vlan_id,
                                self.host), stdout=subprocess.PIPE)))
        if ifindex:
            return ifindex.group()
        else:
            return "index not found"

    """Use the walk command with ifName in order to correlate the ifIndex value with a correct port
    name.

    Issue this command:
    Note: The ifName has OID .1.3.6.1.2.1.31.1.1.1.1.
    snmpwalk -c public@1 crumpy .1.3.6.1.2.1.31.1.1.1.1

    ifMIB.ifMIBObjects.ifXTable.ifXEntry.ifName.1 = VL1
    ifMIB.ifMIBObjects.ifXTable.ifXEntry.ifName.2 = Fa0/1
    ifMIB.ifMIBObjects.ifXTable.ifXEntry.ifName.3 = Fa0/2
    ifMIB.ifMIBObjects.ifXTable.ifXEntry.ifName.4 = Fa0/3
    ifMIB.ifMIBObjects.ifXTable.ifXEntry.ifName.5 = Fa0/4
    ifMIB.ifMIBObjects.ifXTable.ifXEntry.ifName.6 = Fa0/5
    ifMIB.ifMIBObjects.ifXTable.ifXEntry.ifName.7 = Fa0/6
    ...
    Link a MAC address to the port on which the address was learned.
    """
    def get_interface(self, ifindex):

        interface = re.search(str(self.regx.filter_index(ifindex)),
                              str(subprocess.run(self.snmp.get_if_index(
                                  self.snmp_version, self.community_string, self.vlan_id,
                                  self.host), stdout=subprocess.PIPE)))
        if interface:
            return interface.group()
        else:
            return "interface not found"

    """test if ifindex is a trunk
    if value is one it is trunk
    if value is two it is access
    """
    def is_interface_trunk(self, ifindex):

        is_trunk = re.search(str(self.regx.filter_trunk_value(ifindex)),
                             str(subprocess.run(self.snmp.get_trunk(
                                self.snmp_version, self.community_string, self.vlan_id,
                                self.host), stdout=subprocess.PIPE)))
        if is_trunk:
            if is_trunk is 1:
                return True
            else:
                return False
        else:
            return "not found"

"""
host = input("Host: ")
mac_address = input("Mac Address: ")
username = input("Username: ")
password = input("Password: ")
snmp_version = input("SNMP Version: ")
com_str = input("Community String: ")

fd = FindDevice(host, mac_address, username, password)
fd_result = fd.locate_vlan_for_mac_address()
next_hop_host = fd_result[0]
print(next_hop_host)
vlan = fd.locate_vlan_for_mac_address()[1]
print(vlan)
stap = SnmpToAccessPort("2c", com_str, mac_address, vlan, next_hop_host)
is_trunk = True

while is_trunk:
    bridge_port = stap.get_bridge_port()
    if_index = stap.get_ifindex(bridge_port)
    interface = stap.get_interface(if_index)
    is_trunk = stap.is_interface_trunk(if_index)
    print (interface, is_trunk)
"""
