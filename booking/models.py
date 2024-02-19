from django.db import models


# Create your models here.
class Room(models.Model):
    SINGLE_BED = "SB"
    DOUBLE_BED = "DB"

    ROOM_TYPES = {
        SINGLE_BED: "Single Bed",
        DOUBLE_BED: "Double Bed",
    }

    room_no = models.BigAutoField(primary_key=True)
    room_type = models.CharField(max_length=2, choices=ROOM_TYPES, default=DOUBLE_BED)


class Booking(models.Model):
    SINGLE_BED = "SB"
    DOUBLE_BED = "DB"

    ROOM_TYPES = {
        SINGLE_BED: "Single Bed",
        DOUBLE_BED: "Double Bed",
    }

    room_assigned = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    guest_name = models.CharField(max_length=250)
    guest_phone = models.CharField(max_length=15)
    guest_address = models.TextField(max_length=500)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_type = models.CharField(max_length=2, choices=ROOM_TYPES, default=DOUBLE_BED)
