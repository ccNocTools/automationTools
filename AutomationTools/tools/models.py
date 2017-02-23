from django.db import models


"""This class has a single field which holds the current community string."""


class Community_String(models.Model):
    community_string = models.CharField(max_length = 250, default='')


"""This class contains the device database. Each device has all the fields in this class."""


class Device_Database(models.Model):
    device_name = models.CharField(max_length = 250, default='')
    ip_address = models.CharField(max_length = 250, default='')
    os_version = models.CharField(max_length = 250, default='')
