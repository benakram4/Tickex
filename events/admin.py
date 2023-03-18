from django.contrib import admin

from . import models

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Event, EventAdmin)

class EventSeatTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.EventSeatType, EventSeatTypeAdmin)
  