from django.contrib import admin
from django.utils.html import format_html
from .models import Event, Slot, Booking, Favorite


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    
    
    def poster_preview(self, obj):
        if getattr(obj, "poster", None):
            try:
                return format_html(
                    '<img src="{}" style="height:50px;width:auto;border-radius:8px;border:1px solid #ddd;" />',
                    obj.poster.url,
                )
            except Exception:
                return "Poster"
        return "-"

    poster_preview.short_description = "Poster"

    def get_list_display(self, request):
        fields = ["poster_preview"]

        
        possible = ["title", "name", "location", "place", "start_date", "end_date", "date", "created_at"]
        for f in possible:
            if hasattr(Event, f):
                fields.append(f)

        fields.append("id")
        return tuple(fields)

    def get_search_fields(self, request):
        possible = ["title", "name", "location", "place", "description"]
        return tuple([f for f in possible if hasattr(Event, f)])

    list_filter = ()
    ordering = ("-id",)


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    """
    Slot admin. If your Slot has different field names,
    you can adjust list_display below.
    """
    list_display = ("id",)
    search_fields = ()
    list_filter = ()
    ordering = ("-id",)

    def get_list_display(self, request):
        fields = ["id"]
        possible = ["event", "start_datetime", "start_time", "datetime", "capacity", "seats", "is_active"]
        for f in possible:
            if hasattr(Slot, f):
                fields.append(f)
        return tuple(fields)

    def get_search_fields(self, request):
        possible = ["event__title", "event__name"]
        return tuple(possible)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id",)
    ordering = ("-id",)

    def get_list_display(self, request):
        fields = ["id"]
        possible = ["user", "slot", "created_at", "status"]
        for f in possible:
            if hasattr(Booking, f):
                fields.append(f)
        return tuple(fields)

    def get_search_fields(self, request):
        possible = ["user__username", "slot__event__title", "slot__event__name"]
        return tuple(possible)

    list_filter = ()
    if hasattr(Booking, "status"):
        list_filter = ("status",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "created_at")
    search_fields = ("user__username", "event__title")
    ordering = ("-created_at",)
