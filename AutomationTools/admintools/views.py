from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from home.usermod import User_Mod
from tools.models import Community_String, Device_Database
from tools.getIPviaSNMP import findOS


"""View for main users page. If user is not admin, will redirect to home."""


def users(request):
    if not request.user.is_superuser:
        return redirect("/")
    all_users = User.objects.order_by('username')

    context = {
        'all_users': all_users
    }
    return render(request, 'admintools/users.html', context)


"""View for new user form on users page. Uses User_Mod class to create new user and checks 'is_admin' checkbox from
form. Initial password is the same as username. If user is not admin, will redirect to home."""


def new_user(request):
    if not request.user.is_superuser:
        return redirect("/")
    username = request.POST['username']
    try:
        is_admin = bool(request.POST['is_admin'])
    except:
        is_admin = False

    user = User_Mod.create_user(username, is_admin)
    context = {
        'all_users': User.objects.order_by('username'),
        'message': user['message']
    }

    return render(request, "admintools/users.html", context)


"""View for modify user form on users page. First, a list of all user objects is created (all_users). Then the list is
scanned through and a new list (user_list) is created for all the users who were selected on the form. Then if the
new list is not empty the desired action is checked and executed using the User_Mod class.
If user is not admin, will redirect to home."""


def modify_user(request):
    if not request.user.is_superuser:
        return redirect("/")

    all_users = User.objects.order_by('username')
    user_list = []
    context = {
        'all_users': all_users,
        'message': ""
    }
    for user in all_users:
        username = user.username
        try:
            if bool(request.POST[username]):
                user_list.append(username)
        except:
            pass

    if len(user_list) != 0:
        if request.POST['action'] == "Delete Users":
            result = User_Mod.delete_user(user_list)
        elif request.POST['action'] == "Disable Users":
            result = User_Mod.disable_user(user_list)
        elif request.POST['action'] == "Enable Users":
            result = User_Mod.enable_user(user_list)
        elif request.POST['action'] == "Reset Users":
            result = User_Mod.reset_user(user_list)
        context['all_users'] = User.objects.order_by('username')
        context['message'] = result['message']
    else:
        context['message'] = "Please choose user(s) to modify."

    return render(request, 'admintools/users.html', context)


"""View to see and change the community string. If the community string exists, the HTTP render will include that info.
If not, it will send "No community string found." Then it checks to see if a new value for the community string has
been put in by the user. If so, the new community string is changed and a confirmation message is included.
If user is not admin, will redirect to home."""


def community_string(request):
    if not request.user.is_superuser:
        return redirect("/")

    context = {
        "community_string": "",
        "message": ""
    }
    try:
        com_str = Community_String.objects.get().community_string
    except:
        com_str = "No community string found."

    try:
        new_com_str = request.POST['community_string']
        try:
            u = Community_String.objects.get()
        except:
            u = Community_String.objects.create()
        u.community_string = new_com_str
        u.save()
        com_str = new_com_str
        context['message'] = "Community string changed successfully."
    except:
        pass

    context['community_string'] = com_str
    return render(request, "admintools/community_string.html", context)


"""View to display and modify the device database. First it check to see if a new device is being added. If so, it takes
the required information from the form and creates a new Device_Database object.
Then it checks to see if any device checkbox is selected for modification or deletion. A list of all devices is
created (device_list). Then the list is scanned through twice, first to check if an existing device is being modified,
and again to check if any devices are being deleted. The desired action is then performed. Finally, a new device_list
is created to send to the rendered page to be displayed in the table. If user is not admin, will redirect to home."""


def device_database(request):
    if not request.user.is_superuser:
        return redirect("/")

    context = {
        'device_list': "",
        'message': ""
    }
    device_list = Device_Database.objects.all()

    try:
        try:
            com_str = Community_String.objects.get().community_string
        except:
            context['message'] = "Please set Community String."
            return render(request, "admintools/device_database.html", context)
        device_name = request.POST["device_name"]
        ip_address = request.POST["ip_address"]
        device_type = request.POST["device_type"]
        os_version = findOS(com_str, request.POST["ip_address"])
        try:
            for device in device_list:
                if ip_address == device.ip_address:
                    context['message'] = "Device already exists."
                    context['device_list'] = device_list
                    return render(request, "admintools/device_database.html", context)
        except:
            pass
        new_device = Device_Database.objects.create()
        new_device.device_name = device_name
        new_device.ip_address = ip_address
        new_device.os_version = os_version
        new_device.device_type = device_type
        new_device.save()
        context['message'] = "Device added successfully."
    except:
        pass
    try:
        for device in device_list:
            new_device_name = request.POST[device.ip_address + '_name_box']
            if new_device_name != '':
                edited_device = Device_Database.objects.get(ip_address=device.ip_address)
                edited_device.device_name = new_device_name
                edited_device.save()
                context['message'] = "Settings changed successfully."
    except:
        pass

    try:
        for device in device_list:
            new_device_type = request.POST[device.ip_address + '_type_input_box']
            if new_device_type != '':
                edited_device = Device_Database.objects.get(ip_address=device.ip_address)
                edited_device.device_type = new_device_type
                edited_device.save()
                context['message'] = "Settings changed successfully."
    except:
        pass

    for device in device_list:
        try:
            if bool(request.POST[device.ip_address+"_box"]):
                Device_Database.objects.get(ip_address=device.ip_address).delete()
            context['message'] = "Devices deleted successfully."
        except:
            pass
    device_list = Device_Database.objects.order_by('ip_address')
    context['device_list'] = device_list

    return render(request, "admintools/device_database.html", context)


def reset_all(request):
    Community_String.objects.all().delete()
    Device_Database.objects.all().delete()
    User.objects.all().delete()

    return redirect("/")
