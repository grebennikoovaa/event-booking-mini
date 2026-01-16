from django.conf import settings
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_datetime"]

    def __str__(self):
        return f"{self.title} ({self.start_datetime:%Y-%m-%d %H:%M})"


class Slot(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="slots")
    start_datetime = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ["start_datetime"]
        unique_together = [("event", "start_datetime")]

    def __str__(self):
        return f"{self.event.title} — {self.start_datetime:%Y-%m-%d %H:%M}"


class Booking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [("slot", "user")]

    def __str__(self):
        return f"{self.user} -> {self.slot}"

    def seats_left(self) -> int:
        booked = self.bookings.count()
        left = int(self.capacity) - int(booked)
        return max(left, 0)

    def is_full(self) -> bool:
        return self.seats_left() <= 0

   