from django.contrib import admin
from .models import Event, Slot, Booking


class SlotInline(admin.TabularInline):
    model = Slot
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_datetime", "location", "is_published")
    list_filter = ("is_published", "start_datetime")
    search_fields = ("title", "location")
    inlines = [SlotInline]


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("event", "start_datetime", "capacity")
    list_filter = ("event", "start_datetime")
    search_fields = ("event__title",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "slot", "created_at")
    list_filter = ("created_at", "slot__event")
    search_fields = ("user__username", "slot__event__title")
