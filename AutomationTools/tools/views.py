from django.shortcuts import render
from .getIPviaSNMP import findOS


def get_os(request):
    return render(request, 'tools/get_os.html')


def find_os(request):
    community_string = request.POST['community_string']
    ip_address = request.POST['ip_address']

    context = {
        'community_string': community_string,
        'ip_address': ip_address,
        'os': findOS(community_string, ip_address)
    }

    return render(request, 'tools/get_os.html', context)
