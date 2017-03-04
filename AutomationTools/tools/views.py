from django.shortcuts import render
from .getIPviaSNMP import findOS
from .locateHostOnNetwork import FindDevice, SnmpToAccessPort
from .models import Community_String, Device_Database


def get_os(request):
    try:
        com_str = Community_String.objects.get().community_string
    except:
        com_str = ""
    context = {
        "community_string": com_str
    }
    return render(request, 'tools/get_os.html', context)


def find_os(request):
    community_string = request.POST['community_string']
    ip_address = request.POST['ip_address']

    context = {
        'community_string': community_string,
        'ip_address': ip_address,
        'os': findOS(community_string, ip_address)
    }

    return render(request, 'tools/get_os.html', context)


def locate_host(request):
    test = "fail"
    try:
        mac_address = request.POST['mac_address_1'] + "." + request.POST['mac_address_2'] + "." + request.POST['mac_address_3']
        host_address = request.POST['host_switch_ip']
        username = request.POST['username']
        password = request.POST['password']
        community_string = request.POST['community_string']

        f = FindDevice(host_address, mac_address, username, password)

        next_hop_host = f.locate_vlan_for_mac_address()[0]
        vlan = f.locate_vlan_for_mac_address()[1]
        test = vlan + " " + next_hop_host

    except:
        pass

    device_list = []
    for d in Device_Database.objects.all():
        if d.device_type != "Access":
            device_list.append(d)
    context = {
        'device_list': device_list,
        'community_string': Community_String.objects.get().community_string,
        'message': test
    }

    return render(request, 'tools/locate_host.html', context)
