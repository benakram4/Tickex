from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RegularUser, RegularUserProfile, Reseller, ResellerProfile, User, VenueOwner, VenueOwnerProfile
from .forms import NewUserCreationForm


class NewUserAdmin(UserAdmin):
    model = User
    add_form = NewUserCreationForm
    # adds type to the admin signup form
    add_fieldsets = (   
        *UserAdmin.add_fieldsets,
        (
            'User Type',
            {
                'fields': (
                    'type',
                ),
            },
        ),
        
    )
   
    # adds the type field to the user admin page edit form
    fieldsets = (
            *UserAdmin.fieldsets,
            (
                'User Type',
                {
                    'fields': (
                        'type',
                    ),
                },
            ),
        )
            
    
# Register the User model with the UserAdmin
admin.site.register(User, NewUserAdmin)



class  RegularUserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(RegularUserProfile, RegularUserProfileAdmin)


class RegularUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(RegularUser, RegularUserAdmin)




class VenueOwnerProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(VenueOwnerProfile, VenueOwnerProfileAdmin)

class VenueOwnerAdmin(admin.ModelAdmin):
    pass

admin.site.register(VenueOwner, VenueOwnerAdmin)



class ResellerProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(ResellerProfile, ResellerProfileAdmin)

class ResellerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Reseller, ResellerAdmin)

