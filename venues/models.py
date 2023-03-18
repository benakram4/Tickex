from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Venue relate models
# ===================
class Venue(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    contact = models.OneToOneField("venues.VenueContact", on_delete=models.CASCADE, related_name='venue', blank=True, null=True)
    #img will can be only a url to an image in owr model 
    cover_img = models.URLField(blank=True, null=True)
    thumbnail_img = models.URLField(blank=True, null=True)
    owner_id = models.ForeignKey("users.User" ,on_delete=models.CASCADE, related_name='venues')
    
    
    def __str__(self):
        return f'{self.name}({self.id})'
    
class VenueContact(models.Model):
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    street = models.CharField(max_length=30, blank=False)
    postal_code = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=30, blank=False)
    province = models.CharField(max_length=20, blank=False)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    venue_id = models.ForeignKey("venues.Venue", on_delete=models.CASCADE, related_name='contacts')
  
    
    def __str__(self):
        return f'{self.venue_id.name}({self.id}) contact info'
    
    
class VenuesSeatTypeManger(models.Manager):
    # this method will return the total number of seats for a venue for a specific seat type
    def get_total_seats_for_venue(self, venue_id, seat_type_id):
        venue = Venue.objects.get(id=venue_id)
        seat_type = venue.seat_types.get(id=seat_type_id)
        return seat_type.total_seats


class VenueSeatType(models.Model):
    name = models.CharField(max_length=100)
    venue_id = models.ForeignKey("Venue", on_delete=models.CASCADE, related_name='seat_types')
    total_seats = models.IntegerField(default=0,blank=False)
    
    objects = VenuesSeatTypeManger()
    
    def __str__(self):
        return f'{self.name} at ({self.venue_id.name})'
    
# End of Venue relate models
# ==========================

# when a VenueContact is created it will assign the contact object to the venue contact field   
@receiver(post_save, sender=VenueContact)
def assign_contact_to_venue(sender, instance, created, **kwargs):
    if created:
        instance.venue_id.contact = instance
        instance.venue_id.save()
        


                