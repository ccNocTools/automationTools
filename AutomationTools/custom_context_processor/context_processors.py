
def is_admin_processor(request):
    is_admin = str(request.user.is_superuser)
    return {'is_admin': is_admin}
