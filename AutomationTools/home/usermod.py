from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class User_Mod:

    """Returns true if user exists and false if not."""
    def does_user_exist(username):
        return User.objects.filter(username=username).exists()

    """Creates user in User database. Will create admin if is_admin is true, regular user otherwise. The user's default
    password is the same as their username and user will be required to 'register' before being able to log in. This
    will require them to set a password and email address."""
    def create_user(username, is_admin):
        result = {
            'result': False,
            'message': ""
        }

        if User_Mod.does_user_exist(username):
            result['message'] = "Username " + username + " is already in use."
            return result
        if is_admin:
            try:
                User.objects.create_superuser(username, '', username)
                result['result'] = True
                result['message'] = "Admin user created successfully."
            except:
                result['result'] = False
                result['message'] = "Failed to create user."
        else:
            try:
                User.objects.create_user(username, '', username)
                result['result'] = True
                result['message'] = "Standard user created successfully."
            except:
                result['result'] = False
                result['message'] = "Failed to create user."

        return result

    """This will verify the old password, verify that the new password and confirm password match, and then change the
    user's password."""
    def set_password(request, username, old_password, new_password, confirm_password):
        result = {
            'result': False,
            'message': ""
        }

        if not User_Mod.does_user_exist(username):
            result['message'] = "Username " + username + " does not exist."
        else:
            user = User.objects.get(username=username)
            if not user.check_password(old_password):
                result['message'] = "Old password is incorrect."
            elif new_password != confirm_password:
                result['message'] = "Password confirmation does not match new password."
            elif len(new_password) < 8:
                result['message'] = "Password must be 8 characters or longer."
            else:
                try:
                    user.set_password(new_password)
                    user.save()
                    user = authenticate(username = username, password = new_password)
                    login(request, user)
                    result['result'] = True
                    result['message'] = "Password change successful."
                except:
                    result['message'] = "Error changing password."

        return result

    """Sets the users email as long as the password is correct."""
    def set_email(username, password, email):
        result = {
            'result': False,
            'message': ""
        }

        if not User_Mod.does_user_exist(username):
            result['message'] = "Username " + username + " does not exist."
        else:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                result['message'] = "Incorrect password."
            else:
                try:
                    user.email = email
                    user.save()
                    result['result'] = True
                    result['message'] = "Email address change successful."
                except:
                    result['message'] = "Error changing email address."

        return result

    """Takes a list of users and iterates through them to delete each one."""
    def delete_user(user_list):
        result = {
            'result': False,
            'message': ""
        }
        try:
            for username in user_list:
                u = User.objects.get(username=username)
                u.delete()
            result['result'] = True
            result['message'] = "User delete successful."
        except:
            result['message'] = "Error deleting user."

        return result

    """Takes a list of users and iterates over them to disable each one."""
    def disable_user(user_list):
        result = {
            'result': False,
            'message': ""
        }
        try:
            for username in user_list:
                u = User.objects.get(username=username)
                u.is_active = False
                u.save()
            result['result'] = True
            result['message'] = "User disable successful."
        except:
            result['message'] = "Error disabling user."

        return result

    """Takes a list of users and iterates through them to enable each one."""
    def enable_user(user_list):
        result = {
            'result': False,
            'message': ""
        }
        try:
            for username in user_list:
                u = User.objects.get(username=username)
                u.is_active = True
                u.save()
            result['result'] = True
            result['message'] = "User enable successful."
        except:
            result['message'] = "Error enabling user."

        return result

    """Resets user by deleting email and setting password to the same as the username. User will be required to register
    again, setting password and email address."""
    def reset_user(user_list):
        result = {
            'result': False,
            'message': ""
        }
        try:
            for username in user_list:
                u = User.objects.get(username=username)
                u.email = ""
                u.set_password(username)
                u.save()
            User_Mod.enable_user(user_list)
            result['result'] = True
            result['message'] = "User reset successful."
        except:
            result['message'] = "Error resetting user."

        return result
