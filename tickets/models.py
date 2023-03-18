from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import Event, EventSeatType
from users.models import RegularUserProfile, ResellerProfile, User
from venues.models import VenueSeatType



# Tickets relate models
# =====================
class Ticket(models.Model):
    event_id = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name='tickets')
    seat_type_id = models.ForeignKey("venues.VenueSeatType", on_delete=models.CASCADE, related_name='tickets')
    buyer_id = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='tickets')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(500)])
    bought_at = models.DateTimeField(auto_now_add=True) # might be helpful for venue owner to know when the ticket was bought to improve analytics
    

    def __str__(self):
        return f'{self.buyer_id} bought {self.quantity} {self.seat_type_id} tickets for {self.event_id}'
    

@receiver(post_save, sender=Ticket)
def add_to_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.buyer_id.type == User.Types.REGULAR_USER:
            instance.buyer_id.regular_user_profile.orders.add(instance)
            venue_owner = instance.event_id.venue_id.owner_id.venue_owner_profile
            venue_owner.orders.add(instance)
        elif instance.buyer_id.type == User.Types.RESELLER:
            instance.buyer_id.reseller_profile.orders.add(instance)
            venue_owner = instance.event_id.venue_id.owner_id.venue_owner_profile
            venue_owner.orders.add(instance)
        elif instance.buyer_id.type == User.Types.VENUE_OWNER:
            instance.buyer_id.venue_owner_profile.orders.add(instance)
            
@receiver(post_save, sender=Ticket)
def dec_ticket_count(sender, instance, created, **kwargs):
    if created:
        event_pk = instance.event_id.id
        seat_type_pk = instance.seat_type_id.id
        venue_num_seats = VenueSeatType.objects.get(pk=seat_type_pk).total_seats
        event_seat_num = EventSeatType.objects.get_total_seats_for_event(event_pk, seat_type_pk)
        
        # subtract the number of tickets bought from the event_seat_num
        event_seat_num = event_seat_num - instance.quantity
        
        # get the percentage of the number of event_seat_num to the venue_num_seats
        percentage = (event_seat_num / venue_num_seats) * 100

        # save the percentage to the to EventSeatType.objects.get(pk=event_pk).available_seats
        EventSeatType.objects.update_available_seats(event_pk, seat_type_pk, percentage)
        


        
        # print("X" ,seat_type_pk, "X", venue_num_seats, "X", event_seat_num, "X", instance.quantity, "X", percentage, "X", "X",)
        
        
# End of Tickets relate models
# ============================ 