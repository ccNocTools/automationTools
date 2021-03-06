from django.shortcuts import render
from .getIPviaSNMP import findOS
from .locateHostOnNetwork import FindDevice, SnmpToAccessPort
from .models import Community_String, Device_Database
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseBadRequest


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

        print (f)

        nhv = f.locate_vlan_for_mac_address()
        print("nhv:")
        print (nhv)
        next_hop_host = nhv[0]
        print("next hop ip:")
        print (next_hop_host)
        print("vlan:")
        vlan = nhv[1]
        print (vlan)

        test = "vlan succsessful"


        d = SnmpToAccessPort("2c", community_string, mac_address, vlan, next_hop_host)

        is_trunk = True

        while is_trunk:
            bridge_port = d.get_bridge_port()
            if_index = d.get_ifindex(bridge_port)
            interface = d.get_interface(if_index)
            is_trunk = d.is_interface_trunk(if_index)
        test = interface + "  " + if_index + " " + bridge_port

    except:
        pass

    device_list = []
    for d in Device_Database.objects.order_by('ip_address'):
        if d.device_type != "Access":
            device_list.append(d)
    context = {
        'device_list': device_list,
        'community_string': Community_String.objects.get().community_string,
        'message': test
    }

    return render(request, 'tools/locate_host.html', context)


def locate_host_ajax(request):
    test = "Host not found"
    if request.is_ajax():
        try:
            mac_address = request.GET.get('mac_address_1') + request.GET.get('mac_address_2') + \
                          request.GET.get('mac_address_3', None)
            host_address = request.GET.get('host_switch_ip', None)
            username = request.GET.get('username', None)
            password = request.GET.get('password', None)
            community_string = request.GET.get('community_string', None)

            f = FindDevice(host_address, mac_address, username, password)

            next_hop_host = f.locate_vlan_for_mac_address()[0]
            vlan = f.locate_vlan_for_mac_address()[1]

            d = SnmpToAccessPort("2c", community_string, mac_address, vlan, next_hop_host)

            is_trunk = True

            while is_trunk:
                bridge_port = d.get_bridge_port()
                if_index = d.get_ifindex(bridge_port)
                interface = d.get_interface(if_index)
                is_trunk = d.is_interface_trunk(if_index)
            test = interface + "  " + if_index + " " + bridge_port

        except:
            pass

    device_list = []
    for d in Device_Database.objects.order_by('ip_address'):
        if d.device_type != "Access":
            device_list.append(d)
    context = {
        'device_list': device_list,
        'community_string': Community_String.objects.get().community_string,
        'message': test
    }
    response = HttpResponse()
    response['device_list'] = device_list
    response['community_string'] = Community_String.objects.get().community_string
    response['message'] = test
    return render_to_response(request, 'tools/locate_host.html', context)
