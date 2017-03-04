from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .usermod import User_Mod
from tools.models import Community_String



"""View for home page. Will redirect to registration page if no admin user exists or login page if no user is logged in.
"""


def home(request):

    if request.user.is_authenticated:
        context = {
            'is_admin': str(request.user.is_superuser)
        }
        return render(request, 'home/home.html', context)

    admin_exists = False
    all_users = User.objects.all()
    for user in all_users:
        if user.is_superuser:
            admin_exists = True
            break

    if admin_exists:
        return login_page(request, "")
    else:
        return setup(request, "", "", "")


"""View to perform the initial setup of the app along with the first admin user."""


def initialize(request):
    username = request.POST['username']
    email = request.POST['email_address']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    user = User_Mod.create_user(username, True)
    if user['result']:
        user = User_Mod.set_password(request, username, username, password, confirm_password)
        if user['result']:
            user = User_Mod.set_email(username, password, email)
            if user['result']:
                context = {
                    'all_users': User.objects.all(),
                    'message': "Admin user created successfully",
                    'is_admin': True
                }
                return render(request, "/", context)
    context = {
        'message': user['message']

    }
    return render(request, "home/setup.html", context)


def setup(request, username, email, message):
    context = {
        'username': username,
        'email_address': email,
        'message': message
    }
    return render(request, "home/setup.html", context)


"""View that renders login page."""


def login_page(request, message):
    context = {
        'message': message,
        'title': 'Login'
    }
    return render(request, "home/login.html", context)


"""View that attempts to log the user in. Will redirect to register if the user has not yet registered. If login is
successful, the home page is rendered."""


def login_attempt(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        if request.user.email == "":
            context = {
                'username': request.user.username
            }
            auth.logout(request)
            return render(request, "home/register.html", context)
        return redirect("/home")
    else:
        context = {
            'message': "Incorrect username or password.",
            'title': "Login",
            'username': username
        }
        return render(request, "home/login.html", context)


"""View that logs user out and returns to login page."""


def logout(request):
    auth.logout(request)
    return redirect("/")


"""View to register new user (after it is created by an admin)."""


def register(request):
    username = request.POST['username']
    email = request.POST['email_address']
    context = {
        'message': "",
        'username': username
    }
    if email == '':
        context['message'] = "Please enter a valid email address."
        return render(request, "home/register.html", context)

    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    user = User_Mod.set_email(username, username, email)
    if not user['result']:
        context['message'] = user['message']
        return render(request, "home/register.html", context)
    user = User_Mod.set_password(request, username, username, password, confirm_password)
    if not user['result']:
        context['message'] = user['message']
        return render(request, "home/register.html", context)
    context['message'] = "User registered successfully. Login to continue."

    try:
        community_string = request.POST['community_string']
        n = Community_String.objects.create()
        n.community_string = community_string
        n.save()
    except:
        pass

    return render(request, "home/login.html", context)

"""View to render the user options page as well as check if any changes were made and execute those.
Possible changes include password changes,"""


def user_options(request):
    context = {
        'message': ""
    }
    try:
        user_name = request.POST['user_name']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        context['message'] = User_Mod.set_password(request, user_name, old_password, new_password,
                                                   confirm_password)['message']
    except:
        pass
    return render(request, "home/user_options.html", context)
