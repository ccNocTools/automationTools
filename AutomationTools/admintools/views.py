from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from home.usermod import User_Mod


def index(request):
    if not request.user.is_superuser:
        return redirect("/")
    all_users = User.objects.all();
    context = {
        'all_users': all_users
    }

    return render(request, 'admintools/index.html', context)


def add_user(request):
    if not request.user.is_superuser:
        return redirect("/")
    return render(request, "admintools/adduser.html")


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
        'all_users': User.objects.all(),
        'message': user['message']
    }

    return render(request, "admintools/index.html", context)


def modify_user(request):
    if not request.user.is_superuser:
        return redirect("/")

    all_users = User.objects.all()
    user_list = []
    context = {
        'all_users': all_users,
        'message': ""
    }
    for user in all_users:
        username = user.username
        try:
            if bool(request.POST[username]):
                if username == request.user.username:
                    context['message'] = "Cannot modify currently logged in user."
                    return render(request, 'admintools/index.html', context)
                else:
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

        context['all_users'] = User.objects.all();
        context['message'] = result['message']
    else:
        context['message'] = "Please choose user(s) to modify."

    return render(request, 'admintools/index.html', context)
