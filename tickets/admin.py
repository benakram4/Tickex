from django.contrib import admin

from . import models

class TicketAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Ticket, TicketAdmin)