from django.contrib.auth.models import AbstractUser
from django.db import models

# auto creates/deletes a profile for each user when they register/deleted
# first a custom user model is created, then a specific user is created according to the type of user
from django.db.models.signals import post_save, post_delete
# used to receive signals of post_save and post_delete, etc.
from django.dispatch import receiver
from django.forms import ValidationError  # used to raise validation errors


# we create a custom user model that inherits from AbstractUser,
# this custom user model is exactly the same as the default user model if we didn't add any fields to it.
# We do it so we can use the default user model for venuesOwner and add more fields to it
class User(AbstractUser):
    # TextChoices type is enum
    class Types(models.TextChoices):
        # EXAMPLE:
        # [ENUM_NAME] = '[ENUM_VALUE]', '[ENUM_DISPLAY_NAME](optional, if not provided, the enum value will be used, good for front-end use such as forms)'
        REGULAR_USER = 'REGULAR', 'Regular User'
        VENUE_OWNER = 'VENUE_OWNER', 'Venue Owner'
        RESELLER = 'RESELLER', 'Reseller'
        ADMIN = 'ADMIN', 'Admin'

    type = models.CharField(
        max_length=20,
        choices=Types.choices,
        default=Types.ADMIN,  # default type is admin
    )
    
    def get_user_type(self):
        return self.Types(self.type).label

    # this override the way the user is displayed in the admin panel
    def __str__(self):
        return f'{self.username} is a {self.get_user_type()}'





# This create a real model/table in the database, it is not a proxy model like the RegularUser model
# this model is used to store extra information about the user
# each custom user in liked to the base user model by a one to one relationship
# the cascade option means that if the user is deleted, the profile will be deleted as well
class RegularUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='regular_user_profile')
    orders = models.ManyToManyField(
        "tickets.Ticket", related_name='buyers', blank=True)
    
    # only regular users can have this profile
    def save (self, *args, **kwargs):
        if self.user.type != User.Types.REGULAR_USER:
            raise ValidationError("User type is not regular user")
        super().save(*args, **kwargs)
        
    # this override the way the user is displayed in the admin panel
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


# this is will power queries like RegularUser.objects.all()
class RegularUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Types.REGULAR_USER)

class RegularUser(User):
    
    # this will set the type of the user to regular user
    type = User.Types.REGULAR_USER
    
    #this will power queries like RegularUser.objects.all()
    objects = RegularUserManager()
    
    # Add a property to the User model to easily access the ResellerProfile
    @property
    def profile(self):
        return self.regular_user_profile # this refers to the RegularUserProfile model "related_name"

    # proxy true means that this model is not stored in the database and it is driven by the User model
    class Meta:
        proxy = True
        







class ResellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reseller_profile')
    orders = models.ManyToManyField(
        "tickets.Ticket", related_name='resellers', blank=True)
    
    # only reseller users can have this profile
    def save (self, *args, **kwargs):
        if self.user.type != User.Types.RESELLER:
            raise ValidationError("User type is not Reseller user")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class ResellerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Types.RESELLER)
    
    
class Reseller(User):
    
    type = User.Types.RESELLER
    
    objects = ResellerManager()
    
    @property
    def profile(self):
        return self.reseller_profile

    class Meta:
        proxy = True
        

    
    
    
class VenueOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='venue_owner_profile')
    orders = models.ManyToManyField(
        "tickets.Ticket", related_name='venue_owners', blank=True)
    
    # only Venue owner users can have this profile
    def save (self, *args, **kwargs):
        if self.user.type != User.Types.VENUE_OWNER:
            raise ValidationError("User type is not Venue owner user")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
 

class VenueOwnerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Types.VENUE_OWNER)   


class VenueOwner(User):
    
    type = User.Types.VENUE_OWNER
    
    objects = VenueOwnerManager()
    
    @property
    def profile(self):
        return self.venue_owner_profile

    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.venue_owner_profile.user.first_name} {self.venue_owner_profile.user.last_name}'



# this receiver will be called when a new user is created
# and will create a specific user according to the type of user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.type == User.Types.REGULAR_USER:
            RegularUserProfile.objects.create(user=instance)
        elif instance.type == User.Types.VENUE_OWNER:
            VenueOwnerProfile.objects.create(user=instance)
        elif instance.type == User.Types.RESELLER:
            ResellerProfile.objects.create(user=instance)
        elif instance.type == User.Types.ADMIN:
            raise ValidationError("Admin user can be created only by the IT team")
        else:
            raise ValidationError("User type is not valid")



# Listen for the pre_delete signal of each specific user model and delete the corresponding User instance.
@receiver(post_delete, sender=RegularUserProfile)
def delete_regular_user(sender, instance, **kwargs):
    instance.user.delete()


@receiver(post_delete, sender=VenueOwnerProfile)
def delete_venue_owner(sender, instance, **kwargs):
    instance.user.delete()


@receiver(post_delete, sender=ResellerProfile)
def delete_reseller(sender, instance, **kwargs):
    instance.user.delete()
