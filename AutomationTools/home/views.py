from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .usermod import User_Mod

def index(request):

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


def initialize(request):
    username = request.POST['username']
    email = request.POST['email_address']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    user = User_Mod.create_user(username, True)
    if user['result']:
        user = User_Mod.set_password(username, username, password, confirm_password)
        if user['result']:
            user = User_Mod.set_email(username, password, email)
            if user['result']:
                context = {
                    'all_users': User.objects.all(),
                    'message': "Admin user created successfully",
                    'is_admin': True
                }
                return render(request, "admintools/index.html", context)
    context = {
        'error': user['message']

    }
    return render(request, "home/setup.html", context)


def setup(request, username, email, error):
    context = {
        'username': username,
        'email_address': email,
        'error': error
    }
    return render(request, "home/setup.html", context)


def login_page(request, message):
    context = {
        'message': message,
        'title': 'Login'
    }
    return render(request, "home/login.html", context)


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
            'title': "Login"
        }
        return render(request, "home/login.html", context)


def logout(request):
    auth.logout(request)
    return redirect("/")


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
    user = User_Mod.set_password(username, username, password, confirm_password)
    if not user['result']:
        context['message'] = user['message']
        return render(request, "home/register.html", context)
    context['message'] = "User registered successfully."

    return render(request, "home/home.html", context)
