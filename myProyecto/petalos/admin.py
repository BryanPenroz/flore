from django.contrib import admin

from .models import Categoria, Flores, Ticket

# Register your models here.
admin.site.register(Flores)
admin.site.register(Categoria)
admin.site.register(Ticket)

