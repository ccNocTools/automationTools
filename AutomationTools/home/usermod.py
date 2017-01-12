from django.contrib.auth.models import User


class User_Mod:

    def does_user_exist(username):
        return User.objects.filter(username=username).exists()

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

    def set_password(username, old_password, new_password, confirm_password):
        result = {
            'result': False,
            'message': ""
        }

        if not User_Mod.does_user_exist(username):
            result['message'] = "Username " + username + " does not exist."
        else:
            user = User.objects.get(username=username)
            if not user.check_password(old_password):
                result['message'] = "Incorrect password."
            elif new_password != confirm_password:
                result['message'] = "Password confirmation does not match new password."
            elif len(new_password) < 8:
                result['message'] = "Password must be 8 characters or longer."
            else:
                try:
                    user.set_password(new_password)
                    user.save()
                    result['result'] = True
                    result['message'] = "Password change successful."
                except:
                    result['message'] = "Error changing password."

        return result

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
