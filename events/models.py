from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Event related models
# ===================
class Event(models.Model):
    class CategoryOptions(models.TextChoices):
        CONCERT = 'CONCERT', 'Concert'
        THEATER = 'THEATER', 'Theater'
        SPORTS = 'SPORTS', 'Sports'
        OTHERS = 'OTHERS', 'Others' 

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=CategoryOptions.choices, default=CategoryOptions.OTHERS)
    cover_img = models.URLField(blank=True)
    thumbnail_img = models.URLField(blank=True)
    venue_id = models.ForeignKey("venues.Venue", on_delete=models.CASCADE, related_name='events')
    date = models.DateField(blank=False, null=False)
    time = models.TimeField(blank=False, null=False)
    
    def __str__(self):
        return f'{self.name}({self.id})'
    
    class Meta:
        unique_together = ('name', 'date', 'time', 'venue_id')
    

class EventSeatTypeManager(models.Manager):
    # this method will return the total number of seats for a venue for a specific seat type
    def get_total_seats_for_event(self, event_id, seat_type_id):
        event = Event.objects.get(id=event_id)
        venue = event.venue_id
        seat_type = venue.seat_types.get(id=seat_type_id)
        event_seat_type = self.get(event_id=event_id, venue_seat_type_id=seat_type_id)
        event_total_seats = seat_type.total_seats * event_seat_type.available_seats / 100
        return int(event_total_seats)
    
    def get_seat_type_price(self, event_id, seat_type_id):
        event_seat_type = self.get(event_id=event_id, venue_seat_type_id=seat_type_id)
        return event_seat_type.price
    
    def update_available_seats(self, event_id, seat_type_id, seats):
        event_seat_type = self.get(event_id=event_id, venue_seat_type_id=seat_type_id)
        event_seat_type.available_seats = seats
        event_seat_type.save()
        return event_seat_type.available_seats



class EventSeatType(models.Model):
    event_id = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    venue_seat_type_id = models.ForeignKey("venues.VenueSeatType", on_delete=models.CASCADE)
    available_seats = models.DecimalField(max_digits=5, decimal_places=2, default=100.00, validators=[MaxValueValidator(100.00), MinValueValidator(0.00)])
    price = models.DecimalField(max_digits=8, decimal_places=2, default = 0.00)
    
    objects = EventSeatTypeManager()
    
    
    def __str__(self):
        return f'{self.event_id.name}({self.event_id.id}) seat type: {self.venue_seat_type_id.name}({self.venue_seat_type_id.id})'

    class Meta:
        unique_together = ('event_id', 'venue_seat_type_id')

# End of Event relate models
# ==========================