from .models import Booking

def booking_count(request):
    if request.user.is_authenticated:
        count = Booking.objects.filter(user=request.user).count()
        return {"booking_count": count}
    return {"booking_count": 0}
