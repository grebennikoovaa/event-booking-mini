from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Q, Min
from django.contrib.auth import login
from .forms import SignUpForm



from .models import Event, Slot, Booking, Favorite
from .services import create_booking, cancel_booking


def home(request):
    return redirect("event_list")


def event_list(request):
    sort = request.GET.get("sort", "soon")  

    qs = Event.objects.all()

    qs = qs.annotate(next_slot=Min("slots__start_datetime"))

    if sort == "newest":
        qs = qs.order_by("-id")
    elif sort == "title":
        qs = qs.order_by("title")
    else:  
        qs = qs.order_by("next_slot", "title")
    
    fav_ids = set()
    if request.user.is_authenticated:
        fav_ids = set(
            Favorite.objects.filter(user=request.user).values_list("event_id", flat=True)
        )

    return render(
        request,
        "bookings/event_list.html",
        {"events": qs, "sort": sort, "fav_ids": fav_ids},
    )


def event_detail(request, event_id: int):
    event = get_object_or_404(Event, id=event_id, is_published=True)

    slots = event.slots.all()

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
        messages.success(request, "Booking was completely successful!")
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
        messages.success(request, "Cancelled")
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect("event_detail", event_id=slot.event_id)

@login_required
def my_bookings(request):
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("slot", "slot__event")
        .order_by("-created_at")
    )

    return render(request, "bookings/my_bookings.html", {"bookings": bookings})

def landing(request):
    return render(request, "landing.html")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("event_list")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def toggle_favorite(request, event_id):
    if request.method != "POST":
        return redirect("event_list")

    event = get_object_or_404(Event, id=event_id)

    fav, created = Favorite.objects.get_or_create(user=request.user, event=event)
    if not created:
        fav.delete()
        messages.info(request, "Removed from favorites.")
    else:
        messages.success(request, "Added to favorites!")

    return redirect(request.META.get("HTTP_REFERER", "event_list"))

@login_required
def profile(request):
    favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("event")
        .order_by("-created_at")
    )

    my_bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("slot", "slot__event")
        .order_by("-id")
    )

    return render(
        request,
        "bookings/profile.html",
        {"favorites": favorites, "my_bookings": my_bookings},
    )