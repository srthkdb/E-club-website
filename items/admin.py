from django.contrib import admin
from .models import Box, Issued

#these are the classes(tables of database) which can be viewed from django admin panel
admin.site.register(Box)
admin.site.register(Issued)