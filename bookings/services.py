from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Slot, Booking


@transaction.atomic
def create_booking(*, slot_id: int, user) -> Booking:
    slot = Slot.objects.select_for_update().get(id=slot_id)

    if Booking.objects.filter(slot=slot, user=user).exists():
        raise ValidationError("You are already booked for this slot.")

    booked_count = Booking.objects.filter(slot=slot).count()
    if booked_count >= slot.capacity:
        raise ValidationError("No seats left for this slot.")

    booking = Booking.objects.create(slot=slot, user=user)
    return booking


@transaction.atomic
def cancel_booking(*, slot_id: int, user) -> None:
    slot = Slot.objects.select_for_update().get(id=slot_id)

    deleted, _ = Booking.objects.filter(slot=slot, user=user).delete()
    if deleted == 0:
        raise ValidationError("You have no booking for this slot.")
