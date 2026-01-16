from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from .models import Event, Slot, Booking
from .services import create_booking, cancel_booking


def home(request):
    return redirect("event_list")


def event_list(request):
    events = Event.objects.filter(is_published=True).order_by("start_datetime")

    for e in events:
        e.next_slot = e.slots.first()  

    return render(request, "bookings/event_list.html", {"events": events})


def event_detail(request, event_id: int):
    event = get_object_or_404(Event, id=event_id, is_published=True)

   

    user_booked_slot_ids = set()
    if request.user.is_authenticated:
        user_booked_slot_ids = set(
            Booking.objects.filter(user=request.user, slot__event=event)
            .values_list("slot_id", flat=True)
        )

    return render(
        request,
        "bookings/event_detail.html",
        {
            "event": event,
            "slots": slots,
            "user_booked_slot_ids": user_booked_slot_ids,
        },
    )


@login_required
def book_slot(request, slot_id: int):
    if request.method != "POST":
        return redirect("event_list")

    slot = get_object_or_404(Slot, id=slot_id)

    try:
        create_booking(slot_id=slot.id, user=request.user)
        messages.success(request, "Booked ✅")
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect("event_detail", event_id=slot.event_id)


@login_required
def cancel_slot(request, slot_id: int):
    if request.method != "POST":
        return redirect("event_list")

    slot = get_object_or_404(Slot, id=slot_id)

    try:
        cancel_booking(slot_id=slot.id, user=request.user)
        messages.success(request, "Cancelled ✅")
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect("event_detail", event_id=slot.event_id)
