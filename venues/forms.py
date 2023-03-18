from django import forms
from .models import Venue, VenueContact, VenueSeatType


class VenueContactForm(forms.ModelForm):
    class Meta:
        model = VenueContact
        fields = "__all__"
        labels = {
                'website': 'Website (URL Only)',
        }
        
# The extra=1 is to allow for the creation of a new formset
# without having to create a new instance of the model
# The formset is used to create a nested form in the VenueForm
VenueContactFormSet = forms.inlineformset_factory(Venue, VenueContact,max_num=1, form=VenueContactForm, can_delete=False)
        

class VenueSeatTypeForm(forms.ModelForm):
    class Meta:
        model = VenueSeatType
        fields = "__all__"
        labels = {
            'name': 'Seat Type Name',
        }

        
VenueSeatTypeFormSet = forms.inlineformset_factory(Venue, VenueSeatType, extra=1, form=VenueSeatTypeForm, can_delete=True)
VenueSeatTypeFormSetDeleteFalse = forms.inlineformset_factory(Venue, VenueSeatType, extra=1, form=VenueSeatTypeForm, can_delete=False)


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'description', 'cover_img', 'thumbnail_img', 'owner_id'] # exclude = ['contact']
        labels = {
            'name': 'Venue Name',
            'cover_img': 'Cover Image (URL Only)',
            'thumbnail_img': 'Thumbnail Image (URL Only)',
            'owner_id': 'Owner ID',
        }

 


