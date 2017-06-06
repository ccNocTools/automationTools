from tools.models import Device_Database


def is_admin_processor(request):
    is_admin = str(request.user.is_superuser)
    return {'is_admin': is_admin}


def device_database_processor(request):
    return {
        'device_database': Device_Database.objects.all()
    }