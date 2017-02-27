from django.shortcuts import render
from .getIPviaSNMP import findOS
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
    device_list = []
    for d in Device_Database.objects.all():
        if d.device_type != "Access":
            device_list.append(d)
    context = {
        'device_list': device_list,
        'community_string': Community_String.objects.get().community_string,
        'message': ""
    }

    return render(request, 'tools/locate_host.html', context)
