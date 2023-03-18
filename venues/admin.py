from django.contrib import admin

from . import models

class VenueAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Venue, VenueAdmin)


class VenueContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.VenueContact, VenueContactAdmin)


class VenueSeatTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.VenueSeatType, VenueSeatTypeAdmin)