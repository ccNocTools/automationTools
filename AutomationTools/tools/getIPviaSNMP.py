from pysnmp.hlapi import *
import re
import sys

""" Function to snmp into switch and get OS. This will require an snmp engine
    Will take a community string and ipaddress or hostname as arguments. If 2960 switch Function
    will return as a hex value which will need to be decoded for readability. If it is a nexus
    switch the return value is in acsii. Need to check via an if statement
    for testing purposes we are printing results.
"""


def findOS(community_string, hostname):

    try:
        get = getCmd(SnmpEngine(),
                     CommunityData(community_string),
                     UdpTransportTarget((hostname, 161)),
                     ContextData(),
                     ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
        target = str(next(get))
        print(target)
        if target[:11] == "Cisco NX-OS":
            try:
                os = target[:11]
                print (os)
                os_version = re.search('(?<= Version\s).*,', target).group(0).replace(',', '')
                return (os + " " + os_version)
            except:
                return ("No OS found")
        else:
            hex_value = re.search('(?<= hexValue=\')[A-Fa-f0-9]*', target)
            try:
                print(hex_value)
                ascii_value = bytearray.fromhex(hex_value.group()).decode()
                print(ascii_value)
                os = ascii_value[:9]
                os_version = re.search('(?<= Version\s).*,', ascii_value).group(0).replace(',', '')
                return (os + " " + os_version)
            except:
                return ("No OS found")
    except:
        return ("Unable to connect")


#findOS("CCsolarRo", "2.1.1.1")
#findOS("CCsolarRo", "10.0.0.1")
#findOS("CCsolarRo", "10.0.5.6")
