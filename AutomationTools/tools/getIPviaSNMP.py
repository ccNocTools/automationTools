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

    get = getCmd(SnmpEngine(),
                 CommunityData(community_string),
                 UdpTransportTarget((hostname, 161)),
                 ContextData(),
                 ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

    target = str(next(get))
    hexvalue = re.search('(?<= hexValue=\')..................', target)
    os = re.search('(?<=Cisco\s).....', target)

    if hexvalue:
        return(bytearray.fromhex(hexvalue.group()).decode())
    elif os:
        return(os.group())
    else:
        return("no os found")

